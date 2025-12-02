from app import db
from datetime import datetime

class Boleto(db.Model):
    __tablename__ = 'boletos'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    codigo = db.Column(db.String(100), unique=True, nullable=False)
    vencimento = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50))
    descricao = db.Column(db.String(200))
    
    # Chave estrangeira para Fornecedor
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    fornecedor = db.relationship('Fornecedor', backref='boletos')

    def __init__(self, status, codigo, vencimento, valor, tipo, descricao, fornecedor_id=None):
        self.status = status
        self.codigo = codigo
        self.vencimento = vencimento
        self.valor = valor
        self.tipo = tipo
        self.descricao = descricao
        self.fornecedor_id = fornecedor_id

    def atualizar_status(self):
        # Lógica para atualizar status baseado no vencimento
        if datetime.combine(self.vencimento, datetime.min.time()) >= datetime.now():
            self.status = "A vencer"
        else:
            self.status = "Vencido"

    def calcular_dias_vencimento(self):
        delta = datetime.now().date() - self.vencimento
        dias = delta.days
        if dias < 0:
            return f"{abs(dias)} dia(s) até que o boleto expire."
        elif dias > 0:
            return f"{dias} dia(s) desde que o boleto expirou."
        else:
            return "O boleto expira hoje."

    def exibir_boleto(self):
        self.atualizar_status()
        return f"""
          Status: {self.status}
          Código: {self.codigo}
          Vencimento: {self.vencimento} ({self.calcular_dias_vencimento()})
          Valor: R${self.valor:.2f}
          Tipo: {self.tipo}
          Descrição: {self.descricao}
          """
