#!/usr/bin/env python3
"""
Teste do workflow completo incluindo o envio de mensagens via WhatsApp.
"""

import asyncio
import logging
from app.workflow import WorkflowExecutor
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_complete_workflow():
    """Testa o workflow completo com foco no envio de mensagens."""
    
    settings = Settings()
    
    # Dados de teste que simulam um webhook real
    webhook_data = {
        "body": {
            "method": "manual",  # Mudando para "manual" para seguir o caminho correto
            "testCases": [
                "Teste de caso 1: Verificar login",
                "Teste de caso 2: Verificar cadastro", 
                "Teste de caso 3: Verificar pagamento"
            ],
            "chatbotPhone": "+556199999999"
        }
    }
    
    logger.info("=== TESTE DO WORKFLOW COMPLETO ===")
    logger.info(f"Dados do webhook: {webhook_data}")
    
    # Inicializa o executor do workflow
    executor = WorkflowExecutor(settings)
    
    # Modifica o HTTPRequestNode para fazer requisições reais
    from app.nodes.integrations import HTTPRequestNode
    
    # Substitui o método execute do HTTPRequestNode para fazer requisições reais
    original_execute = HTTPRequestNode.execute
    
    async def real_http_execute(self, data=None):
        """Versão que faz requisições HTTP reais."""
        if not self.url:
            logger.warning("HTTP Request node has no URL")
            return data or {}

        # Resolve URL e headers
        resolved_url = self._resolve_template(self.url, data) if data else self.url
        resolved_headers = {}
        for key, value in self.headers.items():
            resolved_headers[key] = (
                self._resolve_template(str(value), data) if data else value
            )

        # Prepara o body da requisição
        json_data = None
        if self.json_body:
            try:
                resolved_body = (
                    self._resolve_template(self.json_body, data)
                    if data
                    else self.json_body
                )
                import json
                json_data = json.loads(resolved_body)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON body: {e}")
                return {"error": "Invalid JSON body"}

        logger.info(f"🚀 Fazendo requisição {self.method} para: {resolved_url}")
        logger.info(f"📋 Headers: {resolved_headers}")
        logger.info(f"📦 Payload: {json_data}")

        # Faz a requisição HTTP real
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                if self.method == "POST":
                    response = await client.post(resolved_url, json=json_data, headers=resolved_headers)
                elif self.method == "GET":
                    response = await client.get(resolved_url, headers=resolved_headers)
                else:
                    logger.warning(f"Método HTTP não suportado: {self.method}")
                    return {"error": f"Unsupported method: {self.method}"}
                
                logger.info(f"✅ Resposta recebida - Status: {response.status_code}")
                logger.info(f"📄 Resposta: {response.text}")
                
                if response.status_code in [200, 201]:
                    try:
                        return {"json": response.json()}
                    except:
                        return {"json": {"status": "sent", "response": response.text}}
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text}"}
                    
        except Exception as e:
            logger.error(f"❌ Erro na requisição HTTP: {e}")
            return {"error": str(e)}
    
    # Substitui temporariamente o método
    HTTPRequestNode.execute = real_http_execute
    
    try:
        # Executa o workflow
        result = await executor.execute(webhook_data)
        
        logger.info("=== RESULTADO DO WORKFLOW ===")
        
        # Verifica se o HTTP Request1 foi executado
        if "HTTP Request1" in result:
            http_result = result["HTTP Request1"]
            logger.info(f"📱 Resultado do envio WhatsApp: {http_result}")
            
            if "error" not in http_result:
                logger.info("✅ SUCESSO: Mensagem enviada via WhatsApp!")
            else:
                logger.error(f"❌ ERRO no envio: {http_result['error']}")
        else:
            logger.warning("⚠️ Nó HTTP Request1 não foi executado")
            
        # Mostra todos os nós executados
        logger.info("📋 Nós executados:")
        for node_name in result.keys():
            logger.info(f"  - {node_name}")
            
        return result
        
    finally:
        # Restaura o método original
        HTTPRequestNode.execute = original_execute


if __name__ == "__main__":
    result = asyncio.run(test_complete_workflow())