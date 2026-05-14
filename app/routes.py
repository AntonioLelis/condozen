from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from .models import Usuario, Chamado

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
@login_required
def dashboard():
    # Buscamos todos os chamados. 
    # Se for Morador, vê só os dele. Se for Síndico/Zelador, vê todos.
    if current_user.perfil == 'morador':
        todos_chamados = Chamado.query.filter_by(autor_id=current_user.id).all()
    else:
        todos_chamados = Chamado.query.all()

    # Separando os chamados por status para facilitar no HTML
    dados_kanban = {
        'aberto': [c for c in todos_chamados if c.status == 'Aberto'],
        'andamento': [c for c in todos_chamados if c.status == 'Em Andamento'],
        'concluido': [c for c in todos_chamados if c.status == 'Concluído']
    }

    return render_template('dashboard.html', kanban=dados_kanban)
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))