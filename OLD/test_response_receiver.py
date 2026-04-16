#!/usr/bin/env python3
"""
Teste do sistema de recebimento de respostas
"""

import json
import requests
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:8000"

print("🧪 TESTE DO SISTEMA DE RECEBIMENTO DE RESPOSTAS")
print("=" * 60)
print()

# 1. Verificar se servidor está rodando
print("1️⃣  Verificando servidor...")
try:
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Servidor está rodando")
    else:
        print("❌ Servidor não está respondendo corretamente")
        exit(1)
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    print("💡 Certifique-se de que o servidor está rodando: python3 START.py")
    exit(1)

print()

# 2. Registrar número (simular envio de mensagens)
print("2️⃣  Registrando número de teste...")
test_phone = "+556132073332"

payload = {
    "phone_number": test_phone,
    "text_list": "Mensagem de teste 1\nMensagem de teste 2"
}

try:
    response = requests.post(
        f"{BASE_URL}/webhook/tela2",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Número registrado: {test_phone}")
        print(f"   Mensagens enviadas: {result.get('sent_messages', 0)}")
    else:
        print(f"❌ Erro ao registrar: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# 3. Verificar números ativos
print("3️⃣  Verificando números ativos...")
try:
    response = requests.get(f"{BASE_URL}/active-numbers")
    if response.status_code == 200:
        result = response.json()
        active_count = result.get('count', 0)
        print(f"✅ Números ativos: {active_count}")
        
        if active_count > 0:
            for phone, data in result.get('active_numbers', {}).items():
                print(f"   📱 {data['phone_number']}")
                print(f"      Registrado em: {data['registered_at']}")
                print(f"      Respostas: {data['responses_count']}")
    else:
        print(f"❌ Erro ao verificar: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# 4. Simular recebimento de mensagem
print("4️⃣  Simulando recebimento de mensagem...")

# Simula webhook da Evolution API
webhook_payload = {
    "event": "messages.upsert",
    "instance": "TESTE_AUTO_MGI",
    "data": {
        "key": {
            "remoteJid": "556132073332@s.whatsapp.net",
            "fromMe": False,
            "id": "TEST123ABC"
        },
        "message": {
            "conversation": "Esta é uma resposta de teste!"
        },
        "messageTimestamp": int(datetime.now().timestamp())
    }
}

try:
    response = requests.post(
        f"{BASE_URL}/webhook/evolution/messages",
        json=webhook_payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        status = result.get('status')
        
        if status == 'success':
            print("✅ Mensagem processada e salva!")
            data = result.get('data', {})
            print(f"   De: {data.get('phone_number')}")
            print(f"   Mensagem: {data.get('message')}")
            print(f"   Timestamp: {data.get('timestamp')}")
        elif status == 'ignored':
            print("⚠️  Mensagem ignorada (não é de número ativo)")
        else:
            print(f"❓ Status desconhecido: {status}")
    else:
        print(f"❌ Erro ao processar: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# 5. Simular mensagem de número NÃO ativo
print("5️⃣  Testando filtro (número não ativo)...")

webhook_payload_other = {
    "event": "messages.upsert",
    "instance": "TESTE_AUTO_MGI",
    "data": {
        "key": {
            "remoteJid": "5511999999999@s.whatsapp.net",  # Número diferente
            "fromMe": False,
            "id": "TEST456DEF"
        },
        "message": {
            "conversation": "Mensagem de número não registrado"
        },
        "messageTimestamp": int(datetime.now().timestamp())
    }
}

try:
    response = requests.post(
        f"{BASE_URL}/webhook/evolution/messages",
        json=webhook_payload_other,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        status = result.get('status')
        
        if status == 'ignored':
            print("✅ Mensagem corretamente ignorada!")
            print("   (Número não está na lista ativa)")
        elif status == 'success':
            print("❌ ERRO: Mensagem foi processada mas deveria ser ignorada!")
        else:
            print(f"❓ Status desconhecido: {status}")
    else:
        print(f"❌ Erro ao processar: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# 6. Verificar contador de respostas
print("6️⃣  Verificando contador de respostas...")
try:
    response = requests.get(f"{BASE_URL}/active-numbers")
    if response.status_code == 200:
        result = response.json()
        
        for phone, data in result.get('active_numbers', {}).items():
            if data['phone_number'] == test_phone:
                responses = data['responses_count']
                print(f"✅ Contador atualizado: {responses} resposta(s)")
                break
    else:
        print(f"❌ Erro ao verificar: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")

print()
print("=" * 60)
print("🎉 TESTE CONCLUÍDO!")
print()
print("📋 Próximos passos:")
print("1. Configure o webhook na Evolution API")
print("2. Envie mensagens reais via interface")
print("3. Responda pelo WhatsApp")
print("4. Verifique os logs do servidor")
print()
print("📚 Documentação: CONFIGURAR_WEBHOOK_EVOLUTION.md")
