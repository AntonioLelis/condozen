import os
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from .models import db, Usuario

load_dotenv()

# Inicializa o LoginManager
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Se tentar acessar página bloqueada, joga pra cá
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

def create_app():
    app = Flask(__name__)
    
    # Chave secreta obrigatória para gerenciar a sessão do usuário com segurança
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-super-secreta-provisoria')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Ensina o Flask-Login a achar o usuário pelo ID
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    from .routes import main
    app.register_blueprint(main)

    return app