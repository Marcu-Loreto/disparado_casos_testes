#!/usr/bin/env python3
"""
Script de teste para o webhook distribuidor
"""

import json
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

print("=" * 70)
print("🧪 TESTE DO WEBHOOK DISTRIBUIDOR")
print("=" * 70)
print()

# Payload de teste (simula mensagem da Evolution API)
test_payload = {
    "event": "messages.upsert",
    "instance": "TESTE_AUTO_MGI",
    "data": {
        "key": {
            "remoteJid": "5519993388617@s.whatsapp.net",
            "fromMe": False,
            "id": "TEST123"
        },
        "message": {
            "conversation": "Mensagem de teste do distribuidor"
        },
        "messageTimestamp": int(time.time())
    }
}

print("📋 Payload de teste:")
print(json.dumps(test_payload, indent=2, ensure_ascii=False))
print()

# Testa o distribuidor
print("🔄 Enviando para o distribuidor...")
print()

try:
    data = json.dumps(test_payload).encode('utf-8')
    req = Request(
        "http://localhost:9000/webhook/distributor",
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode('utf-8'))
        
        print("=" * 70)
        print("✅ DISTRIBUIDOR RESPONDEU")
        print("=" * 70)
        print()
        print("📋 Resposta:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()
        
        if result.get("status") == "success":
            print("🎉 Teste bem-sucedido!")
            print()
            print(f"📤 Webhook distribuído para {result.get('destinations', 0)} destinos")
            print()
            print("💡 Verifique os logs do distribuidor para ver:")
            print("   ✅ N8N: OK")
            print("   ✅ Python Local: OK")
        else:
            print("⚠️  Distribuidor respondeu mas com status diferente de success")
        
        print()
        print("=" * 70)

except HTTPError as e:
    print(f"❌ Erro HTTP {e.code}: {e.reason}")
    print()
    print("💡 Possíveis causas:")
    print("   - Distribuidor não está rodando")
    print("   - Porta 9000 ocupada por outro processo")
    print()
    print("🔧 Solução:")
    print("   python3 webhook_distributor.py")

except URLError as e:
    print(f"❌ Erro de conexão: {e.reason}")
    print()
    print("💡 O distribuidor não está rodando!")
    print()
    print("🔧 Inicie o distribuidor:")
    print("   python3 webhook_distributor.py")

except Exception as e:
    print(f"❌ Erro inesperado: {e}")

print()
print("=" * 70)
print("🔍 VERIFICAÇÕES ADICIONAIS")
print("=" * 70)
print()

# Testa health check
print("1️⃣  Testando health check do distribuidor...")
try:
    req = Request("http://localhost:9000/health")
    with urlopen(req, timeout=5) as response:
        health = json.loads(response.read().decode('utf-8'))
        print("   ✅ Distribuidor está saudável")
        print(f"   📤 Destinos configurados: {len(health.get('destinations', []))}")
except:
    print("   ❌ Health check falhou")

print()

# Testa servidor Python
print("2️⃣  Testando servidor Python...")
try:
    req = Request("http://localhost:8000/health")
    with urlopen(req, timeout=5) as response:
        health = json.loads(response.read().decode('utf-8'))
        print("   ✅ Servidor Python está rodando")
except:
    print("   ❌ Servidor Python não está rodando")
    print("   🔧 Inicie: python3 START.py")

print()
print("=" * 70)
