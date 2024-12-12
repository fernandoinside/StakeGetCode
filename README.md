# StakeGetCode

Telegram Bot - Extração de Códigos e Automacao

Este projeto é um bot para o Telegram que monitora mensagens de canais específicos, realiza extração de texto a partir de imagens ou vídeos usando OCR (Optical Character Recognition) e automatiza a abertura de URLs com base em códigos extraídos.

Recursos

Monitoramento de mensagens em canais do Telegram.

Suporte a mensagens com vídeos e imagens.

Extração de texto de imagens e quadros de vídeos usando o Tesseract OCR.

Filtragem e extração de códigos de mensagens de texto.

Geração automática de URLs baseadas nos códigos extraídos.

Automatização de cliques e movimentação do mouse para interações adicionais.

Tecnologias Utilizadas

Python 3

Telethon - Biblioteca para interagir com a API do Telegram.

OpenCV - Processamento de vídeos e imagens.

Tesseract OCR - Extração de texto a partir de imagens.

PyAutoGUI - Automatação de movimentação e cliques do mouse.

Configuração

Requisitos

Python 3.7 ou superior

Instalar as dependências listadas no arquivo requirements.txt.

Tesseract OCR instalado no sistema (certifique-se de configurar o caminho corretamente no código).

Instalação

Clone este repositório:

$ git clone https://github.com/fernandoinside/StakeGetCode.git
$ cd StakeGetCode

Instale as dependências:

$ pip install -r requirements.txt

Configure as credenciais da API do Telegram no arquivo main.py:

api_id = 'SEU_API_ID'
api_hash = 'SEU_API_HASH'
phone = 'SEU_TELEFONE'

Certifique-se de que o Tesseract OCR esteja instalado e configure o caminho correto no código:

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

Execução

Para iniciar o bot, execute o seguinte comando:

$ python main.py

Funcionalidades Detalhadas

Monitoramento de Canais:

IDs de canais a serem monitorados podem ser configurados diretamente no código.

Monitora tanto mensagens de texto quanto mensagens com mídia (imagens e vídeos).

Extração de Texto:

Utiliza a biblioteca Tesseract OCR para reconhecer texto em imagens e quadros extraídos de vídeos.

Geração de URLs e Automatização de Cliques:

Gera URLs baseadas em códigos extraídos e realiza a automação de cliques usando PyAutoGUI para simular interações no navegador.

Estrutura do Projeto

main.py: Script principal do projeto.

requirements.txt: Lista de dependências do projeto.

Observações

Certifique-se de que você possui permissão para acessar os canais monitorados.

Ajuste as posições de clique do mouse de acordo com a resolução e configurações do seu sistema.

Contribuição

Contribuições são bem-vindas! Para contribuir, faça um fork deste repositório, crie uma branch com suas modificações e envie um pull request.

Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.