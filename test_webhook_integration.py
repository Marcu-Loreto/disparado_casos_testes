#!/usr/bin/env python3
"""
Teste completo da integração webhook para WhatsApp.
"""

import asyncio
import json
import httpx
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_URL = "http://localhost:8000"


async def test_json_webhook():
    """Testa o webhook com payload JSON."""
    
    payload = {
        "phone_number": "+556132073332",
        "messages": [
            {"text": "🤖 Teste JSON - Mensagem 1", "delay": 2},
            {"text": "📱 Sistema funcionando via JSON!", "delay": 3},
            {"text": "✅ Integração WhatsApp ativa", "delay": 2}
        ]
    }
    
    logger.info("=== TESTE WEBHOOK JSON ===")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
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
                logger.info("✅ Teste JSON bem-sucedido!")
                return result
            else:
                logger.error("❌ Teste JSON falhou")
                return None
                
    except Exception as e:
        logger.error(f"❌ Erro no teste JSON: {e}")
        return None


async def test_paste_webhook():
    """Testa o webhook com texto colado."""
    
    payload = {
        "phone_number": "+556132073332",
        "text_list": """🤖 Teste texto colado - Linha 1
📱 Sistema funcionando via paste!
✅ Mensagens enviadas linha por linha"""
    }
    
    logger.info("=== TESTE WEBHOOK TEXTO COLADO ===")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
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
                logger.info("✅ Teste texto colado bem-sucedido!")
                return result
            else:
                logger.error("❌ Teste texto colado falhou")
                return None
                
    except Exception as e:
        logger.error(f"❌ Erro no teste texto colado: {e}")
        return None


async def test_legacy_webhook():
    """Testa o webhook com formato legado do N8N."""
    
    payload = {
        "phone_number": "+556132073332",
        "body": {
            "method": "webhook",
            "testCases": [
                "🤖 Teste formato legado - Caso 1",
                "📱 Compatibilidade N8N mantida",
                "✅ Sistema funcionando perfeitamente"
            ],
            "chatbotPhone": "+556132073332"
        }
    }
    
    logger.info("=== TESTE WEBHOOK FORMATO LEGADO ===")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
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


async def test_health_endpoint():
    """Testa o endpoint de health check."""
    
    logger.info("=== TESTE HEALTH CHECK ===")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{WEBHOOK_URL}/health")
            
            logger.info(f"Status: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                logger.info("✅ Health check OK!")
                return True
            else:
                logger.error("❌ Health check falhou")
                return False
                
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
        return False


async def test_csv_content():
    """Testa processamento de conteúdo CSV inline."""
    
    payload = {
        "phone_number": "+556132073332",
        "csv_content": """text,delay
🤖 Teste CSV - Mensagem 1,2
📱 Sistema funcionando via CSV!,3
✅ Processamento CSV ativo,2"""
    }
    
    logger.info("=== TESTE CSV INLINE ===")
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
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
                logger.info("✅ Teste CSV inline bem-sucedido!")
                return result
            else:
                logger.error("❌ Teste CSV inline falhou")
                return None
                
    except Exception as e:
        logger.error(f"❌ Erro no teste CSV inline: {e}")
        return None


async def run_all_tests():
    """Executa todos os testes."""
    
    print("🚀 INICIANDO TESTES DE INTEGRAÇÃO WEBHOOK\n")
    
    # Testa health check primeiro
    health_ok = await test_health_endpoint()
    if not health_ok:
        print("❌ Servidor não está respondendo. Certifique-se de que está rodando.")
        return
    
    print()
    
    # Executa todos os testes
    tests = [
        ("JSON", test_json_webhook),
        ("Texto Colado", test_paste_webhook),
        ("Formato Legado", test_legacy_webhook),
        ("CSV Inline", test_csv_content)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        result = await test_func()
        results[test_name] = result is not None
        
        # Pequeno delay entre testes
        await asyncio.sleep(2)
    
    # Resumo final
    print(f"\n{'='*50}")
    print("📊 RESUMO DOS TESTES:")
    
    for test_name, success in results.items():
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"   {test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Integração funcionando perfeitamente.")
    else:
        print("⚠️ Alguns testes falharam. Verifique os logs acima.")


if __name__ == "__main__":
    print("Para executar os testes, certifique-se de que o servidor webhook está rodando:")
    print("./venv/bin/python -m app.webhook_server")
    print()
    
    choice = input("Servidor está rodando? (s/n): ").lower().strip()
    
    if choice == 's':
        asyncio.run(run_all_tests())
    else:
        print("Inicie o servidor primeiro e execute este teste novamente.")