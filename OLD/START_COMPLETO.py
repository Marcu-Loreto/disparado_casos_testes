#!/usr/bin/env python3
"""
Inicia o sistema completo: Distribuidor + Servidor Python + Interface Web
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

processes = []

# Carrega porta do .env
def load_env():
    """Carrega variáveis do arquivo .env"""
    env_path = Path(__file__).parent / '.env'
    env_vars = {}
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars

env = load_env()
WEBHOOK_PORT = env.get('WEBHOOK_PORT', '8004')

def signal_handler(sig, frame):
    """Handler para Ctrl+C - para todos os processos."""
    print("\n\n🛑 Parando todos os serviços...")
    for p in processes:
        try:
            p.terminate()
        except:
            pass
    print("✅ Todos os serviços foram parados")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("=" * 70)
print("🚀 INICIANDO SISTEMA COMPLETO")
print("=" * 70)
print()

# 1. Inicia o Distribuidor
print("1️⃣  Iniciando Webhook Distribuidor (porta 9000)...")
try:
    p1 = subprocess.Popen(
        [sys.executable, "webhook_distributor.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    processes.append(p1)
    time.sleep(2)
    
    if p1.poll() is None:
        print("   ✅ Distribuidor iniciado")
    else:
        print("   ❌ Erro ao iniciar distribuidor")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Erro: {e}")
    sys.exit(1)

print()

# 2. Inicia o Servidor Python
print(f"2️⃣  Iniciando Servidor Python (porta {WEBHOOK_PORT})...")
try:
    p2 = subprocess.Popen(
        [sys.executable, "start_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    processes.append(p2)
    time.sleep(2)
    
    if p2.poll() is None:
        print("   ✅ Servidor Python iniciado")
    else:
        print("   ❌ Erro ao iniciar servidor Python")
        for p in processes:
            p.terminate()
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Erro: {e}")
    for p in processes:
        p.terminate()
    sys.exit(1)

print()

# 3. Inicia o Servidor Web
print("3️⃣  Iniciando Interface Web (porta 8084)...")
try:
    p3 = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8084"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    processes.append(p3)
    time.sleep(1)
    
    if p3.poll() is None:
        print("   ✅ Interface Web iniciada")
    else:
        print("   ❌ Erro ao iniciar interface web")
        for p in processes:
            p.terminate()
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Erro: {e}")
    for p in processes:
        p.terminate()
    sys.exit(1)

print()
print("=" * 70)
print("✅ SISTEMA COMPLETO INICIADO")
print("=" * 70)
print()
print("📊 Serviços rodando:")
print()
print("   🔀 Webhook Distribuidor:")
print("      http://localhost:9000/webhook/distributor")
print("      Health: http://localhost:9000/health")
print()
print("   🐍 Servidor Python:")
print(f"      http://localhost:{WEBHOOK_PORT}")
print(f"      Envio: http://localhost:{WEBHOOK_PORT}/webhook/tela2")
print(f"      Recepção: http://localhost:{WEBHOOK_PORT}/webhook/evolution/messages")
print()
print("   🌐 Interface Web:")
print("      http://localhost:8084/whatsapp_final.html")
print()
print("=" * 70)
print()
print("💡 Próximos passos:")
print()
print("1. Configure o webhook na Evolution API:")
print("   python3 configurar_webhook_distribuidor.py")
print()
print("2. Acesse a interface:")
print("   http://localhost:8080/whatsapp_final.html")
print()
print("3. Envie mensagens e veja as respostas em tempo real!")
print()
print("=" * 70)
print()
print("🔍 Logs em tempo real:")
print("   - Distribuidor: Mostra webhooks recebidos e distribuídos")
print("   - Python: Mostra mensagens processadas e salvas")
print()
print("🛑 Para parar: Pressione Ctrl+C")
print()
print("=" * 70)
print()

# Mantém rodando e mostra logs
try:
    while True:
        # Verifica se algum processo morreu
        for i, p in enumerate(processes):
            if p.poll() is not None:
                print(f"\n❌ Processo {i+1} parou inesperadamente!")
                for proc in processes:
                    proc.terminate()
                sys.exit(1)
        
        time.sleep(1)
        
except KeyboardInterrupt:
    signal_handler(None, None)
