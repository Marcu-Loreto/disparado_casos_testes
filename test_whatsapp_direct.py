#!/usr/bin/env python3
"""
Teste direto para verificar se a API do WhatsApp está funcionando.
"""

import asyncio
import httpx
import logging
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_whatsapp_api_direct():
    """Testa diretamente a API do Evolution para WhatsApp."""
    
    settings = Settings()
    
    # URL e dados da requisição
    url = f"{settings.EVOLUTION_API_URL}/message/sendText/{settings.EVOLUTION_INSTANCE}"
    headers = {
        "apikey": settings.EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "number": "+556132073332",
        "text": "🤖 Teste automatizado - Sistema de mensagens funcionando!"
    }
    
    logger.info("=== TESTE DIRETO DA API WHATSAPP ===")
    logger.info(f"URL: {url}")
    logger.info(f"Instância: {settings.EVOLUTION_INSTANCE}")
    logger.info(f"API Key: {settings.EVOLUTION_API_KEY[:10]}...")
    logger.info(f"Payload: {payload}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            logger.info("Enviando requisição...")
            response = await client.post(url, json=payload, headers=headers)
            
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Body: {response.text}")
            
            if response.status_code == 200 or response.status_code == 201:
                logger.info("✅ SUCESSO: Mensagem enviada com sucesso!")
                try:
                    response_data = response.json()
                    return {"success": True, "response": response_data}
                except:
                    return {"success": True, "response": response.text}
            else:
                logger.error(f"❌ FALHA: Status {response.status_code}")
                return {"success": False, "error": response.text, "status_code": response.status_code}
                
    except httpx.TimeoutException:
        logger.error("❌ ERRO: Timeout na requisição")
        return {"success": False, "error": "Timeout"}
    except httpx.ConnectError:
        logger.error("❌ ERRO: Não foi possível conectar à API")
        return {"success": False, "error": "Connection error"}
    except Exception as e:
        logger.error(f"❌ ERRO: {e}")
        return {"success": False, "error": str(e)}


async def test_api_status():
    """Testa se a API está respondendo."""
    
    settings = Settings()
    
    # Testa endpoint de status ou info
    url = f"{settings.EVOLUTION_API_URL}/instance/fetchInstances"
    headers = {
        "apikey": settings.EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    
    logger.info("=== TESTE DE STATUS DA API ===")
    logger.info(f"URL: {url}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                logger.info("✅ API está respondendo")
                return {"success": True, "response": response.json()}
            else:
                logger.warning(f"⚠️ API respondeu com status {response.status_code}")
                return {"success": False, "status_code": response.status_code}
                
    except Exception as e:
        logger.error(f"❌ Erro ao testar API: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    print("=== ANÁLISE DA INTEGRAÇÃO WHATSAPP ===\n")
    
    # Testa status da API
    print("1. Testando status da API...")
    status_result = asyncio.run(test_api_status())
    print(f"Resultado: {status_result}\n")
    
    # Testa envio de mensagem
    print("2. Testando envio de mensagem...")
    message_result = asyncio.run(test_whatsapp_api_direct())
    print(f"Resultado: {message_result}\n")
    
    # Análise final
    print("=== ANÁLISE FINAL ===")
    if message_result.get("success"):
        print("✅ FUNCIONANDO: O sistema de envio de mensagens via WhatsApp está operacional!")
    else:
        print("❌ PROBLEMA: Há problemas na integração com WhatsApp")
        print("Possíveis causas:")
        print("- API Key inválida ou expirada")
        print("- Instância não configurada corretamente")
        print("- Problemas de conectividade")
        print("- Endpoint da API alterado")