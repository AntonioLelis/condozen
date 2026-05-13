from invoke import task
from app import create_app
from app.models import db, Usuario, Chamado
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

@task
def test(c):
    """Roda os testes automatizados usando o pytest"""
    print("🧪 Rodando suíte de testes...")
    c.run("pytest -v")

@task
def popular_kanban(c):
    """Gera chamados de teste para visualizar o Kanban"""
    app = create_app()
    with app.app_context():
        admin = Usuario.query.filter_by(email='admin@condozen.com').first()
        if not admin:
            print("❌ Erro: Rode 'inv criar-admin' primeiro.")
            return

        chamados = [
            Chamado(titulo="Lâmpada queimada Hall", descricao="Bloco B, 3º andar", local_ocorrencia="Área Comum", prioridade="Baixa", status="Aberto", autor_id=admin.id),
            Chamado(titulo="Vazamento Garagem", descricao="Cano estourado vaga 42", local_ocorrencia="Subsolo 1", prioridade="Alta", status="Aberto", autor_id=admin.id),
            Chamado(titulo="Manutenção Elevador", descricao="Elevador social parado", local_ocorrencia="Bloco A", prioridade="Média", status="Em Andamento", autor_id=admin.id),
            Chamado(titulo="Pintura Portão", descricao="Retoque no portão principal", local_ocorrencia="Entrada", prioridade="Baixa", status="Concluído", autor_id=admin.id),
        ]

        for c in chamados:
            db.session.add(c)
        
        db.session.commit()
        print("✅ Kanban populado com sucesso!")