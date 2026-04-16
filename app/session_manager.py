#!/usr/bin/env python3
"""
Session Manager - Gerencia sessões de envio e recebimento de mensagens
Cada envio cria uma sessão única com CSV próprio
"""

import logging
import os
import csv
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class Session:
    """Representa uma sessão de envio/recebimento."""
    session_id: str
    phone_number: str
    total_messages_sent: int
    responses_received: int
    started_at: str
    csv_filename: str
    status: str  # 'active', 'completed', 'expired'
    
    def to_dict(self):
        return asdict(self)


class SessionManager:
    """Gerencia sessões de envio e recebimento."""
    
    def __init__(self, sessions_dir: str = "sessions"):
        """
        Inicializa gerenciador de sessões.
        
        Args:
            sessions_dir: Diretório para armazenar CSVs das sessões
        """
        self.sessions_dir = sessions_dir
        self.active_sessions: Dict[str, Session] = {}
        
        # Cria diretório se não existir
        os.makedirs(sessions_dir, exist_ok=True)
        
        logger.info(f"✅ Session Manager inicializado: {sessions_dir}")
    
    def create_session(self, phone_number: str, total_messages: int) -> Session:
        """
        Cria nova sessão de envio.
        
        Args:
            phone_number: Número que receberá mensagens
            total_messages: Total de mensagens enviadas
            
        Returns:
            Objeto Session criado
        """
        # Gera ID único da sessão
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"{phone_number.replace('+', '')}_{timestamp}"
        
        # Nome do CSV
        csv_filename = f"respostas_{session_id}.csv"
        csv_path = os.path.join(self.sessions_dir, csv_filename)
        
        # Cria CSV com cabeçalho
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Phone Number', 'Response', 'Session ID'])
        
        # Cria sessão
        session = Session(
            session_id=session_id,
            phone_number=phone_number,
            total_messages_sent=total_messages,
            responses_received=0,
            started_at=datetime.now().isoformat(),
            csv_filename=csv_filename,
            status='active'
        )
        
        # Armazena sessão ativa
        self.active_sessions[phone_number] = session
        
        logger.info(f"📝 Sessão criada: {session_id} para {phone_number}")
        logger.info(f"📄 CSV: {csv_filename}")
        
        return session
    
    def get_session(self, phone_number: str) -> Optional[Session]:
        """
        Retorna sessão ativa para um número.
        
        Args:
            phone_number: Número de telefone
            
        Returns:
            Session ou None se não existir
        """
        return self.active_sessions.get(phone_number)
    
    def add_response(self, phone_number: str, message: str, timestamp: str = None) -> bool:
        """
        Adiciona resposta à sessão ativa.
        
        Args:
            phone_number: Número que respondeu
            message: Texto da resposta
            timestamp: Data/hora (opcional)
            
        Returns:
            True se adicionou com sucesso
        """
        session = self.get_session(phone_number)
        
        if not session:
            logger.warning(f"⚠️  Nenhuma sessão ativa para {phone_number}")
            return False
        
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Adiciona ao CSV da sessão
        csv_path = os.path.join(self.sessions_dir, session.csv_filename)
        
        try:
            with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, phone_number, message, session.session_id])
            
            # Atualiza contador
            session.responses_received += 1
            
            # Verifica se completou
            if session.responses_received >= session.total_messages_sent:
                session.status = 'completed'
                logger.info(f"✅ Sessão {session.session_id} COMPLETA!")
            
            logger.info(f"💾 Resposta {session.responses_received}/{session.total_messages_sent} salva em {session.csv_filename}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resposta: {e}")
            return False
    
    def get_session_progress(self, phone_number: str) -> Dict:
        """
        Retorna progresso da sessão.
        
        Args:
            phone_number: Número de telefone
            
        Returns:
            Dicionário com progresso
        """
        session = self.get_session(phone_number)
        
        if not session:
            return {
                "exists": False,
                "message": "Nenhuma sessão ativa"
            }
        
        progress_percent = 0
        if session.total_messages_sent > 0:
            progress_percent = int((session.responses_received / session.total_messages_sent) * 100)
        
        return {
            "exists": True,
            "session_id": session.session_id,
            "phone_number": session.phone_number,
            "total_messages": session.total_messages_sent,
            "responses_received": session.responses_received,
            "progress_percent": progress_percent,
            "status": session.status,
            "is_completed": session.status == 'completed',
            "csv_filename": session.csv_filename,
            "started_at": session.started_at
        }
    
    def close_session(self, phone_number: str) -> Optional[str]:
        """
        Fecha sessão e retorna caminho do CSV.
        
        Args:
            phone_number: Número de telefone
            
        Returns:
            Caminho do CSV ou None
        """
        session = self.active_sessions.pop(phone_number, None)
        
        if session:
            session.status = 'completed'
            csv_path = os.path.join(self.sessions_dir, session.csv_filename)
            logger.info(f"🔒 Sessão fechada: {session.session_id}")
            return csv_path
        
        return None
    
    def list_all_sessions(self) -> List[Dict]:
        """
        Lista todas as sessões (ativas e arquivadas).
        
        Returns:
            Lista de dicionários com informações das sessões
        """
        sessions = []
        
        # Adiciona sessões ativas
        for session in self.active_sessions.values():
            sessions.append(session.to_dict())
        
        # Lista CSVs no diretório
        if os.path.exists(self.sessions_dir):
            for filename in os.listdir(self.sessions_dir):
                if filename.endswith('.csv'):
                    filepath = os.path.join(self.sessions_dir, filename)
                    
                    # Conta linhas (respostas)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            line_count = sum(1 for _ in f) - 1  # -1 para cabeçalho
                        
                        # Extrai info do nome do arquivo
                        # Formato: respostas_5519993388617_20260404_123045.csv
                        parts = filename.replace('respostas_', '').replace('.csv', '').split('_')
                        
                        if len(parts) >= 3:
                            phone = parts[0]
                            date = parts[1]
                            time = parts[2]
                            
                            sessions.append({
                                'session_id': f"{phone}_{date}_{time}",
                                'phone_number': f"+{phone}",
                                'responses_received': line_count,
                                'csv_filename': filename,
                                'status': 'archived',
                                'created_at': f"{date[:4]}-{date[4:6]}-{date[6:8]} {time[:2]}:{time[2:4]}:{time[4:6]}"
                            })
                    except Exception as e:
                        logger.error(f"Erro ao processar {filename}: {e}")
        
        return sessions
    
    def get_active_sessions_count(self) -> int:
        """Retorna número de sessões ativas."""
        return len(self.active_sessions)


# Instância global
session_manager = SessionManager()
