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
url = "http://localhost:8080/whatsapp_final.html"
print(f"🌍 Abrindo navegador: {url}")
webbrowser.open(url)

print("\n" + "=" * 50)
print("✅ SISTEMA COMPLETO FUNCIONAL!")
print("=" * 50)
print("📱 Interface: http://localhost:8080/whatsapp_final.html")
print("📡 API WhatsApp: http://localhost:8000")
print("\n🎯 FUNCIONALIDADES COMPLETAS:")
print("1. 📤 Enviar mensagens automatizadas")
print("2. 📥 Receber respostas em tempo real")
print("3. 📊 Contador incremental (X/Total)")
print("4. 💬 Última resposta destacada")
print("5. ✅ Detecção automática de task completa")
print("6. 📄 CSV único por sessão com timestamp")
print("7. 📁 Histórico completo de sessões")
print("8. 💾 Download de CSVs anteriores")
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