from app import db

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    endereco = db.Column(db.String(200))
    contato = db.Column(db.String(50))

    def __init__(self, nome, cnpj, endereco, contato):
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
        self.contato = contato
