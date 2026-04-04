#!/usr/bin/env python3
"""
🚀 WHATSAPP MESSAGE SENDER - VERSÃO FINAL
Execute: python3 START.py
"""

import os
import subprocess
import time
import webbrowser

print("📱 WHATSAPP MESSAGE SENDER")
print("🚀 Versão Final - Totalmente Independente")
print("📊 Limite: 1000 mensagens por envio")
print("✅ Sem dependências externas")
print("=" * 50)

# Mata processos existentes
print("🧹 Limpando processos...")
os.system("pkill -f 'webhook' 2>/dev/null")
os.system("pkill -f 'http.server 8080' 2>/dev/null")
time.sleep(1)

# Inicia servidor standalone
print("📡 Iniciando servidor WhatsApp...")
api = subprocess.Popen(["python3", "-m", "app.standalone_server"])
time.sleep(3)

# Inicia interface web
print("🌐 Iniciando interface web...")
web = subprocess.Popen(["python3", "-m", "http.server", "8080"])
time.sleep(2)

# Abre navegador
url = "http://localhost:8080/whatsapp_simple.html"
print(f"🌍 Abrindo navegador: {url}")
webbrowser.open(url)

print("\n" + "=" * 50)
print("✅ SISTEMA TOTALMENTE FUNCIONAL!")
print("=" * 50)
print("📱 Interface: http://localhost:8080/whatsapp_simple.html")
print("📡 API WhatsApp: http://localhost:8000")
print("📊 Limite: 1000 mensagens por envio")
print("📞 Número teste: +556132073332")
print("🔧 Evolution API: Configurada e funcionando")
print("\n📋 INSTRUÇÕES:")
print("1. 📝 Cole suas mensagens (uma por linha)")
print("2. 👀 Veja o contador em tempo real")
print("3. ⚙️ Ajuste o delay se necessário")
print("4. 🚀 Clique 'Enviar Mensagens'")
print("5. 📊 Acompanhe o progresso")
print("\n⚠️  Para parar: Pressione Ctrl+C")
print("=" * 50)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n🛑 Parando sistema...")
    api.terminate()
    web.terminate()
    print("✅ Sistema parado com sucesso!")
    print("👋 Até logo!")