#!/usr/bin/env python3
"""
🚀 COMANDO ÚNICO PARA INICIAR O SISTEMA WHATSAPP
Execute: python3 RUN.py
"""

import os
import subprocess
import time
import webbrowser

print("🚀 WHATSAPP MESSAGE DISPATCHER")
print("🔧 Iniciando sistema...")

# Mata processos existentes
os.system("pkill -f 'simple_webhook_server' 2>/dev/null")
os.system("pkill -f 'http.server 8080' 2>/dev/null")
time.sleep(1)

# Inicia API em background
print("📡 Iniciando API...")
api = subprocess.Popen(["python3", "-m", "app.simple_webhook_server"])
time.sleep(3)

# Inicia interface web em background  
print("🌐 Iniciando interface...")
web = subprocess.Popen(["python3", "-m", "http.server", "8080"])
time.sleep(2)

# Abre navegador
url = "http://localhost:8080/whatsapp_sender_page.html"
print(f"🌍 Abrindo: {url}")
webbrowser.open(url)

print("\n✅ SISTEMA FUNCIONANDO!")
print("📱 Acesse: http://localhost:8080/whatsapp_sender_page.html")
print("📞 Número teste: +556132073332")
print("⚠️  Ctrl+C para parar")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Parando...")
    api.terminate()
    web.terminate()
    print("✅ Parado!")