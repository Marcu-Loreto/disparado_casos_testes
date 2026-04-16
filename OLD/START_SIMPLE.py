#!/usr/bin/env python3
"""
🚀 INICIAR WHATSAPP SENDER SIMPLES
Execute: python3 START_SIMPLE.py
"""

import os
import subprocess
import time
import webbrowser

print("📱 WHATSAPP MESSAGE SENDER")
print("🔧 Versão Simplificada - Até 1000 mensagens")
print("=" * 50)

# Mata processos existentes
print("🧹 Limpando processos...")
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

# Abre navegador com a interface simples
url = "http://localhost:8080/whatsapp_simple.html"
print(f"🌍 Abrindo: {url}")
webbrowser.open(url)

print("\n✅ SISTEMA FUNCIONANDO!")
print("📱 Interface: http://localhost:8080/whatsapp_simple.html")
print("📊 Limite: 1000 mensagens por envio")
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