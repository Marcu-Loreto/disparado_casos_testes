#!/usr/bin/env python3
"""
Response Receiver - Recebe respostas do WhatsApp via webhook Evolution API
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ResponseReceiver:
    """Recebe e processa respostas do WhatsApp."""
    
    def __init__(self):
        # Armazena números ativos aguardando respostas
        self.active_numbers = {}
    
    def register_number(self, phone_number: str):
        """
        Registra um número como ativo para receber respostas.
        
        Args:
            phone_number: Número que foi enviado mensagens
        """
        # Normaliza número (remove +, espaços, etc)
        normalized = self.normalize_phone(phone_number)
        
        self.active_numbers[normalized] = {
            "registered_at": datetime.now().isoformat(),
            "phone_number": phone_number,
            "responses_count": 0
        }
        
        logger.info(f"Número {phone_number} registrado para receber respostas")
    
    def unregister_number(self, phone_number: str):
        """Remove número da lista de ativos."""
        normalized = self.normalize_phone(phone_number)
        if normalized in self.active_numbers:
            del self.active_numbers[normalized]
            logger.info(f"Número {phone_number} removido da lista ativa")
    
    def is_number_active(self, phone_number: str) -> bool:
        """Verifica se número está ativo para receber respostas."""
        normalized = self.normalize_phone(phone_number)
        return normalized in self.active_numbers
    
    def process_incoming_message(self, webhook_data: Dict) -> Optional[Dict]:
        """
        Processa mensagem recebida do webhook Evolution API.
        
        Args:
            webhook_data: Dados do webhook da Evolution API
            
        Returns:
            Dict com dados processados ou None se deve ignorar
        """
        try:
            # Extrai dados da mensagem
            data = webhook_data.get("data", {})
            
            # Verifica se é mensagem recebida (não enviada)
            if data.get("key", {}).get("fromMe"):
                logger.debug("Mensagem enviada por nós, ignorando")
                return None
            
            # Extrai informações
            remote_jid = data.get("key", {}).get("remoteJid", "")
            message_text = self.extract_message_text(data)
            timestamp = data.get("messageTimestamp", datetime.now().timestamp())
            
            if not remote_jid or not message_text:
                logger.debug("Mensagem sem remetente ou texto, ignorando")
                return None
            
            # Normaliza número do remetente
            sender_number = self.extract_phone_from_jid(remote_jid)
            
            # Verifica se é de um número ativo
            if not self.is_number_active(sender_number):
                logger.debug(f"Número {sender_number} não está na lista ativa, ignorando")
                return None
            
            # Atualiza contador
            normalized = self.normalize_phone(sender_number)
            self.active_numbers[normalized]["responses_count"] += 1
            
            # Formata timestamp
            dt = datetime.fromtimestamp(int(timestamp))
            formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
            
            logger.info(f"Resposta recebida de {sender_number}: {message_text[:50]}...")
            
            return {
                "phone_number": sender_number,
                "message": message_text,
                "timestamp": formatted_timestamp,
                "remote_jid": remote_jid,
                "raw_data": data
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem recebida: {e}")
            return None
    
    def extract_message_text(self, data: Dict) -> str:
        """Extrai texto da mensagem de diferentes formatos."""
        message = data.get("message", {})
        
        # Tenta diferentes formatos de mensagem
        text = (
            message.get("conversation") or
            message.get("extendedTextMessage", {}).get("text") or
            message.get("imageMessage", {}).get("caption") or
            message.get("videoMessage", {}).get("caption") or
            ""
        )
        
        return text.strip()
    
    def extract_phone_from_jid(self, jid: str) -> str:
        """
        Extrai número de telefone do JID do WhatsApp.
        
        Exemplos:
        - 5561999999999@s.whatsapp.net -> 5561999999999
        - 5561999999999 -> 5561999999999
        """
        # Remove sufixo @s.whatsapp.net ou @g.us
        phone = jid.split("@")[0]
        
        # Remove caracteres não numéricos
        phone = ''.join(filter(str.isdigit, phone))
        
        return phone
    
    def normalize_phone(self, phone: str) -> str:
        """
        Normaliza número de telefone para comparação.
        
        Remove +, espaços, hífens, etc.
        """
        # Remove tudo exceto dígitos
        normalized = ''.join(filter(str.isdigit, phone))
        
        return normalized
    
    def get_active_numbers(self) -> Dict:
        """Retorna lista de números ativos."""
        return self.active_numbers.copy()


# Instância global
response_receiver = ResponseReceiver()
