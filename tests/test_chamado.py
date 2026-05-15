from app.models import db, Chamado, Usuario


def test_pagina_novo_chamado_carrega(client):
    """Garante que a pagina de novo chamado retorna 200 quando logado."""
    client.post('/login', data={
        'email': 'teste@condozen.com',
        'senha': 'senha123'
    })

    response = client.get('/chamado/novo')
    assert response.status_code == 200
    assert 'Abrir Novo Chamado'.encode('utf-8') in response.data


def test_novo_chamado_sem_login_redireciona(client):
    """Garante que a rota /chamado/novo esta protegida para usuarios nao logados."""
    response = client.get('/chamado/novo')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_criar_chamado_com_sucesso(client, app):
    """
    Loga como morador, envia o formulario com dados validos
    e verifica se o chamado foi salvo no banco atrelado ao usuario logado.
    """
    client.post('/login', data={
        'email': 'teste@condozen.com',
        'senha': 'senha123'
    })

    response = client.post('/chamado/novo', data={
        'titulo': 'Torneira com vazamento',
        'descricao': 'Torneira do banheiro social vazando',
        'local_ocorrencia': 'Apto 201 - Bloco B',
        'prioridade': 'Alta'
    }, follow_redirects=True)

    # Deve redirecionar para o dashboard com mensagem de sucesso
    assert response.status_code == 200
    assert 'Chamado aberto com sucesso!'.encode('utf-8') in response.data

    # Verifica se o chamado foi salvo no banco
    with app.app_context():
        usuario = Usuario.query.filter_by(email='teste@condozen.com').first()
        chamado = Chamado.query.filter_by(autor_id=usuario.id).first()

        assert chamado is not None
        assert chamado.titulo == 'Torneira com vazamento'
        assert chamado.descricao == 'Torneira do banheiro social vazando'
        assert chamado.local_ocorrencia == 'Apto 201 - Bloco B'
        assert chamado.prioridade == 'Alta'
        assert chamado.status == 'Aberto'
        assert chamado.autor_id == usuario.id


def test_criar_chamado_campos_vazios(client):
    """
    Envia o formulario sem preencher os campos obrigatorios
    e verifica se a mensagem de erro aparece.
    """
    client.post('/login', data={
        'email': 'teste@condozen.com',
        'senha': 'senha123'
    })

    response = client.post('/chamado/novo', data={
        'titulo': '',
        'descricao': '',
        'local_ocorrencia': '',
        'prioridade': 'Baixa'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Preencha todos os campos'.encode('utf-8') in response.data


def test_chamado_aparece_no_dashboard(client, app):
    """
    Apos criar um chamado, ele deve aparecer na coluna 'Aberto' do Kanban.
    """
    client.post('/login', data={
        'email': 'teste@condozen.com',
        'senha': 'senha123'
    })

    # Cria o chamado via POST
    client.post('/chamado/novo', data={
        'titulo': 'Elevador com defeito',
        'descricao': 'Porta nao fecha direito',
        'local_ocorrencia': 'Bloco A',
        'prioridade': 'Urgente'
    })

    # Acessa o dashboard e verifica se o chamado aparece
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert 'Elevador com defeito'.encode('utf-8') in response.data
    assert 'Aberto (1)'.encode('utf-8') in response.data


def test_morador_ve_apenas_seus_chamados(client, app):
    """
    Morador deve ver apenas os chamados que ele mesmo abriu,
    nao os de outros usuarios.
    """
    with app.app_context():
        from werkzeug.security import generate_password_hash
        # Cria um segundo usuario morador
        outro = Usuario(
            nome='Outro Morador',
            email='outro@condozen.com',
            senha_hash=generate_password_hash('senha123'),
            perfil='morador'
        )
        db.session.add(outro)
        db.session.flush()

        # Cria um chamado do outro usuario
        chamado_alheio = Chamado(
            titulo='Chamado do Outro',
            descricao='Nao deve aparecer',
            local_ocorrencia='Apto 999',
            prioridade='Baixa',
            status='Aberto',
            autor_id=outro.id
        )
        db.session.add(chamado_alheio)
        db.session.commit()

    # Loga como o usuario de teste original
    client.post('/login', data={
        'email': 'teste@condozen.com',
        'senha': 'senha123'
    })

    response = client.get('/dashboard')
    assert response.status_code == 200
    # O chamado do outro usuario nao deve aparecer
    assert 'Chamado do Outro'.encode('utf-8') not in response.data
