from app.models import db, Chamado, Usuario

def test_acesso_dashboard_sem_login(client):
    """Garante que a rota /dashboard está protegida"""
    response = client.get('/dashboard')
    # 302 é o código HTTP para redirecionamento (mandando de volta pro login)
    assert response.status_code == 302

def test_dashboard_renderiza_kanban(client, app):
    """Loga, cria um chamado e verifica se ele aparece na coluna correta do Kanban"""
    
    # 1. Fazemos o login usando o usuário criado lá no conftest.py
    client.post('/login', data={
        'email': 'teste@condozen.com',
        'senha': 'senha123'
    })

    # 2. Injetamos um chamado de teste no banco de dados temporário
    with app.app_context():
        usuario = Usuario.query.filter_by(email="teste@condozen.com").first()
        
        chamado_teste = Chamado(
            titulo="Vazamento na Piscina",
            descricao="Cano estourado perto da bomba",
            local_ocorrencia="Área de Lazer",
            prioridade="Alta",
            status="Aberto", # Vai ter que cair na primeira coluna
            autor_id=usuario.id
        )
        db.session.add(chamado_teste)
        db.session.commit()

    # 3. Acessamos o dashboard logados
    response = client.get('/dashboard')
    
    # 4. As verificações (Asserts)
    assert response.status_code == 200 # Página carregou
    assert b"Vazamento na Piscina" in response.data # O título do chamado está no HTML
    assert b"Aberto (1)" in response.data # A contagem da coluna atualizou para 1