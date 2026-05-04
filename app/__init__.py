from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Importa e registra as rotas (que criaremos depois)
    from .routes import main
    app.register_blueprint(main)

    return app