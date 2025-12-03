from app import db
from app.models.boleto import Boleto
from app.models.nota_fiscal import NotaFiscal

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

    def listar_boletos(self):
        return Boleto.query.all()

    def listar_notas_fiscais(self):
        return NotaFiscal.query.all()

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
