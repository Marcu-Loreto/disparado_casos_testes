#!/usr/bin/env python3
"""
Teste do sistema de sessões
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

print("🧪 TESTE DO SISTEMA DE SESSÕES")
print("=" * 60)

# 1. Enviar mensagens (cria sessão)
print("\n1️⃣  Enviando 3 mensagens de teste...")
payload = {
    "phone_number": "+5519993388617",
    "text_list": "Teste 1\nTeste 2\nTeste 3"
}

response = requests.post(f"{API_URL}/webhook/tela2", json=payload)
result = response.json()

print(f"✅ Status: {result['status']}")
print(f"📊 Mensagens enviadas: {result['sent_messages']}")
print(f"🆔 Session ID: {result['session_id']}")
print(f"📄 CSV: {result['csv_filename']}")

session_id = result['session_id']
phone = result['phone_number']

# 2. Verificar progresso da sessão
print("\n2️⃣  Verificando progresso da sessão...")
time.sleep(1)

response = requests.get(f"{API_URL}/session/{phone}")
progress = response.json()

print(f"✅ Sessão existe: {progress['exists']}")
print(f"📊 Progresso: {progress['responses_received']}/{progress['total_messages']}")
print(f"📈 Percentual: {progress['progress_percent']}%")
print(f"🎯 Status: {progress['status']}")

# 3. Simular recebimento de respostas
print("\n3️⃣  Simulando recebimento de 3 respostas...")

for i in range(1, 4):
    webhook_payload = {
        "event": "messages.upsert",
        "data": {
            "key": {
                "remoteJid": "5519993388617@s.whatsapp.net",
                "fromMe": False
            },
            "message": {
                "conversation": f"Resposta {i} de teste"
            }
        }
    }
    
    response = requests.post(f"{API_URL}/webhook/evolution/messages", json=webhook_payload)
    result = response.json()
    
    if result['status'] == 'success':
        progress = result['progress']
        print(f"  ✅ Resposta {i}: {progress['responses_received']}/{progress['total_messages']} ({progress['progress_percent']}%)")
        
        if progress['is_completed']:
            print(f"  🎉 SESSÃO COMPLETA!")
    
    time.sleep(0.5)

# 4. Listar todas as sessões
print("\n4️⃣  Listando todas as sessões...")
response = requests.get(f"{API_URL}/sessions")
data = response.json()

print(f"✅ Total de sessões: {data['count']}")
print(f"🔥 Sessões ativas: {data['active_count']}")

for session in data['sessions'][:3]:
    print(f"\n  📁 {session.get('session_id', 'N/A')}")
    print(f"     Número: {session.get('phone_number', 'N/A')}")
    print(f"     Respostas: {session.get('responses_received', 0)}")
    print(f"     Status: {session.get('status', 'N/A')}")
    print(f"     CSV: {session.get('csv_filename', 'N/A')}")

print("\n" + "=" * 60)
print("✅ TESTE CONCLUÍDO!")
print("=" * 60)
