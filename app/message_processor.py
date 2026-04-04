#!/usr/bin/env python3
"""
Processador de mensagens para WhatsApp com suporte a diferentes formatos.
"""

import asyncio
import logging
from typing import Dict, Any, List
import httpx
from datetime import datetime

from config.settings import Settings

logger = logging.getLogger(__name__)


class WhatsAppMessageProcessor:
    """Processador de mensagens para WhatsApp."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_url = settings.EVOLUTION_API_URL
        self.api_key = settings.EVOLUTION_API_KEY
        self.instance = settings.EVOLUTION_INSTANCE
    
    async def send_message_batch(
        self, 
        phone_number: str, 
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Envia um lote de mensagens com delays configuráveis.
        
        Args:
            phone_number: Número do telefone de destino
            messages: Lista de mensagens com texto e delay
            
        Returns:
            Lista com resultados de cada envio
        """
        results = []
        
        logger.info(f"Iniciando envio de {len(messages)} mensagens para {phone_number}")
        
        for i, message in enumerate(messages):
            try:
                # Envia a mensagem
                result = await self.send_single_message(
                    phone_number=phone_number,
                    text=message["text"]
                )
                
                results.append({
                    "index": i,
                    "text": message["text"],
                    "status": "sent" if result.get("success") else "failed",
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })
                
                logger.info(f"Mensagem {i+1}/{len(messages)} enviada: {result.get('status', 'unknown')}")
                
                # Aplica delay antes da próxima mensagem (exceto na última)
                if i < len(messages) - 1:
                    delay = message.get("delay", 2)
                    logger.info(f"Aguardando {delay}s antes da próxima mensagem...")
                    await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"Erro ao enviar mensagem {i+1}: {e}")
                results.append({
                    "index": i,
                    "text": message["text"],
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Estatísticas finais
        sent_count = sum(1 for r in results if r["status"] == "sent")
        failed_count = len(results) - sent_count
        
        logger.info(f"Envio concluído: {sent_count} enviadas, {failed_count} falharam")
        
        return results
    
    async def send_single_message(self, phone_number: str, text: str) -> Dict[str, Any]:
        """
        Envia uma única mensagem via WhatsApp.
        
        Args:
            phone_number: Número do telefone
            text: Texto da mensagem
            
        Returns:
            Resultado do envio
        """
        url = f"{self.api_url}/message/sendText/{self.instance}"
        headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "number": phone_number,
            "text": text
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code in [200, 201]:
                    return {
                        "success": True,
                        "status": "sent",
                        "response": response.json(),
                        "message_id": response.json().get("key", {}).get("id")
                    }
                else:
                    return {
                        "success": False,
                        "status": "failed",
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "error": str(e)
            }
    
    async def validate_phone_number(self, phone_number: str) -> bool:
        """
        Valida se o número de telefone está ativo no WhatsApp.
        
        Args:
            phone_number: Número para validar
            
        Returns:
            True se válido, False caso contrário
        """
        # Remove caracteres especiais do número
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # Validação básica de formato brasileiro
        if len(clean_number) < 10 or len(clean_number) > 13:
            return False
        
        # Aqui poderia fazer uma verificação real via API
        # Por enquanto, assume que números com formato correto são válidos
        return True
    
    def format_phone_number(self, phone_number: str) -> str:
        """
        Formata o número de telefone para o padrão correto.
        
        Args:
            phone_number: Número original
            
        Returns:
            Número formatado
        """
        # Remove todos os caracteres não numéricos
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # Adiciona código do país se não tiver
        if len(clean_number) == 11 and clean_number.startswith('11'):
            # Número de São Paulo sem código do país
            clean_number = '55' + clean_number
        elif len(clean_number) == 10:
            # Número sem DDD, assume São Paulo
            clean_number = '5511' + clean_number
        
        return clean_number


class MessageBatchValidator:
    """Validador para lotes de mensagens."""
    
    @staticmethod
    def validate_message_batch(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Valida um lote de mensagens.
        
        Args:
            messages: Lista de mensagens para validar
            
        Returns:
            Resultado da validação
        """
        if not messages:
            return {"valid": False, "error": "Lista de mensagens vazia"}
        
        if len(messages) > 1000:
            return {"valid": False, "error": "Máximo de 1000 mensagens por lote"}
        
        errors = []
        for i, message in enumerate(messages):
            if not isinstance(message, dict):
                errors.append(f"Mensagem {i+1}: deve ser um objeto")
                continue
            
            if "text" not in message or not message["text"].strip():
                errors.append(f"Mensagem {i+1}: texto é obrigatório")
            
            if len(message.get("text", "")) > 4096:
                errors.append(f"Mensagem {i+1}: texto muito longo (máx 4096 caracteres)")
            
            delay = message.get("delay", 2)
            if not isinstance(delay, (int, float)) or delay < 0 or delay > 60:
                errors.append(f"Mensagem {i+1}: delay deve ser entre 0 e 60 segundos")
        
        if errors:
            return {"valid": False, "errors": errors}
        
        return {"valid": True, "message_count": len(messages)}