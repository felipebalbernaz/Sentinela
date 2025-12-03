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
        """Lista todos os boletos (para uso administrativo)"""
        return Boleto.query.all()

    def listar_boletos_por_usuario(self, usuario_id: int):
        """Lista boletos de um usuário específico"""
        return Boleto.query.filter_by(usuario_id=usuario_id).all()

    def listar_notas_fiscais(self):
        """Lista todas as notas fiscais (para uso administrativo)"""
        return NotaFiscal.query.all()

    def listar_notas_fiscais_por_usuario(self, usuario_id: int):
        """Lista notas fiscais de um usuário específico"""
        return NotaFiscal.query.filter_by(usuario_id=usuario_id).all()

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
