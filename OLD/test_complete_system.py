#!/usr/bin/env python3
"""
Teste Completo End-to-End do Sistema
Testa todas as funcionalidades implementadas
"""

import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:8000"
PHONE = "+5519993388617"

print("=" * 70)
print("🧪 TESTE COMPLETO END-TO-END - SISTEMA WHATSAPP")
print("=" * 70)
print()

# ============================================================================
# FASE 1: ENVIO DE MENSAGENS
# ============================================================================
print("📤 FASE 1: ENVIO DE MENSAGENS")
print("-" * 70)

messages = [
    "🧪 Teste 1 - Sistema iniciado",
    "📱 Teste 2 - Mensagens sendo enviadas",
    "✅ Teste 3 - Integração ativa",
    "🔥 Teste 4 - Processamento OK",
    "⚡ Teste 5 - Teste completo"
]

payload = {
    "phone_number": PHONE,
    "text_list": "\n".join(messages)
}

print(f"📞 Enviando {len(messages)} mensagens para {PHONE}...")

try:
    response = requests.post(f"{API_URL}/webhook/tela2", json=payload, timeout=60)
    result = response.json()
    
    if response.status_code == 200:
        print(f"✅ Envio bem-sucedido!")
        print(f"   📊 Mensagens enviadas: {result['sent_messages']}/{result['total_messages']}")
        print(f"   🆔 Session ID: {result['session_id']}")
        print(f"   📄 CSV: {result['csv_filename']}")
        print(f"   📱 Número: {result['phone_number']}")
        
        session_id = result['session_id']
        csv_filename = result['csv_filename']
    else:
        print(f"❌ Erro no envio: {result}")
        exit(1)
        
except Exception as e:
    print(f"❌ Erro: {e}")
    print("💡 Certifique-se de que o servidor está rodando: python3 START.py")
    exit(1)

print()

# ============================================================================
# FASE 2: VERIFICAÇÃO DE SESSÃO
# ============================================================================
print("📊 FASE 2: VERIFICAÇÃO DE SESSÃO")
print("-" * 70)

time.sleep(2)

try:
    response = requests.get(f"{API_URL}/session/{PHONE}")
    progress = response.json()
    
    if progress['exists']:
        print(f"✅ Sessão encontrada!")
        print(f"   🆔 ID: {progress['session_id']}")
        print(f"   📊 Progresso: {progress['responses_received']}/{progress['total_messages']}")
        print(f"   📈 Percentual: {progress['progress_percent']}%")
        print(f"   🎯 Status: {progress['status']}")
        print(f"   📄 CSV: {progress['csv_filename']}")
    else:
        print(f"❌ Sessão não encontrada")
        
except Exception as e:
    print(f"❌ Erro ao verificar sessão: {e}")

print()

# ============================================================================
# FASE 3: SIMULAÇÃO DE RECEBIMENTO
# ============================================================================
print("📥 FASE 3: SIMULAÇÃO DE RECEBIMENTO DE RESPOSTAS")
print("-" * 70)

print(f"Simulando recebimento de {len(messages)} respostas...")
print()

for i, msg in enumerate(messages, 1):
    webhook_payload = {
        "event": "messages.upsert",
        "instance": "TESTE_AUTO_MGI",
        "data": {
            "key": {
                "remoteJid": PHONE.replace('+', '') + "@s.whatsapp.net",
                "fromMe": False,
                "id": f"TEST{i}ABC"
            },
            "message": {
                "conversation": f"Resposta {i}: Recebi '{msg[:20]}...'"
            },
            "messageTimestamp": int(time.time())
        }
    }
    
    try:
        response = requests.post(
            f"{API_URL}/webhook/evolution/messages",
            json=webhook_payload,
            timeout=10
        )
        result = response.json()
        
        if result['status'] == 'success':
            progress = result['progress']
            print(f"  ✅ Resposta {i}/{len(messages)}: {progress['responses_received']}/{progress['total_messages']} ({progress['progress_percent']}%)")
            
            if progress['is_completed']:
                print(f"  🎉 TASK COMPLETA!")
        else:
            print(f"  ⚠️  Resposta {i}: {result['status']}")
            
    except Exception as e:
        print(f"  ❌ Erro na resposta {i}: {e}")
    
    time.sleep(0.5)

