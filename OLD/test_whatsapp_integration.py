#!/usr/bin/env python3
"""
Teste específico para verificar se o envio de mensagens via WhatsApp está funcionando.
"""

import asyncio
import logging
from app.nodes.integrations import HTTPRequestNode
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_whatsapp_message():
    """Testa o envio de mensagem via WhatsApp usando o nó HTTP Request."""
    
    # Carrega as configurações
    settings = Settings()
    
    # Dados de teste simulando o que viria do webhook
    test_data = {
        "Edit Fields1": {
            "json": {
                "URL": settings.EVOLUTION_API_URL,
                "instancia": settings.EVOLUTION_INSTANCE,
                "API_KEY": settings.EVOLUTION_API_KEY,
                "Telefone_bot_+556132073332": "+556199999999"
            }
        },
        "Edit Fields": {
            "json": {
                "perguntas": "Esta é uma mensagem de teste automatizada via WhatsApp!"
            }
        }
    }
    
    # Cria o nó HTTP Request configurado para WhatsApp
    whatsapp_node = HTTPRequestNode(
        method="POST",
        url='{{ $item("0").$node["Edit Fields1"].json["URL"] }}/message/sendText/{{ $item("0").$node["Edit Fields1"].json["instancia"] }}',
        headers={
            "apikey": '{{ $item("0").$node["Edit Fields1"].json["API_KEY"] }}'
        },
        json_body='{"number": "+556132073332", "text": "{{ $item(\\"0\\").$node[\\"Edit Fields\\"].json[\\"perguntas\\"] }}"}'
    )
    
    logger.info("=== TESTE DE ENVIO DE MENSAGEM VIA WHATSAPP ===")
    logger.info(f"URL da API: {settings.EVOLUTION_API_URL}")
    logger.info(f"Instância: {settings.EVOLUTION_INSTANCE}")
    logger.info(f"API Key: {settings.EVOLUTION_API_KEY[:10]}...")
    
    # Executa o nó
    result = await whatsapp_node.execute(test_data)
    
    logger.info("=== RESULTADO DO TESTE ===")
    logger.info(f"Resultado: {result}")
    
    return result


async def test_whatsapp_with_real_request():
    """Testa com uma requisição HTTP real (descomente para usar)."""
    import httpx
    
    settings = Settings()
    
    # Dados da mensagem
    url = f"{settings.EVOLUTION_API_URL}/message/sendText/{settings.EVOLUTION_INSTANCE}"
    headers = {
        "apikey": settings.EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "number": "+556132073332",
        "text": "Teste de mensagem automatizada - Sistema funcionando!"
    }
    
    logger.info("=== TESTE COM REQUISIÇÃO HTTP REAL ===")
    logger.info(f"URL: {url}")
    logger.info(f"Headers: {headers}")
    logger.info(f"Payload: {payload}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            
            if response.status_code == 200:
                logger.info("✅ Mensagem enviada com sucesso!")
                return {"success": True, "response": response.json()}
            else:
                logger.error("❌ Falha no envio da mensagem")
                return {"success": False, "error": response.text}
                
    except Exception as e:
        logger.error(f"❌ Erro na requisição: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # Executa o teste simulado por padrão
    result = asyncio.run(test_whatsapp_message())