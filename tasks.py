from invoke import task

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