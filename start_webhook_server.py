#!/usr/bin/env python3
"""
Script para iniciar o servidor webhook do WhatsApp Message Dispatcher.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    try:
        import fastapi
        import uvicorn
        import pandas
        import httpx
        print("✅ Dependências verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("Execute: ./venv/bin/pip install -r requirements.txt")
        return False

def start_server():
    """Inicia o servidor webhook."""
    
    print("🚀 WhatsApp Message Dispatcher")
    print("=" * 50)
    
    # Verifica dependências
    if not check_dependencies():
        return
    
    # Verifica se o virtual environment existe
    venv_path = Path("venv/bin/python")
    if not venv_path.exists():
        print("❌ Virtual environment não encontrado")
        print("Execute: python3 -m venv venv && ./venv/bin/pip install -r requirements.txt")
        return
    
    print("\n📋 Configuração:")
    print("- Servidor: http://localhost:8000")
    print("- Webhook: http://localhost:8000/webhook/tela2")
    print("- Health: http://localhost:8000/health")
    print("- Docs: http://localhost:8000/docs")
    
    print("\n🌐 Endpoints disponíveis:")
    print("- POST /webhook/tela2 - Webhook principal (JSON/texto)")
    print("- POST /webhook/tela2/upload/csv - Upload CSV")
    print("- POST /webhook/tela2/upload/xlsx - Upload XLSX")
    
    print("\n📱 Formatos suportados:")
    print("- JSON estruturado com mensagens e delays")
    print("- Texto colado (uma mensagem por linha)")
    print("- Arquivo CSV com coluna 'text' ou 'message'")
    print("- Arquivo XLSX com coluna 'text' ou 'message'")
    print("- Formato legado N8N (compatibilidade)")
    
    # Pergunta se quer abrir a página de teste
    open_test = input("\n🔧 Abrir página de teste no navegador? (s/n): ").lower().strip()
    
    if open_test == 's':
        test_page_path = Path("webhook_test_page.html").absolute()
        if test_page_path.exists():
            webbrowser.open(f"file://{test_page_path}")
            print(f"📄 Página de teste aberta: {test_page_path}")
        else:
            print("❌ Página de teste não encontrada")
    
    print("\n🚀 Iniciando servidor...")
    print("Pressione Ctrl+C para parar")
    print("-" * 50)
    
    try:
        # Inicia o servidor usando o uvicorn
        cmd = [
            str(venv_path),
            "-m", "uvicorn",
            "app.webhook_server:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")

if __name__ == "__main__":
    start_server()