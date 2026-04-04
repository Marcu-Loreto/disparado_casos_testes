#!/usr/bin/env python3
"""
Teste simples do webhook sem dependências extras.
"""

import asyncio
import json
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_URL = "http://localhost:8000"


async def test_simple_webhook():
    """Testa o webhook com payload simples."""
    
    payload = {
        "phone_number": "+556132073332",
        "messages": [
            {"text": "🤖 Teste webhook simplificado - Mensagem 1", "delay": 2},
            {"text": "📱 Sistema funcionando perfeitamente!", "delay": 3},
            {"text": "✅ Integração WhatsApp ativa", "delay": 2}
        ]
    }
    
    logger.info("=== TESTE WEBHOOK SIMPLIFICADO ===")
    logger.info(f"URL: {WEBHOOK_URL}/webhook/tela2")
    logger.info(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Primeiro testa health
            health_response = await client.get(f"{WEBHOOK_URL}/health")
            logger.info(f"Health check: {health_response.status_code}")
            
            if health_response.status_code != 200:
                logger.error("❌ Servidor não está respondendo")
                return
            
            # Testa o webhook
            response = await client.post(
                f"{WEBHOOK_URL}/webhook/tela2",
                json=payload
            )
            
            logger.info(f"Status: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Teste bem-sucedido!")
                logger.info(f"📊 Mensagens enviadas: {result.get('sent_messages', 0)}")
                logger.info(f"📱 Telefone: {result.get('phone_number')}")
                return result
            else:
                logger.error("❌ Teste falhou")
                return None
                
    except httpx.ConnectError:
        logger.error("❌ Não foi possível conectar ao servidor")
        logger.error("Certifique-se de que o servidor está rodando:")
        logger.error("python3 -m app.simple_webhook_server")
        return None
    except Exception as e:
        logger.error(f"❌ Erro no teste: {e}")
        return None


async def test_text_list():
    """Testa com lista de texto."""
    
    payload = {
        "phone_number": "+556132073332",
        "text_list": """🤖 Primeira mensagem via texto
📱 Segunda mensagem do sistema
✅ Terceira mensagem de confirmação"""
    }
    
    logger.info("=== TESTE LISTA DE TEXTO ===")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{WEBHOOK_URL}/webhook/tela2",
                json=payload
            )
            
            logger.info(f"Status: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Teste lista de texto bem-sucedido!")
                return result
            else:
                logger.error("❌ Teste lista de texto falhou")
                return None
                
    except Exception as e:
        logger.error(f"❌ Erro no teste lista de texto: {e}")
        return None


async def test_legacy_format():
    """Testa formato legado N8N."""
    
    payload = {
        "body": {
            "method": "webhook",
            "testCases": [
                "🤖 Teste formato legado - Caso 1",
                "📱 Compatibilidade N8N mantida",
                "✅ Sistema funcionando"
            ],
            "chatbotPhone": "+556132073332"
        }
    }
    
    logger.info("=== TESTE FORMATO LEGADO ===")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{WEBHOOK_URL}/webhook/tela2",
                json=payload
            )
            
            logger.info(f"Status: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Teste formato legado bem-sucedido!")
                return result
            else:
                logger.error("❌ Teste formato legado falhou")
                return None
                
    except Exception as e:
        logger.error(f"❌ Erro no teste formato legado: {e}")
        return None


async def run_tests():
    """Executa todos os testes."""
    
    print("🧪 EXECUTANDO TESTES DO WEBHOOK SIMPLIFICADO\n")
    
    tests = [
        ("Webhook Simples", test_simple_webhook),
        ("Lista de Texto", test_text_list),
        ("Formato Legado", test_legacy_format)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"🔍 {test_name}")
        print('='*40)
        
        result = await test_func()
        results[test_name] = result is not None
        
        await asyncio.sleep(1)  # Pequeno delay entre testes
    
    # Resumo
    print(f"\n{'='*40}")
    print("📊 RESUMO DOS TESTES")
    print('='*40)
    
    for test_name, success in results.items():
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram!")
        print("🚀 Sistema de webhook está funcionando corretamente!")
    else:
        print("\n⚠️ Alguns testes falharam.")


if __name__ == "__main__":
    asyncio.run(run_tests())