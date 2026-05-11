from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default='morador') # morador, zelador, sindico
    
    # Relacionamento: Um usuario pode ter varios chamados
    chamados = db.relationship('Chamado', backref='autor', lazy=True)

class Chamado(db.Model):
    __tablename__ = 'chamados'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    local_ocorrencia = db.Column(db.String(100), nullable=False) # Ex: Bloco A - Apto 302, ou Area Comum
    
    status = db.Column(db.String(20), nullable=False, default='Aberto') # Aberto, Em Andamento, Concluido
    prioridade = db.Column(db.String(20), nullable=False, default='Baixa') # Baixa, Media, Alta, Urgente
    
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    data_resolucao = db.Column(db.DateTime, nullable=True)
    
    # Chave estrangeira ligando o chamado ao usuario que o abriu
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)