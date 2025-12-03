from app import db
from app.models.boleto import Boleto
from app.models.nota_fiscal import NotaFiscal
from app.models.fornecedor import Fornecedor
from sqlalchemy import or_

class FinanceRepository:
    def salvar_boleto(self, boleto: Boleto):
        try:
            db.session.add(boleto)
            db.session.commit()
            print(f"Boleto {boleto.codigo} salvo.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar boleto: {e}")
            raise e

    def salvar_nota_fiscal(self, nota: NotaFiscal):
        try:
            db.session.add(nota)
            db.session.commit()
            print(f"Nota Fiscal {nota.codigo} salva.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar nota fiscal: {e}")
            raise e

    def listar_boletos(self, search_query=None, status_filter=None):
        query = Boleto.query.join(Fornecedor, Fornecedor.id == Boleto.fornecedor_id, isouter=True)

        if status_filter:
            query = query.filter(Boleto.status == status_filter)
        
        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(
                or_(
                    Boleto.codigo.ilike(search_term),
                    Boleto.descricao.ilike(search_term),
                    Fornecedor.nome.ilike(search_term)
                )
            )
            
        return query.all()

    def listar_notas_fiscais(self, search_query=None, status_filter=None):
        query = NotaFiscal.query.join(Fornecedor, Fornecedor.id == NotaFiscal.fornecedor_id, isouter=True)

        if status_filter:
            if status_filter == 'Pago':
                query = query.filter(NotaFiscal.pago == True)
            elif status_filter == 'Não Pago':
                query = query.filter(NotaFiscal.pago == False)

        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(
                or_(
                    NotaFiscal.codigo.ilike(search_term),
                    NotaFiscal.descricao.ilike(search_term),
                    Fornecedor.nome.ilike(search_term)
                )
            )

        return query.all()

    def buscar_nota_por_id(self, nota_id: int):
        return NotaFiscal.query.get(nota_id)

    def atualizar_status_nota(self, nota_id: int, pago: bool):
        try:
            nota = NotaFiscal.query.get(nota_id)
            if not nota:
                return None
            nota.pago = pago
            db.session.add(nota)
            db.session.commit()
            return nota
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar status da nota: {e}")
            raise e

    def buscar_boleto_por_id(self, boleto_id: int):
        return Boleto.query.get(boleto_id)

    def atualizar_status_boleto(self, boleto_id: int, status: str):
        try:
            boleto = Boleto.query.get(boleto_id)
            if not boleto:
                return None
            boleto.status = status
            db.session.add(boleto)
            db.session.commit()
            return boleto
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar status do boleto: {e}")
            raise e

    def deletar_nota_fiscal(self, nota_id: int):
        try:
            nota = self.buscar_nota_por_id(nota_id)
            if nota:
                db.session.delete(nota)
                db.session.commit()
                print(f"Nota fiscal com ID {nota_id} deletada.")
            else:
                print(f"Nota fiscal com ID {nota_id} não encontrada.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar nota fiscal: {e}")
            raise e

    def atualizar_nota_fiscal(self, nota_id, codigo, recebimento, valor, tipo, descricao, fornecedor_id, pago):
        try:
            nota = self.buscar_nota_por_id(nota_id)
            if nota:
                nota.codigo = codigo
                nota.recebimento = recebimento
                nota.valor = valor
                nota.tipo = tipo
                nota.descricao = descricao
                nota.fornecedor_id = fornecedor_id
                nota.pago = pago
                db.session.commit()
                print(f"Nota fiscal com ID {nota_id} atualizada.")
                return nota
            else:
                print(f"Nota fiscal com ID {nota_id} não encontrada.")
                return None
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar nota fiscal: {e}")
            raise e

    def atualizar_boleto(self, boleto_id, codigo, vencimento, valor, tipo, descricao, fornecedor_id, status):
        try:
            boleto = self.buscar_boleto_por_id(boleto_id)
            if boleto:
                boleto.codigo = codigo
                boleto.vencimento = vencimento
                boleto.valor = valor
                boleto.tipo = tipo
                boleto.descricao = descricao
                boleto.fornecedor_id = fornecedor_id
                boleto.status = status
                db.session.commit()
                print(f"Boleto com ID {boleto_id} atualizado.")
                return boleto
            else:
                print(f"Boleto com ID {boleto_id} não encontrado.")
                return None
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar boleto: {e}")
            raise e

    def deletar_boleto(self, boleto_id: int):
        try:
            boleto = self.buscar_boleto_por_id(boleto_id)
            if boleto:
                db.session.delete(boleto)
                db.session.commit()
                print(f"Boleto com ID {boleto_id} deletado.")
            else:
                print(f"Boleto com ID {boleto_id} não encontrado.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar boleto: {e}")
            raise e
