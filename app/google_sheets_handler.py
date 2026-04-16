#!/usr/bin/env python3
"""
Google Sheets Handler - Salva respostas recebidas
Usa SQLite como armazenamento principal + CSV/Sheets como backup
"""

import json
import logging
import csv
import os
from datetime import datetime
from config.settings import Settings
from app.database import db_handler

logger = logging.getLogger(__name__)
settings = Settings()


class GoogleSheetsHandler:
    """Handler para salvar respostas."""
    
    def __init__(self, storage_type="sqlite"):
        """
        Inicializa handler.
        
        Args:
            storage_type: "sqlite" (padrão), "csv", ou "sheets"
        """
        self.storage_type = storage_type
        self.document_id = settings.GOOGLE_SHEETS_DOCUMENT_ID
        self.sheet_id = "1646724078"
    
    def save_response(self, phone_number: str, message: str, timestamp: str = None):
        """
        Salva resposta recebida no banco SQLite.
        
        Args:
            phone_number: Número que enviou a resposta
            message: Texto da mensagem recebida
            timestamp: Data/hora da mensagem (opcional)
        """
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Salva no banco SQLite (principal)
            success = db_handler.save_response(timestamp, phone_number, message)
            
            if success:
                logger.info(f"✅ Resposta salva: {phone_number} - {message[:50]}...")
                return {
                    "success": True,
                    "message": "Resposta salva no banco de dados",
                    "data": {
                        "timestamp": timestamp,
                        "phone_number": phone_number,
                        "response": message
                    },
                    "storage": "sqlite"
                }
            else:
                return {
                    "success": False,
                    "error": "Falha ao salvar no banco"
                }
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resposta: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_responses_csv(self):
        """Retorna todas as respostas do banco."""
        responses = db_handler.get_all_responses()
        
        # Converte para formato CSV compatível
        csv_responses = []
        for r in responses:
            csv_responses.append({
                'Timestamp': r['timestamp'],
                'Phone Number': r['phone_number'],
                'Response': r['response']
            })
        
        return csv_responses
    
    def append_row(self, values: list):
        """
        Adiciona uma nova linha.
        
        Args:
            values: Lista de valores [timestamp, phone, message]
        """
        if len(values) >= 3:
            return self.save_response(values[1], values[2], values[0])
        else:
            return {"success": False, "error": "Valores insuficientes"}
