from app import db
from app.models.fornecedor import Fornecedor

class FornecedorRepository:
    def salvar(self, fornecedor: Fornecedor):
        try:
            db.session.add(fornecedor)
            db.session.commit()
            print(f"Fornecedor {fornecedor.nome} salvo.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar fornecedor: {e}")
            raise e

    def listar_fornecedores(self):
        return Fornecedor.query.all()

    def buscar_por_cnpj(self, cnpj: str):
        return Fornecedor.query.filter_by(cnpj=cnpj).first()

    def buscar_por_id(self, id: int):
        return Fornecedor.query.get(id)

    def criar_fornecedor(self, nome, cnpj, endereco, contato):
        novo_fornecedor = Fornecedor(
            nome=nome,
            cnpj=cnpj,
            endereco=endereco,
            contato=contato
        )
        self.salvar(novo_fornecedor)
        return novo_fornecedor
