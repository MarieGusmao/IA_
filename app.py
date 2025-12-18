import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Bot Ativo", layout="centered")

st.title("🤖 Bot Telegram")
st.success("O serviço está ativo no Render.")

# Inicia o bot UMA ÚNICA VEZ
if "bot_iniciado" not in st.session_state:
    st.session_state.bot_iniciado = True
    subprocess.Popen(["python", "bot.py"])

st.markdown("""
Este Web Service existe apenas para manter o bot online.
Use o Telegram para conversar com o bot.
""")