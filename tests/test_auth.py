def test_pagina_login_carrega(client):
    """Garante que a página de login retorna status 200 e tem o título"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Acesso CondoZen" in response.data

def test_login_com_sucesso(client):
    """Testa se as credenciais corretas logam o usuário e redirecionam ao dashboard"""
    response = client.post('/login', data={
        'email': 'teste@condozen.com',
        'senha': 'senha123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Bem-vindo, Usu\xc3\xa1rio de Teste!" in response.data

def test_login_senha_errada(client):
    """Testa se a senha incorreta gera a mensagem de erro"""
    response = client.post('/login', data={
        'email': 'teste@condozen.com',
        'senha': 'senha_errada'
    }, follow_redirects=True)
    
    assert b"E-mail ou senha incorretos." in response.data

def test_acesso_dashboard_sem_login(client):
    """Garante que tentar acessar /dashboard sem logar redireciona pro login"""
    response = client.get('/dashboard', follow_redirects=True)
    
    # Se ele redirecionou pro login, a frase do form deve aparecer na tela
    assert b"Acesso CondoZen" in response.data
    assert b"Bem-vindo" not in response.data