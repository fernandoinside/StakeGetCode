import time
import cv2
import pytesseract
import os
import re
import webbrowser  # Importar a biblioteca para abrir URLs
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import pyautogui

# Credenciais da API do Telegram
api_id = ''
api_hash = ''
phone = '+55'

# Inicia o cliente do Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Configuração do pytesseract (ajuste o caminho do Tesseract se necessário)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Caminho do tesseract no seu sistema

# Função para extrair o frame do vídeo e realizar OCR
def extrair_frame_e_extrair_texto(video_path, tempo_em_segundos=1):
    # Carregar o vídeo
    cap = cv2.VideoCapture(video_path)
    
    # Verificar se o vídeo foi carregado corretamente
    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}. Verifique o arquivo.")
        return
    
    # Obter o total de quadros no vídeo
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames por segundo
    print(f"Total de frames: {total_frames}, FPS: {fps}")
    
    # Calcular o quadro correspondente ao tempo desejado
    frame_atual = int(fps * tempo_em_segundos)
    print(f"Frame desejado para {tempo_em_segundos} segundos: {frame_atual}")
    
    # Ajustar para o caso em que o cálculo de quadro ultrapassa o total de quadros
    if frame_atual >= total_frames:
        print(f"Aviso: O quadro solicitado ({frame_atual}) está além do total de quadros ({total_frames}). Ajustando para o último quadro.")
        frame_atual = total_frames - 1  # Garantir que o quadro seja o último disponível
    
    # Tentar capturar o quadro desejado
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_atual)  # Pular para o quadro desejado
    ret, frame = cap.read()
    
    if ret:
        # Salvar o frame em um arquivo temporário
        imagem_temporaria = "frame_extraido.png"
        cv2.imwrite(imagem_temporaria, frame)
        print(f"Frame extraído e salvo em: {imagem_temporaria}")
        
        # Realizar OCR para extrair texto da imagem
        texto_extraido = pytesseract.image_to_string(frame)
        print(f"Texto extraído: {texto_extraido}")
        
        # Remover o arquivo temporário
        os.remove(imagem_temporaria)
        
        # Filtrar o texto abaixo de "CODE"
        match = re.search(r'CODE\s*(\S+)', texto_extraido)  # Captura o texto após "CODE"
        if match:
            codigo = match.group(1)
            print(f"Código extraído: {codigo}")
            
            # Gerar e abrir a URL
            url = f"https://stake.com/pt/settings/offers?currency=brl&type=drop&code={codigo}&modal=redeemBonus"
            print(f"URL gerada: {url}")
            webbrowser.open(url)  # Abre a URL no navegador
            # Mover o mouse para a posição (x=100, y=200)
            pyautogui.moveTo(1000, 780)
            # Clicar na posição atual do mouse
            time.sleep(10)
            pyautogui.click()
        else:
            print("Texto abaixo de 'CODE' não encontrado.")
    else:
        print(f"Erro ao extrair o frame. Verifique o arquivo do vídeo. Tentando outras opções...")

        # Tentar capturar o primeiro quadro
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Tentar capturar o primeiro quadro
        ret, frame = cap.read()
        if ret:
            imagem_temporaria = "frame_extraido_inicial.png"
            cv2.imwrite(imagem_temporaria, frame)
            print(f"Primeiro quadro extraído e salvo em: {imagem_temporaria}")
            
            # Realizar OCR para extrair texto da imagem
            texto_extraido = pytesseract.image_to_string(frame)
            print(f"Texto extraído do primeiro quadro: {texto_extraido}")
            
            # Remover o arquivo temporário
            os.remove(imagem_temporaria)
        else:
            print("Erro ao tentar capturar o primeiro quadro. Verifique o arquivo de vídeo.")

    # Liberar o objeto de captura
    cap.release()

# Função para salvar o texto em um arquivo
def salvar_texto(texto, numero_mensagem):
    caminho_arquivo = f"mensagem_{numero_mensagem}.txt"
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)
    print(f"Texto da mensagem {numero_mensagem} salvo em: {caminho_arquivo}")

