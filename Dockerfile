# Use uma imagem base do Python
FROM python:3.8

# Defina o diretório de trabalho como /app
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do aplicativo para o contêiner
COPY . .

# Exponha a porta 5000 para o mundo exterior
EXPOSE 5000

# Comando para executar o aplicativo quando o contêiner for iniciado
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]