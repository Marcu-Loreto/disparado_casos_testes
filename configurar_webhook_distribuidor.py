#!/usr/bin/env python3
"""
Configura webhook na Evolution API para usar o distribuidor
"""

import requests
import json
import sys
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

env = load_env()

# Configurações
EVOLUTION_URL = env.get('EVOLUTION_API_URL', 'https://evolution.etechats.com.br')
API_KEY = env.get('EVOLUTION_API_KEY', '')
INSTANCE = env.get('EVOLUTION_INSTANCE', 'TESTE_AUTO_MGI')

print("=" * 70)
print("🔀 CONFIGURAÇÃO DO WEBHOOK DISTRIBUIDOR")
print("=" * 70)
print()
print("⚠️  ATENÇÃO: Isso vai alterar o webhook atual!")
print()
print("📋 Configuração atual:")
print(f"   Evolution API: {EVOLUTION_URL}")
print(f"   Instância: {INSTANCE}")
print()

# Opções de URL do distribuidor
print("📍 Onde o distribuidor está rodando?")
print()
print("1. Mesma VPS da Evolution (webhook.etechats.com.br)")
print("2. Localhost com ngrok (para testes)")
print("3. Outro servidor/IP")
print()

opcao = input("Escolha (1/2/3): ").strip()

if opcao == "1":
    # Mesma VPS
    distributor_url = "https://webhook.etechats.com.br:9000/webhook/distributor"
    print()
    print("✅ Usando VPS: https://webhook.etechats.com.br:9000")
    print()
    print("⚠️  Certifique-se de que:")
    print("   1. O distribuidor está rodando: python3 webhook_distributor.py")
    print("   2. A porta 9000 está aberta no firewall")
    print("   3. O servidor Python está rodando na porta 8000")

elif opcao == "2":
    # Ngrok
    print()
    print("💡 Inicie o ngrok em outro terminal:")
    print("   ngrok http 9000")
    print()
    ngrok_url = input("Cole a URL do ngrok (ex: https://abc123.ngrok.io): ").strip()
    
    if not ngrok_url:
        print("❌ URL não pode estar vazia!")
        sys.exit(1)
    
    distributor_url = f"{ngrok_url.rstrip('/')}/webhook/distributor"

elif opcao == "3":
    # Outro servidor
    print()
    servidor = input("Digite a URL do servidor (ex: https://meu-servidor.com): ").strip()
    
    if not servidor:
        print("❌ URL não pode estar vazia!")
        sys.exit(1)
    
    distributor_url = f"{servidor.rstrip(':')}:9000/webhook/distributor"

else:
    print("❌ Opção inválida!")
    sys.exit(1)

print()
print("=" * 70)
print("📋 RESUMO DA CONFIGURAÇÃO")
print("=" * 70)
print()
print(f"🌐 Webhook Distribuidor: {distributor_url}")
print()
print("📤 O distribuidor vai enviar para:")
print("   1. N8N: https://webhook.etechats.com.br/webhook/TESTE01")
print("   2. Python: http://localhost:8000/webhook/evolution/messages")
print()
print("⚠️  IMPORTANTE:")
print("   - O webhook atual do N8N será substituído")
print("   - Mas o N8N continuará recebendo via distribuidor")
print("   - Certifique-se de que o distribuidor está rodando!")
print()

confirma = input("Confirma configuração? (s/n): ").strip().lower()

if confirma != 's':
    print("❌ Configuração cancelada")
    sys.exit(0)

print()
print("🔄 Configurando webhook na Evolution API...")

# Payload
payload = {
    "url": distributor_url,
    "webhook_by_events": True,
    "events": ["messages.upsert"]
}

headers = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

try:
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
        print("📋 Resposta da Evolution API:")
        try:
            result = response.json()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except:
            print(response.text)
        
        print()
        print("🎯 Próximos passos:")
        print()
        print("1. Certifique-se de que o distribuidor está rodando:")
        print("   python3 webhook_distributor.py")
        print()
        print("2. Certifique-se de que o Python está rodando:")
        print("   python3 START.py")
        print()
        print("3. Teste enviando uma mensagem pelo WhatsApp")
        print()
        print("4. Verifique os logs do distribuidor:")
        print("   Deve mostrar: ✅ N8N: OK e ✅ Python Local: OK")
        print()
        print("🔍 Para verificar o webhook configurado:")
        print(f"   curl -H 'apikey: {API_KEY[:20]}...' \\")
        print(f"     {EVOLUTION_URL}/webhook/find/{INSTANCE}")
        
    else:
        print("❌ ERRO AO CONFIGURAR WEBHOOK")
        print("=" * 70)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        print()
        print("💡 Possíveis causas:")
        print("   - API Key inválida")
        print("   - Instância não existe")
        print("   - URL do distribuidor incorreta")
        print()
        print("🔧 Verifique:")
        print(f"   EVOLUTION_API_URL={EVOLUTION_URL}")
        print(f"   EVOLUTION_API_KEY={API_KEY[:20]}...")
        print(f"   EVOLUTION_INSTANCE={INSTANCE}")
    
    print("=" * 70)
    
except requests.exceptions.ConnectionError:
    print("❌ Erro de conexão com Evolution API")
    print(f"   Verifique se {EVOLUTION_URL} está acessível")
except requests.exceptions.Timeout:
    print("❌ Timeout ao conectar com Evolution API")
except Exception as e:
    print(f"❌ Erro: {e}")

print()
