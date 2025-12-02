from app import db

class NotaFiscal(db.Model):
    __tablename__ = 'notas_fiscais'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    recebimento = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50))
    descricao = db.Column(db.String(200))

    # Chave estrangeira para Fornecedor (opcional)
    # fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))

    def __init__(self, codigo, recebimento, valor, tipo, descricao):
        self.codigo = codigo
        self.recebimento = recebimento
        self.valor = valor
        self.tipo = tipo
        self.descricao = descricao

    def exibir_nota_fiscal(self):
        return f"""
          Código: {self.codigo}
          Recebimento: {self.recebimento}
          Valor: R${self.valor:.2f}
          Tipo: {self.tipo}
          Descrição: {self.descricao}
          """