async def obter_ultimas_mensagens(canal_id):
    print(f"Obtendo as últimas 5 mensagens do canal com ID {canal_id}...")
    mensagens = await client.get_messages(canal_id, limit=1)  # Pegando as últimas 5 mensagens
    if mensagens:
        for i, mensagem in enumerate(mensagens, 1):
            if isinstance(mensagem.media, MessageMediaDocument) and mensagem.media.document.mime_type == 'video/mp4':
                # Baixar o vídeo
                video_path = await mensagem.download_media()
                print(f"Vídeo salvo: {video_path}")
                
                # Extrair o frame e realizar OCR
                extrair_frame_e_extrair_texto(video_path, tempo_em_segundos=5)
                
            # Salvar o texto da mensagem
            texto = mensagem.text
            salvar_texto(texto, i)
            
            print(f"Mensagem {i}: {texto}")
            match = re.search(r'- Code: (\w+)', texto)
            if match:
                codigo = match.group(1)
                print(f"Código encontrado (Mensagem {i}): {codigo}")
                url = f"https://stake.com/pt/settings/offers?currency=brl&type=drop&code={codigo}&modal=redeemBonus"
                print(f"URL (Mensagem {i}): {url}")
                webbrowser.open(url)  # Abre a URL no navegador
                # Mover o mouse para a posição (x=100, y=200)
                pyautogui.moveTo(1000, 780)
                # Clicar na posição atual do mouse
                time.sleep(10)
                pyautogui.click()
    else:
        print("Nenhuma mensagem encontrada no canal.")

@client.on(events.NewMessage(chats=[-0, -1, -2]))  # Passa uma lista de IDs de canais
async def monitorar_novas_mensagens(event):
    if isinstance(event.media, MessageMediaPhoto):
        # Salvar a imagem
        photo = await event.download_media()
        print(f"Imagem salva: {photo}")
    elif isinstance(event.media, MessageMediaDocument):
        if event.media.document.mime_type == 'video/mp4':
            # Salvar o vídeo
            video_path = await event.download_media()
            print(f"Vídeo salvo: {video_path}")
            
            # Extrair o frame e realizar OCR
            extrair_frame_e_extrair_texto(video_path, tempo_em_segundos=5)
    
    # Salvar o texto da mensagem
    texto = event.message.text
    salvar_texto(texto, "nova")

    print(f"Nova mensagem recebida: {texto}")
    match = re.search(r'- Code: (\w+)', texto)
    if match:
        codigo = match.group(1)
        print(f"Código encontrado: {codigo}")
        url = f"https://stake.com/pt/settings/offers?currency=brl&type=drop&code={codigo}&modal=redeemBonus"
        print(f"URL: {url}")
        webbrowser.open(url)  # Abre a URL no navegador
        # Mover o mouse para a posição (x=100, y=200)
        pyautogui.moveTo(1000, 780)
        # Clicar na posição atual do mouse
        time.sleep(10)
        pyautogui.click()


async def main():
    url = f"https://stake.com/pt/affiliate/funds?tab=rakeback&modal=vip"
    print(f"URL: {url}")
    webbrowser.open(url)  # Abre a URL no navegador
    # Mover o mouse para a posição (x=100, y=200)
    pyautogui.moveTo(1000, 620)
    # Clicar na posição atual do mouse
    time.sleep(10)
    pyautogui.click()
    time.sleep(10)
    
    await client.start(phone)  # Login automático se a sessão já existe
    
    # Defina os IDs dos canais a serem monitorados
    canal_ids = [-0, -1, -2]  # Lista com os IDs dos canais
    
    # Baixa as últimas mensagens de todos os canais
    for canal_id in canal_ids:
        await obter_ultimas_mensagens(canal_id)    

    print("Monitorando novas mensagens...")
    
    # Inicia o monitoramento de novas mensagens de todos os canais
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
