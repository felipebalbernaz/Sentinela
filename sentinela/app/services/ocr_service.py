import re
import pytesseract
from PIL import Image
import cv2
import numpy as np
from datetime import datetime
from typing import Dict, Optional
import io
import os
import platform

class OCRService:
    """Serviço para processamento OCR de boletos e notas fiscais"""
    
    def __init__(self):
        # Configuração automática do caminho do Tesseract no Windows
        if platform.system() == 'Windows':
            # Caminhos comuns do Tesseract no Windows
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Pré-processa a imagem para melhorar a qualidade do OCR
        """
        # Converter bytes para imagem PIL
        image = Image.open(io.BytesIO(image_bytes))
        
        # Converter para numpy array
        img_array = np.array(image)
        
        # Converter para escala de cinza se necessário
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Aplicar threshold para melhorar contraste
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Redimensionar se a imagem for muito pequena
        height, width = thresh.shape
        if width < 600:
            scale = 600 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            thresh = cv2.resize(thresh, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        return thresh
    
    def extract_text(self, image_bytes: bytes) -> str:
        """
        Extrai texto de uma imagem usando OCR
        """
        try:
            processed_image = self.preprocess_image(image_bytes)
            text = pytesseract.image_to_string(processed_image, lang='por')
            return text
        except Exception as e:
            raise Exception(f"Erro ao processar OCR: {str(e)}")
    
    def extract_boleto_data(self, image_bytes: bytes) -> Dict[str, Optional[str]]:
        """
        Extrai dados específicos de um boleto bancário
        Retorna um dicionário com os campos extraídos
        """
        text = self.extract_text(image_bytes)
        
        data = {
            'codigo': None,
            'vencimento': None,
            'valor': None,
            'descricao': None,
            'texto_completo': text
        }
        
        # Extrair código de barras (padrão brasileiro: números com pontos e espaços)
        codigo_pattern = r'\d{5}\.?\d{5}\s+\d{5}\.?\d{6}\s+\d{5}\.?\d{6}\s+\d{1}\s+\d{14}'
        codigo_match = re.search(codigo_pattern, text.replace(' ', '').replace('.', ''))
        if codigo_match:
            codigo = codigo_match.group(0)
            # Formatar código de barras
            codigo = re.sub(r'(\d{5})(\d{5})(\d{5})(\d{6})(\d{5})(\d{6})(\d{1})(\d{14})', 
                          r'\1.\2 \3.\4 \5.\6 \7 \8', codigo)
            data['codigo'] = codigo
        
        # Extrair valor (padrão: R$ seguido de números)
        valor_patterns = [
            r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
            r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*R\$',
            r'VALOR[:\s]*R?\$?\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
            r'TOTAL[:\s]*R?\$?\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)'
        ]
        
        for pattern in valor_patterns:
            valor_match = re.search(pattern, text, re.IGNORECASE)
            if valor_match:
                valor_str = valor_match.group(1).replace('.', '').replace(',', '.')
                try:
                    data['valor'] = valor_str
                except:
                    pass
                break
        
        # Extrair data de vencimento (padrão brasileiro: DD/MM/YYYY ou DD/MM/YY)
        vencimento_patterns = [
            r'VENCIMENTO[:\s]*(\d{1,2}/\d{1,2}/\d{2,4})',
            r'VENC[:\s]*(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
        ]
        
        for pattern in vencimento_patterns:
            venc_match = re.search(pattern, text, re.IGNORECASE)
            if venc_match:
                data_str = venc_match.group(1)
                try:
                    # Tentar converter para formato YYYY-MM-DD
                    if len(data_str.split('/')[-1]) == 2:
                        # Formato DD/MM/YY
                        day, month, year = data_str.split('/')
                        year = '20' + year if int(year) < 50 else '19' + year
                    else:
                        # Formato DD/MM/YYYY
                        day, month, year = data_str.split('/')
                    
                    # Validar se é uma data válida
                    datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                    data['vencimento'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                except:
                    pass
                break
        
        # Extrair descrição (linha que contém palavras-chave)
        descricao_keywords = ['PAGAR', 'REFERENTE', 'DESCRIÇÃO', 'HISTÓRICO']
        lines = text.split('\n')
        for line in lines:
            for keyword in descricao_keywords:
                if keyword in line.upper():
                    descricao = line.split(':', 1)[-1].strip() if ':' in line else line.strip()
                    if descricao and len(descricao) > 5:
                        data['descricao'] = descricao[:200]  # Limitar tamanho
                        break
        
        return data
    
    def extract_nota_fiscal_data(self, image_bytes: bytes) -> Dict[str, Optional[str]]:
        """
        Extrai dados específicos de uma nota fiscal
        Retorna um dicionário com os campos extraídos
        """
        text = self.extract_text(image_bytes)
        
        data = {
            'codigo': None,
            'recebimento': None,
            'valor': None,
            'descricao': None,
            'tipo': None,
            'texto_completo': text
        }
        
        # Extrair número da nota fiscal
        nf_patterns = [
            r'N[Fº°]?\s*[:\s]*(\d{3,9})',
            r'NOTA\s*FISCAL[:\s]*N[Fº°]?\s*[:\s]*(\d{3,9})',
            r'N[Fº°]?\s*(\d{3,9})',
        ]
        
        for pattern in nf_patterns:
            nf_match = re.search(pattern, text, re.IGNORECASE)
            if nf_match:
                data['codigo'] = f"NF-{nf_match.group(1)}"
                break
        
        # Extrair valor
        valor_patterns = [
            r'VALOR\s*TOTAL[:\s]*R?\$?\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
            r'TOTAL[:\s]*R?\$?\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
            r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
        ]
        
        for pattern in valor_patterns:
            valor_match = re.search(pattern, text, re.IGNORECASE)
            if valor_match:
                valor_str = valor_match.group(1).replace('.', '').replace(',', '.')
                try:
                    data['valor'] = valor_str
                except:
                    pass
                break
        
        # Extrair data de emissão/recebimento
        data_patterns = [
            r'DATA\s*DE\s*EMISSÃO[:\s]*(\d{1,2}/\d{1,2}/\d{2,4})',
            r'DATA[:\s]*(\d{1,2}/\d{1,2}/\d{2,4})',
            r'(\d{1,2}/\d{1,2}/\d{2,4})',
        ]
        
        for pattern in data_patterns:
            data_match = re.search(pattern, text, re.IGNORECASE)
            if data_match:
                data_str = data_match.group(1)
                try:
                    if len(data_str.split('/')[-1]) == 2:
                        day, month, year = data_str.split('/')
                        year = '20' + year if int(year) < 50 else '19' + year
                    else:
                        day, month, year = data_str.split('/')
                    
                    datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                    data['recebimento'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                except:
                    pass
                break
        
        # Extrair tipo (Entrada/Saída)
        if re.search(r'ENTRADA', text, re.IGNORECASE):
            data['tipo'] = 'Entrada'
        elif re.search(r'SA[ÍI]DA', text, re.IGNORECASE):
            data['tipo'] = 'Saída'
        
        # Extrair descrição (produtos ou serviços)
        descricao_keywords = ['PRODUTO', 'SERVIÇO', 'DESCRIÇÃO', 'ITEM']
        lines = text.split('\n')
        for line in lines:
            for keyword in descricao_keywords:
                if keyword in line.upper():
                    descricao = line.split(':', 1)[-1].strip() if ':' in line else line.strip()
                    if descricao and len(descricao) > 5:
                        data['descricao'] = descricao[:200]
                        break
        
        return data

