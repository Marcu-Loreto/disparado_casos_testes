#!/usr/bin/env python3
"""
Script para inicializar o sistema completo de WhatsApp Message Dispatcher.
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Exibe o banner do sistema."""
    print("=" * 60)
    print("📱 WHATSAPP MESSAGE DISPATCHER")
    print("=" * 60)
    print("🚀 Sistema de Envio Automatizado de Mensagens")
    print("✅ Múltiplos formatos: Texto, JSON, CSV, XLSX")
    print("⚡ Interface web moderna e intuitiva")
    print("=" * 60)

def check_system():
    """Verifica se o sistema está pronto."""
    print("\n🔍 Verificando sistema...")
    
    # Verifica arquivos essenciais
    required_files = [
        "app/simple_webhook_server.py",
        "whatsapp_sender_page.html",
        "config/settings.py",
        ".env"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Arquivos faltando:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Todos os arquivos necessários encontrados")
    return True

def start_webhook_server():
    """Inicia o servidor webhook."""
    print("\n🚀 Iniciando servidor webhook...")
    
    try:
        # Inicia o servidor webhook em background
        webhook_process = subprocess.Popen([
            sys.executable, "-m", "app.simple_webhook_server"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aguarda um pouco para o servidor inicializar
        time.sleep(3)
        
        # Verifica se o processo ainda está rodando
        if webhook_process.poll() is None:
            print("✅ Servidor webhook iniciado com sucesso!")
            print("📡 API disponível em: http://localhost:8000")
            return webhook_process
        else:
            print("❌ Falha ao iniciar servidor webhook")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor webhook: {e}")
        return None

def start_web_server():
    """Inicia o servidor web para a interface."""
    print("\n🌐 Iniciando servidor web...")
    
    try:
        # Inicia servidor HTTP para servir a página
        web_process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8080"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(2)
        
        if web_process.poll() is None:
            print("✅ Servidor web iniciado com sucesso!")
            print("🌍 Interface disponível em: http://localhost:8080/whatsapp_sender_page.html")
            return web_process
        else:
            print("❌ Falha ao iniciar servidor web")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor web: {e}")
        return None

def open_browser():
    """Abre o navegador com a interface."""
    try:
        url = "http://localhost:8080/whatsapp_sender_page.html"
        print(f"\n🌐 Abrindo navegador: {url}")
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"❌ Erro ao abrir navegador: {e}")
        return False

def show_instructions():
    """Mostra instruções de uso."""
    print("\n" + "=" * 60)
    print("📋 INSTRUÇÕES DE USO")
    print("=" * 60)
    print("1. 🌐 Acesse: http://localhost:8080/whatsapp_sender_page.html")
    print("2. 📱 Informe o número do WhatsApp (já preenchido para teste)")
    print("3. 📝 Escolha o método de envio:")
    print("   • Colar Lista: Cole mensagens uma por linha")
    print("   • JSON Avançado: Controle individual de delays")
    print("   • Upload Arquivo: CSV ou XLSX")
    print("4. 🚀 Clique em 'Enviar Mensagens'")
    print("5. ✅ Acompanhe o progresso e resultados")
    print("\n📞 Número de teste configurado: +556132073332")
    print("🔧 Para alterar, edite o arquivo .env")
    print("=" * 60)

def main():
    """Função principal."""
    print_banner()
    
    # Verifica sistema
    if not check_system():
        print("\n❌ Sistema não está completo. Execute a instalação primeiro.")
        return
    
    # Inicia servidores
    webhook_process = start_webhook_server()
    if not webhook_process:
        print("\n❌ Não foi possível iniciar o sistema.")
        return
    
    web_process = start_web_server()
    if not web_process:
        print("\n❌ Não foi possível iniciar a interface web.")
        webhook_process.terminate()
        return
    
    # Abre navegador
    time.sleep(1)
    open_browser()
    
    # Mostra instruções
    show_instructions()
    
    print("\n🎯 SISTEMA PRONTO PARA USO!")
    print("\n⚠️  Para parar o sistema, pressione Ctrl+C")
    
    try:
        # Mantém os processos rodando
        while True:
            time.sleep(1)
            
            # Verifica se os processos ainda estão rodando
            if webhook_process.poll() is not None:
                print("\n❌ Servidor webhook parou inesperadamente")
                break
                
            if web_process.poll() is not None:
                print("\n❌ Servidor web parou inesperadamente")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Parando sistema...")
        
        # Para os processos
        if webhook_process and webhook_process.poll() is None:
            webhook_process.terminate()
            print("✅ Servidor webhook parado")
            
        if web_process and web_process.poll() is None:
            web_process.terminate()
            print("✅ Servidor web parado")
        
        print("👋 Sistema encerrado com sucesso!")

if __name__ == "__main__":
    main()