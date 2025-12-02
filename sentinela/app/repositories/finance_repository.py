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
