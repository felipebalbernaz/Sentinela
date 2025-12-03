import pytesseract
from PIL import Image

class OcrService:
    def ler_texto_da_imagem(self, image_stream):
        # Abre a imagem usando PIL
        imagem = Image.open(image_stream)
        
        # Extrai o texto
        texto = pytesseract.image_to_string(imagem, lang='por') # 'por' para português
        
        return texto
