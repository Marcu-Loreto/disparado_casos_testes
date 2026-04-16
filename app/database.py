#!/usr/bin/env python3
"""
Database Handler - SQLite para armazenar histórico de respostas
"""

import sqlite3
import logging
import os
from datetime import datetime
from typing import List, Dict, Optional
import csv

logger = logging.getLogger(__name__)


class DatabaseHandler:
    """Handler para banco de dados SQLite."""
    
    def __init__(self, db_path: str = "whatsapp_responses.db"):
        """
        Inicializa handler do banco de dados.
        
        Args:
            db_path: Caminho do arquivo do banco de dados
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Cria tabelas se não existirem."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de respostas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de exportações (histórico de CSVs gerados)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                total_records INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_phone_number 
            ON responses(phone_number)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON responses(timestamp)
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Banco de dados inicializado: {self.db_path}")
    
    def save_response(self, timestamp: str, phone_number: str, message: str) -> bool:
        """
        Salva resposta no banco de dados.
        
        Args:
            timestamp: Data/hora da resposta
            phone_number: Número que enviou
            message: Texto da mensagem
            
        Returns:
            True se salvou com sucesso
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO responses (timestamp, phone_number, response) VALUES (?, ?, ?)',
                (timestamp, phone_number, message)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"💾 Resposta salva no banco: {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar no banco: {e}")
            return False
    
    def get_all_responses(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Retorna todas as respostas.
        
        Args:
            limit: Limite de registros (None = todos)
            
        Returns:
            Lista de dicionários com as respostas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if limit:
                cursor.execute(
                    'SELECT * FROM responses ORDER BY id DESC LIMIT ?',
                    (limit,)
                )
            else:
                cursor.execute('SELECT * FROM responses ORDER BY id DESC')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar respostas: {e}")
            return []
    
    def get_responses_by_phone(self, phone_number: str) -> List[Dict]:
        """Retorna respostas de um número específico."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT * FROM responses WHERE phone_number = ? ORDER BY id DESC',
                (phone_number,)
            )
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar respostas por número: {e}")
            return []
    
    def get_total_responses(self) -> int:
        """Retorna total de respostas no banco."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM responses')
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
            
        except Exception as e:
            logger.error(f"❌ Erro ao contar respostas: {e}")
            return 0
    
    def export_to_csv(self, output_dir: str = "exports") -> Dict:
        """
        Exporta todas as respostas para CSV com timestamp.
        
        Args:
            output_dir: Diretório para salvar o CSV
            
        Returns:
            Dicionário com informações da exportação
        """
        try:
            # Cria diretório se não existir
            os.makedirs(output_dir, exist_ok=True)
            
            # Nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"respostas_whatsapp_{timestamp}.csv"
            filepath = os.path.join(output_dir, filename)
            
            # Busca todas as respostas
            responses = self.get_all_responses()
            
            if not responses:
                return {
                    "success": False,
                    "error": "Nenhuma resposta para exportar"
                }
            
            # Cria CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Timestamp', 'Phone Number', 'Response', 'Created At'])
                
                for r in responses:
                    writer.writerow([
                        r['id'],
                        r['timestamp'],
                        r['phone_number'],
                        r['response'],
                        r['created_at']
                    ])
            
            # Registra exportação
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO exports (filename, filepath, total_records) VALUES (?, ?, ?)',
                (filename, filepath, len(responses))
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"📥 CSV exportado: {filepath} ({len(responses)} registros)")
            
            return {
                "success": True,
                "filename": filename,
                "filepath": filepath,
                "total_records": len(responses),
                "timestamp": timestamp
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao exportar CSV: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_export_history(self) -> List[Dict]:
        """Retorna histórico de exportações."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM exports ORDER BY id DESC')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar histórico: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas do banco."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de respostas
            cursor.execute('SELECT COUNT(*) FROM responses')
            total_responses = cursor.fetchone()[0]
            
            # Números únicos
            cursor.execute('SELECT COUNT(DISTINCT phone_number) FROM responses')
            unique_numbers = cursor.fetchone()[0]
            
            # Primeira resposta
            cursor.execute('SELECT MIN(created_at) FROM responses')
            first_response = cursor.fetchone()[0]
            
            # Última resposta
            cursor.execute('SELECT MAX(created_at) FROM responses')
            last_response = cursor.fetchone()[0]
            
            # Total de exportações
            cursor.execute('SELECT COUNT(*) FROM exports')
            total_exports = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_responses": total_responses,
                "unique_numbers": unique_numbers,
                "first_response": first_response,
                "last_response": last_response,
                "total_exports": total_exports
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar estatísticas: {e}")
            return {}


# Instância global
db_handler = DatabaseHandler()
