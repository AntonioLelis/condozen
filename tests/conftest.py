import pytest
from app import create_app
from app.models import db, Usuario
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    # Cria o app e força as configurações para modo de teste
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    # Cria o contexto, o banco falso e um usuário para testarmos
    with app.app_context():
        db.create_all()
        
        usuario_teste = Usuario(
            nome="Usuário de Teste",
            email="teste@condozen.com",
            senha_hash=generate_password_hash("senha123"),
            perfil="morador"
        )
        db.session.add(usuario_teste)
        db.session.commit()

        yield app

        # Limpa tudo depois que os testes rodam
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    # Ferramenta do Flask que simula o navegador acessando nossas rotas
    return app.test_client()