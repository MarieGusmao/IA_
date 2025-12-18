#chat com telegram

from dbm import sqlite3
import os
from langchain_groq import ChatGroq
from telegram import Update
from telegram.ext import Updater, ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

# Configuração do banco de dados SQLite
DB_NAME = "chatbot_logs.db" #Pasta de arquivo física
#conn de Conexão
conn = sqlite3.connect(DB_NAME) #Arquivo físico
cursor = conn.cursor() #Caneta

# Criar tabela para armazenar logs de conversas
cursor.execute('''CREATE TABLE IF NOT EXISTS chat_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pergunta TEXT,
                    resposta TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
conn.commit()

os.environ["GROQ_API_KEY"] = "GROQ_API_KEY"
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
#Criar o Modelo de IA Llama 3

chat = ChatGroq(
     model = "llama-3.1-8b-instant",
    temperature =0,
    )

#Função para Interagir com o ChatBot

def conversar_com_chatbot(pergunta:str) -> str:
    resposta = chat.invoke([
        ("system", "Você é um assistente."),
        ("user",  pergunta)
    ])
    return resposta.content

#Função para lidar com mensagens recebidas:

async def handle_message (update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """“Olá! Seja bem-vindo(a) 😊
    Sou Mariana Gusmão, corretora especialista em lançamentos imobiliários.
    Para te indicar opções alinhadas ao seu momento, me conte o que é essencial para você hoje como: localização, valor, tipo de imóvel e objetivos.""")
    
async def responder_mensagem (update: Update,
        Context: ContextTypes.DEFAULT_TYPE) -> None:
    pergunta = update.message.text
    resposta = conversar_com_chatbot (pergunta)
    await update.message.reply_text (resposta)

def main () -> None:
    #Criar a aplicação do bot
    application = ApplicationBuilder ().token(
        TELEGRAM_BOT_TOKEN).build()
    
    # Adicionar manipuladores de comando e mensagens

    application.add_handler (
        CommandHandler( "start", handle_message))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND,
        responder_mensagem))
    
    #Iniciar o bot
    application.run_polling()

if __name__ == "__main__":
    main()