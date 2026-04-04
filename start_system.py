#!/usr/bin/env python3
"""
Comando simples para iniciar o sistema WhatsApp Message Dispatcher
"""

import os
import sys
import time
import subprocess
import webbrowser

def main():
    print("🚀 INICIANDO WHATSAPP MESSAGE DISPATCHER")
    print("=" * 50)
    
    # Para processos existentes nas portas
    print("🔧 Limpando portas...")
    os.system("pkill -f 'python3 -m app.simple_webhook_server' 2>/dev/null")
    os.system("pkill -f 'python3 -m http.server 8080' 2>/dev/null")
    time.sleep(2)
    
    # Inicia servidor webhook
    print("📡 Iniciando API webhook...")
    webhook_cmd = [sys.executable, "-m", "app.simple_webhook_server"]
    webhook_process = subprocess.Popen(webhook_cmd)
    time.sleep(3)
    
    # Inicia servidor web
    print("🌐 Iniciando servidor web...")
    web_cmd = [sys.executable, "-m", "http.server", "8080"]
    web_process = subprocess.Popen(web_cmd)
    time.sleep(2)
    
    # Abre navegador
    url = "http://localhost:8080/whatsapp_sender_page.html"
    print(f"🌍 Abrindo: {url}")
    webbrowser.open(url)
    
    print("\n✅ SISTEMA NO AR!")
    print("=" * 50)
    print("📱 Interface: http://localhost:8080/whatsapp_sender_page.html")
    print("📡 API: http://localhost:8000")
    print("📞 Número teste: +556132073332")
    print("=" * 50)
    print("⚠️  Pressione Ctrl+C para parar")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Parando sistema...")
        webhook_process.terminate()
        web_process.terminate()
        print("✅ Sistema parado!")

if __name__ == "__main__":
    main()