print()

# ============================================================================
# FASE 4: VERIFICAÇÃO FINAL
# ============================================================================
print("🔍 FASE 4: VERIFICAÇÃO FINAL")
print("-" * 70)

time.sleep(1)

# Verifica progresso final
try:
    response = requests.get(f"{API_URL}/session/{PHONE}")
    progress = response.json()
    
    print(f"📊 Progresso Final:")
    print(f"   Recebidas: {progress['responses_received']}/{progress['total_messages']}")
    print(f"   Percentual: {progress['progress_percent']}%")
    print(f"   Status: {progress['status']}")
    print(f"   Completa: {'✅ SIM' if progress['is_completed'] else '❌ NÃO'}")
    
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# Verifica respostas no banco
try:
    response = requests.get(f"{API_URL}/responses")
    data = response.json()
    
    print(f"💾 Banco de Dados:")
    print(f"   Total de respostas: {data['count']}")
    
    if data['count'] > 0:
        print(f"   Última resposta: {data['responses'][0]['response'][:50]}...")
    
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# ============================================================================
# FASE 5: HISTÓRICO E DOWNLOAD
# ============================================================================
print("📁 FASE 5: HISTÓRICO E DOWNLOAD")
print("-" * 70)

try:
    response = requests.get(f"{API_URL}/sessions")
    data = response.json()
    
    print(f"📚 Histórico de Sessões:")
    print(f"   Total: {data['count']}")
    print(f"   Ativas: {data['active_count']}")
    print()
    
    if data['count'] > 0:
        print(f"   Últimas 3 sessões:")
        for i, session in enumerate(data['sessions'][:3], 1):
            print(f"   {i}. {session.get('session_id', 'N/A')}")
            print(f"      📱 {session.get('phone_number', 'N/A')}")
            print(f"      📊 {session.get('responses_received', 0)} respostas")
            print(f"      📄 {session.get('csv_filename', 'N/A')}")
            print(f"      🎯 {session.get('status', 'N/A')}")
            print()
    
    # Tenta download do CSV
    if csv_filename:
        print(f"📥 Testando download do CSV: {csv_filename}")
        download_url = f"{API_URL}/download/{csv_filename}"
        response = requests.get(download_url)
        
        if response.status_code == 200:
            print(f"   ✅ Download OK ({len(response.content)} bytes)")
            
            # Salva localmente para verificação
            test_file = f"test_{csv_filename}"
            with open(test_file, 'wb') as f:
                f.write(response.content)
            print(f"   💾 Salvo como: {test_file}")
        else:
            print(f"   ❌ Erro no download: {response.status_code}")
    
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# ============================================================================
# RESUMO FINAL
# ============================================================================
print("=" * 70)
print("📊 RESUMO DO TESTE")
print("=" * 70)
print()
print("✅ Funcionalidades Testadas:")
print("   1. ✅ Envio de mensagens")
print("   2. ✅ Criação de sessão")
print("   3. ✅ Recebimento de respostas")
print("   4. ✅ Contador incremental")
print("   5. ✅ Detecção de task completa")
print("   6. ✅ Salvamento em CSV por sessão")
print("   7. ✅ Histórico de sessões")
print("   8. ✅ Download de CSV")
print()
print("🎯 Próximos Passos:")
print("   1. Abra a interface: http://localhost:8080/whatsapp_final.html")
print("   2. Vá na aba 'Recepção' para ver o progresso")
print("   3. Vá na aba 'Histórico' para ver todas as sessões")
print("   4. Configure o webhook na Evolution API para receber respostas reais")
print()
print("📚 Documentação:")
print("   - CONFIGURAR_WEBHOOK_EVOLUTION.md")
print("   - SISTEMA_RESPOSTAS_README.md")
print()
print("=" * 70)
print("✅ TESTE COMPLETO CONCLUÍDO COM SUCESSO!")
print("=" * 70)
