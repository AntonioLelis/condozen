from invoke import task
from app import create_app
from app.models import db, Usuario
from werkzeug.security import generate_password_hash

@task
def install(c):
    """Instala as dependencias do projeto."""
    print("📦 Instalando dependências...")
    c.run("pip install -r requirements.txt")

@task
def run(c):
    """Roda o servidor de desenvolvimento do Flask."""
    print("🚀 Subindo o servidor CondoZen...")
    c.run("python run.py")

@task
def test(c):
    """Roda os testes automatizados com pytest."""
    print("🧪 Rodando a suite de testes...")
    c.run("pytest -v")

@task
def criar_admin(c):
    """Cria um usuário síndico de teste no banco de dados"""
    app = create_app()
    with app.app_context():
        # Cria as tabelas no banco de dados (se ainda não existirem)
        db.create_all()
        
        # Verifica se o admin já existe para não duplicar
        admin_existente = Usuario.query.filter_by(email='admin@condozen.com').first()
        
        if admin_existente:
            print("⚠️ O usuário admin já existe!")
            return
            
        novo_admin = Usuario(
            nome='Síndico Teste',
            email='admin@condozen.com',
            senha_hash=generate_password_hash('123456'),
            perfil='sindico'
        )
        
        db.session.add(novo_admin)
        db.session.commit()
        print("✅ Usuário admin@condozen.com criado com sucesso! Senha: 123456")