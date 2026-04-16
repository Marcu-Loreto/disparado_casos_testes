#!/usr/bin/env python3
"""
Script para configurar webhook na Evolution API
Lê configurações do arquivo .env
"""

import requests
import json
import sys
import os
from pathlib import Path

# Carrega configurações do .env
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

# Carrega variáveis
env = load_env()

# Configurações da Evolution API (do .env)
EVOLUTION_URL = env.get('EVOLUTION_API_URL', 'https://evolution.etechats.com.br')
API_KEY = env.get('EVOLUTION_API_KEY', '')
INSTANCE = env.get('EVOLUTION_INSTANCE', 'TESTE_AUTO_MGI')

# URL do webhook de recepção (do .env)
WEBHOOK_URL = env.get('WEBHOOK_RECEPTION_URL', 'https://webhook.etechats.com.br/webhook/TESTE01')

print("=" * 70)
print("🔧 CONFIGURAÇÃO DE WEBHOOK - EVOLUTION API")
print("=" * 70)
print()
print("📋 Configurações carregadas do .env:")
print(f"   Evolution API: {EVOLUTION_URL}")
print(f"   Instância: {INSTANCE}")
print(f"   Webhook URL: {WEBHOOK_URL}")
print()
print("💡 Este webhook receberá as respostas do WhatsApp")
print("   As mensagens serão processadas e salvas em sessions/*.csv")
print()

confirma = input("Confirma configuração? (s/n): ").strip().lower()

if confirma != 's':
    print("❌ Configuração cancelada")
    sys.exit(0)

print()
print("🔄 Configurando webhook na Evolution API...")

# Payload para configurar webhook
payload = {
    "url": WEBHOOK_URL,
    "webhook_by_events": True,
    "events": ["messages.upsert"]
}

headers = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

try:
    # Configura webhook
    response = requests.post(
        f"{EVOLUTION_URL}/webhook/set/{INSTANCE}",
        json=payload,
        headers=headers,
        timeout=30
    )
    
    print()
    print("=" * 70)
    
    if response.status_code in [200, 201]:
        print("✅ WEBHOOK CONFIGURADO COM SUCESSO!")
        print("=" * 70)
        print()
        print("📋 Detalhes da configuração:")
        try:
            result = response.json()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except:
            print(response.text)
        
        print()
        print("🎯 Próximos passos:")
        print()
        print("1. Inicie o sistema:")
        print("   python3 START.py")
        print()
        print("2. Acesse a interface:")
        print("   http://localhost:8080/whatsapp_final.html")
        print()
        print("3. Envie mensagens pela aba 'Enviar'")
        print()
        print("4. Responda pelo WhatsApp")
        print()
        print("5. Veja as respostas na aba 'Recepção'")
        print()
        print("📁 Respostas serão salvas em:")
        print(f"   sessions/respostas_NUMERO_TIMESTAMP.csv")
        print()
        print("🔍 Para verificar se o webhook está recebendo:")
        print(f"   Monitore os logs do servidor em {WEBHOOK_URL}")
        
    else:
        print("❌ ERRO AO CONFIGURAR WEBHOOK")
        print("=" * 70)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        print()
        print("💡 Possíveis causas:")
        print("   - API Key inválida")
        print("   - Instância não existe ou não está conectada")
        print("   - URL do webhook incorreta")
        print()
        print("🔧 Verifique as configurações no arquivo .env:")
        print(f"   EVOLUTION_API_URL={EVOLUTION_URL}")
        print(f"   EVOLUTION_API_KEY={API_KEY[:20]}...")
        print(f"   EVOLUTION_INSTANCE={INSTANCE}")
        print(f"   WEBHOOK_RECEPTION_URL={WEBHOOK_URL}")
    
    print("=" * 70)
    
except requests.exceptions.ConnectionError:
    print("❌ Erro de conexão com Evolution API")
    print(f"   Verifique se {EVOLUTION_URL} está acessível")
    print()
    print("   Teste manualmente:")
    print(f"   curl {EVOLUTION_URL}/instance/fetchInstances")
    
except requests.exceptions.Timeout:
    print("❌ Timeout ao conectar com Evolution API")
    print("   A API pode estar lenta ou indisponível")
    
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    print()
    print("   Verifique:")
    print("   1. Arquivo .env existe e está configurado")
    print("   2. Biblioteca 'requests' está instalada: pip install requests")

print()
