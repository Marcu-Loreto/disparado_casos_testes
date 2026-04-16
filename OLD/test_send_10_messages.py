#!/usr/bin/env python3
"""
Teste de envio de 10 mensagens com intervalo de 3 segundos
"""

import json
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime

# Configuração
API_URL = "http://localhost:8000/webhook/tela2"
PHONE_NUMBER = "+5519993388617"
DELAY = 3  # segundos entre mensagens

# 10 mensagens de teste
MESSAGES = [
    "🧪 Mensagem 1 - Teste de envio automático",
    "📱 Mensagem 2 - Sistema funcionando",
    "✅ Mensagem 3 - Integração ativa",
    "🔥 Mensagem 4 - Processamento OK",
    "⚡ Mensagem 5 - Metade do teste",
    "🎯 Mensagem 6 - Continuando envio",
    "📊 Mensagem 7 - Monitoramento ativo",
    "🛡️ Mensagem 8 - Validação OK",
    "🌟 Mensagem 9 - Quase lá",
    "🎉 Mensagem 10 - Teste concluído!"
]

print("=" * 60)
print("🧪 TESTE DE ENVIO DE 10 MENSAGENS")
print("=" * 60)
print(f"📞 Número destino: {PHONE_NUMBER}")
print(f"⏱️  Intervalo: {DELAY} segundos")
print(f"📊 Total de mensagens: {len(MESSAGES)}")
print("=" * 60)
print()

# Prepara payload
text_list = "\n".join(MESSAGES)
payload = {
    "phone_number": PHONE_NUMBER,
    "text_list": text_list
}

print("📤 Enviando mensagens...")
print()

try:
    # Prepara requisição
    data = json.dumps(payload).encode('utf-8')
    req = Request(
        API_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    # Envia requisição
    start_time = time.time()
    
    with urlopen(req, timeout=300) as response:  # 5 minutos de timeout
        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("=" * 60)
        print("✅ ENVIO CONCLUÍDO!")
        print("=" * 60)
        print(f"Status: {result.get('status')}")
        print(f"Mensagens enviadas: {result.get('sent_messages')}/{result.get('total_messages')}")
        print(f"Número: {result.get('phone_number')}")
        print(f"Tempo total: {duration:.1f} segundos")
        print(f"Tempo esperado: {len(MESSAGES) * DELAY} segundos")
        print("=" * 60)
        print()
        
        # Mostra primeiros resultados
        if 'results' in result and result['results']:
            print("📋 Primeiras mensagens enviadas:")
            for i, msg_result in enumerate(result['results'][:5], 1):
                status = msg_result.get('status', 'unknown')
                text = msg_result.get('text', '')[:50]
                print(f"  {i}. [{status}] {text}...")
            print()
        
        print("=" * 60)
        print("📥 PRÓXIMOS PASSOS:")
        print("=" * 60)
        print("1. ✅ Número registrado para receber respostas")
        print("2. 📱 Responda pelo WhatsApp no número:", PHONE_NUMBER)
        print("3. 🔍 Verifique respostas em:")
        print("   - Interface: http://localhost:8080/whatsapp_complete.html")
        print("   - API: http://localhost:8000/responses")
        print("   - CSV: cat responses.csv")
        print()
        print("4. 📊 Números ativos:")
        print("   curl http://localhost:8000/active-numbers")
        print("=" * 60)
        
except HTTPError as e:
    print(f"❌ Erro HTTP {e.code}: {e.reason}")
    try:
        error_data = e.read().decode('utf-8')
        print(f"Detalhes: {error_data}")
    except:
        pass
except URLError as e:
    print(f"❌ Erro de conexão: {e.reason}")
    print()
    print("💡 Certifique-se de que o servidor está rodando:")
    print("   python3 START.py")
except Exception as e:
    print(f"❌ Erro: {e}")

print()
