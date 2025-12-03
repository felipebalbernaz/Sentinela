from app import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cpf = db.Column(db.String(14), unique=True)

    # Relacionamentos (opcional, para uso futuro)
    # boletos = db.relationship('Boleto', backref='usuario', lazy=True)
    # notas_fiscais = db.relationship('NotaFiscal', backref='usuario', lazy=True)

    def __init__(self, nome, email, senha, telefone, endereco, cpf):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.endereco = endereco
        self.cpf = cpf

    def excluir_conta(self):
        # Lógica para excluir conta (pode ser apenas desativar ou remover do DB)
        db.session.delete(self)
        db.session.commit()
        print("Conta excluída com sucesso!")
