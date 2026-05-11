from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from .models import Usuario

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    # Se o cara já tá logado, manda direto pro painel
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        # Valida se o usuário existe e se a senha digitada bate com o hash do banco
        if usuario and check_password_hash(usuario.senha_hash, senha):
            login_user(usuario)
            return redirect(url_for('main.dashboard'))
        else:
            flash('E-mail ou senha incorretos.', 'error')
            
    return render_template('login.html')

@main.route('/dashboard')
@login_required # Isso aqui é a mágica: tranca a página pra quem não tá logado
def dashboard():
    return f"<h1>Bem-vindo, {current_user.nome}!</h1><p>Você é um: {current_user.perfil}</p><a href='/logout'>Sair</a>"

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))