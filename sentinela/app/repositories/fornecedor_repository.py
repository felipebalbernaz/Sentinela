from app import db
from app.models.fornecedor import Fornecedor
from sqlalchemy import or_

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

    def listar_fornecedores(self, search_query=None):
        query = Fornecedor.query

        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(
                or_(
                    Fornecedor.nome.ilike(search_term),
                    Fornecedor.cnpj.ilike(search_term),
                    Fornecedor.endereco.ilike(search_term),
                    Fornecedor.contato.ilike(search_term)
                )
            )

        return query.all()

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

    def deletar(self, fornecedor_id: int):
        try:
            fornecedor = self.buscar_por_id(fornecedor_id)
            if fornecedor:
                db.session.delete(fornecedor)
                db.session.commit()
                print(f"Fornecedor com ID {fornecedor_id} deletado.")
            else:
                print(f"Fornecedor com ID {fornecedor_id} não encontrado.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar fornecedor: {e}")
            raise e

    def atualizar_fornecedor(self, fornecedor_id, nome, cnpj, endereco, contato):
        try:
            fornecedor = self.buscar_por_id(fornecedor_id)
            if fornecedor:
                fornecedor.nome = nome
                fornecedor.cnpj = cnpj
                fornecedor.endereco = endereco
                fornecedor.contato = contato
                db.session.commit()
                print(f"Fornecedor com ID {fornecedor_id} atualizado.")
                return fornecedor
            else:
                print(f"Fornecedor com ID {fornecedor_id} não encontrado.")
                return None
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar fornecedor: {e}")
            raise e
