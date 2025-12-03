from app.repositories.finance_repository import FinanceRepository
from app.repositories.fornecedor_repository import FornecedorRepository
from app.models.boleto import Boleto
from app.models.nota_fiscal import NotaFiscal
from datetime import datetime

class FinanceService:
    def __init__(self):
        self.finance_repository = FinanceRepository()
        self.fornecedor_repository = FornecedorRepository()

    def obter_resumo_dashboard(self, usuario_id: int):
        # Lógica de negócio para calcular totais
        boletos = self.finance_repository.listar_boletos_por_usuario(usuario_id)
        notas = self.finance_repository.listar_notas_fiscais_por_usuario(usuario_id)
        
        # Calcular totais
        a_vencer = sum(b.valor for b in boletos if b.status == "A vencer")
        vencidos = sum(b.valor for b in boletos if b.status == "Vencido")
        pagos = sum(n.valor for n in notas if n.pago)
        
        return {
            "a_vencer": a_vencer,
            "vencidos": vencidos,
            "pagos": pagos
        }

    def listar_boletos(self, usuario_id: int):
        return self.finance_repository.listar_boletos_por_usuario(usuario_id)

    def listar_notas_fiscais(self, usuario_id: int):
        return self.finance_repository.listar_notas_fiscais_por_usuario(usuario_id)

    def obter_nota_por_id(self, nota_id: int, usuario_id: int):
        nota = self.finance_repository.buscar_nota_por_id(nota_id)
        # Verificar se a nota pertence ao usuário
        if nota and nota.usuario_id == usuario_id:
            return nota
        return None

    def atualizar_status_nota(self, nota_id: int, pago: bool, usuario_id: int):
        nota = self.obter_nota_por_id(nota_id, usuario_id)
        if nota:
            return self.finance_repository.atualizar_status_nota(nota_id, pago)
        return None

    def listar_fornecedores(self):
        return self.fornecedor_repository.listar_fornecedores()

    def criar_boleto(self, status, codigo, vencimento, valor, tipo, descricao, usuario_id, fornecedor_id=None):
        try:
            boleto = Boleto(
                status=status,
                codigo=codigo,
                vencimento=vencimento,
                valor=valor,
                tipo=tipo,
                descricao=descricao,
                usuario_id=usuario_id,
                fornecedor_id=fornecedor_id
            )
            self.finance_repository.salvar_boleto(boleto)
            return boleto
        except Exception as e:
            print(f"Erro ao criar boleto: {e}")
            raise e

    def criar_nota_fiscal(self, codigo, recebimento, valor, tipo, descricao, usuario_id, fornecedor_id=None, pago=False):
        try:
            nota = NotaFiscal(
                codigo=codigo,
                recebimento=recebimento,
                valor=valor,
                tipo=tipo,
                descricao=descricao,
                usuario_id=usuario_id,
                fornecedor_id=fornecedor_id,
                pago=pago
            )
            self.finance_repository.salvar_nota_fiscal(nota)
            return nota
        except Exception as e:
            print(f"Erro ao criar nota fiscal: {e}")
            raise e
