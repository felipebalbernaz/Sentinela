from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cpf = db.Column(db.String(14), unique=True)

    # Relacionamentos
    boletos = db.relationship('Boleto', backref='usuario', lazy=True, cascade='all, delete-orphan')
    notas_fiscais = db.relationship('NotaFiscal', backref='usuario', lazy=True, cascade='all, delete-orphan')

    def __init__(self, nome, email, senha, telefone=None, endereco=None, cpf=None):
        self.nome = nome
        self.email = email
        self.set_senha(senha)  # Usa hash ao invés de texto puro
        self.telefone = telefone
        self.endereco = endereco
        self.cpf = cpf

    def set_senha(self, senha):
        """Define a senha usando hash"""
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return check_password_hash(self.senha_hash, senha)

    @property
    def senha(self):
        """Propriedade para compatibilidade (não deve ser usada diretamente)"""
        raise AttributeError('Senha não é um atributo legível. Use check_senha() para verificar.')

    def excluir_conta(self):
        """Lógica para excluir conta (pode ser apenas desativar ou remover do DB)"""
        db.session.delete(self)
        db.session.commit()
        print("Conta excluída com sucesso!")
