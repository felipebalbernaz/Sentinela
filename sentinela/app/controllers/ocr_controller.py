from flask import request, render_template, flash
from app.services.ocr_service import OcrService # Importe novo serviço

# Instancia o serviço
ocr_service = OcrService()

def upload_nota():
    if request.method == 'POST':
        # Verifica se o arquivo existe na requisição
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado')
            return render_template('seu_template.html')
            
        file = request.files['file']
        
        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return render_template('seu_template.html')

        if file:
            # Chama o serviço passando o arquivo
            texto_extraido = ocr_service.ler_texto_da_imagem(file)
            
            # AQUI VOCÊ FAZ O QUE QUISER COM O TEXTO
            # Ex: Salvar no banco ou mostrar na tela
            print(texto_extraido) 
            
            return render_template('resultado.html', texto=texto_extraido)
