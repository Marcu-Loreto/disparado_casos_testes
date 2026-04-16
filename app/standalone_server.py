#!/usr/bin/env python3
"""
Servidor standalone usando apenas bibliotecas padrão do Python.
"""

import json
import logging
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from config.settings import Settings
from app.response_receiver import response_receiver
from app.google_sheets_handler import GoogleSheetsHandler
from app.database import db_handler
from app.session_manager import session_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global settings
settings = Settings()
sheets_handler = GoogleSheetsHandler()


class StandaloneHandler(BaseHTTPRequestHandler):
    """Handler para requisições HTTP usando apenas bibliotecas padrão."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self.send_json_response({"status": "healthy", "timestamp": "2026-04-01"})
        elif self.path == '/':
            response = {
                "message": "WhatsApp Message Dispatcher - Standalone",
                "version": "1.0.0",
                "status": "running",
                "endpoints": {
                    "send_webhook": "/webhook/tela2",
                    "receive_webhook": "/webhook/evolution/messages",
                    "active_numbers": "/active-numbers",
                    "view_responses": "/responses",
                    "health": "/health"
                }
            }
            self.send_json_response(response)
        elif self.path == '/active-numbers':
            # Retorna números ativos aguardando respostas
            active = response_receiver.get_active_numbers()
            self.send_json_response({
                "status": "success",
                "active_numbers": active,
                "count": len(active)
            })
        elif self.path == '/responses':
            # Retorna todas as respostas salvas
            try:
                responses = sheets_handler.get_all_responses_csv()
                stats = db_handler.get_statistics()
                
                self.send_json_response({
                    "status": "success",
                    "responses": responses,
                    "count": len(responses),
                    "storage": "sqlite",
                    "statistics": stats
                })
            except Exception as e:
                self.send_json_response({
                    "status": "error",
                    "error": str(e)
                }, status_code=500)
        
        elif self.path == '/export':
            # Exporta respostas para CSV com timestamp
            try:
                result = db_handler.export_to_csv()
                self.send_json_response(result)
            except Exception as e:
                self.send_json_response({
                    "status": "error",
                    "error": str(e)
                }, status_code=500)
        
        elif self.path == '/export-history':
            # Retorna histórico de exportações
            try:
                history = db_handler.get_export_history()
                self.send_json_response({
                    "status": "success",
                    "exports": history,
                    "count": len(history)
                })
            except Exception as e:
                self.send_json_response({
                    "status": "error",
                    "error": str(e)
                }, status_code=500)
        
        elif self.path.startswith('/session/'):
            # Informações de sessão específica
            try:
                phone = self.path.split('/')[-1]
                progress = session_manager.get_session_progress(phone)
                self.send_json_response(progress)
            except Exception as e:
                self.send_json_response({
                    "status": "error",
                    "error": str(e)
                }, status_code=500)
        
        elif self.path == '/sessions':
            # Lista todas as sessões
            try:
                sessions = session_manager.list_all_sessions()
                self.send_json_response({
                    "status": "success",
                    "sessions": sessions,
                    "count": len(sessions),
                    "active_count": session_manager.get_active_sessions_count()
                })
            except Exception as e:
                self.send_json_response({
                    "status": "error",
                    "error": str(e)
                }, status_code=500)
        
        elif self.path.startswith('/download/'):
            # Download de arquivo CSV exportado
            try:
                filename = self.path.split('/')[-1]
                
                # Tenta em exports/ primeiro, depois sessions/
                filepath = None
                if os.path.exists(os.path.join('exports', filename)):
                    filepath = os.path.join('exports', filename)
                elif os.path.exists(os.path.join('sessions', filename)):
                    filepath = os.path.join('sessions', filename)
                
                if filepath and os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        content = f.read()
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/csv')
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_error(404, "Arquivo não encontrado")
            except Exception as e:
                self.send_error(500, str(e))
        
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/webhook/tela2':
            try:
                # Lê o corpo da requisição
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON
                payload = json.loads(post_data.decode('utf-8'))
                logger.info(f"Webhook recebido com {len(str(payload))} caracteres")
                
                # Processa o payload
                processed_data = self.process_webhook_payload(payload)
                
                # Registra número para receber respostas
                response_receiver.register_number(processed_data["phone_number"])
                
                # Cria sessão de envio
                session = session_manager.create_session(
                    phone_number=processed_data["phone_number"],
                    total_messages=len(processed_data["messages"])
                )
                
                # Envia mensagens
                results = self.send_messages_batch(
                    phone_number=processed_data["phone_number"],
                    messages=processed_data["messages"]
                )
                
                # Conta sucessos
                sent_count = sum(1 for r in results if r.get("status") == "sent")
                
                response = {
                    "status": "success",
                    "message": f"{sent_count} mensagens enviadas com sucesso",
                    "total_messages": len(results),
                    "sent_messages": sent_count,
                    "phone_number": processed_data["phone_number"],
                    "session_id": session.session_id,
                    "csv_filename": session.csv_filename,
                    "results": results[:5]  # Limita resposta para não sobrecarregar
                }
                
                self.send_json_response(response)
                
            except Exception as e:
                logger.error(f"Erro no webhook: {e}")
                error_response = {"error": str(e), "status": "error"}
                self.send_json_response(error_response, status_code=400)
        
        elif self.path == '/webhook/evolution/messages':
            # Webhook para receber mensagens da Evolution API
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                payload = json.loads(post_data.decode('utf-8'))
                logger.info(f"Mensagem recebida da Evolution API")
                
                # Extrai dados brutos mesmo sem número ativo registrado
                data = payload.get("data", {})
                
                # Ignora mensagens enviadas por nós
                if data.get("key", {}).get("fromMe"):
                    self.send_json_response({"status": "ignored", "message": "Mensagem própria ignorada"})
                    return
                
                remote_jid = data.get("key", {}).get("remoteJid", "")
                message_obj = data.get("message", {})
                message_text = (
                    message_obj.get("conversation") or
                    message_obj.get("extendedTextMessage", {}).get("text") or
                    message_obj.get("imageMessage", {}).get("caption") or
                    message_obj.get("videoMessage", {}).get("caption") or
                    ""
                ).strip()
                
                ts = data.get("messageTimestamp", None)
                if ts:
                    from datetime import datetime as dt
                    timestamp = dt.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                phone_number = remote_jid.split("@")[0] if remote_jid else ""
                
                if not phone_number or not message_text:
                    self.send_json_response({"status": "ignored", "message": "Sem número ou texto"})
                    return
                
                # Salva SEMPRE no banco SQLite, independente de número ativo
                result = sheets_handler.save_response(
                    phone_number=phone_number,
                    message=message_text,
                    timestamp=timestamp
                )
                
                # Tenta adicionar à sessão ativa (se existir)
                session_added = session_manager.add_response(
                    phone_number=phone_number,
                    message=message_text,
                    timestamp=timestamp
                )
                
                logger.info(f"✅ Resposta salva: {phone_number} | session={session_added}")
                
                self.send_json_response({
                    "status": "success",
                    "message": "Resposta salva no banco de dados",
                    "phone_number": phone_number,
                    "saved_to_db": result.get("success", False),
                    "session_added": session_added
                })
                
            except Exception as e:
                logger.error(f"Erro ao processar mensagem recebida: {e}")
                error_response = {"error": str(e), "status": "error"}
                self.send_json_response(error_response, status_code=400)
        
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_json_response(self, data, status_code=200):
        """Envia resposta JSON."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def process_webhook_payload(self, payload):
        """Processa diferentes tipos de payload."""
        
        # Extrai número de telefone
        phone_number = (
            payload.get("phone_number") or 
            payload.get("chatbotPhone") or
            payload.get("body", {}).get("chatbotPhone")
        )
        
        if not phone_number:
            raise ValueError("Número de telefone é obrigatório")
        
        # Extrai delay customizado (padrão: 2 segundos)
        custom_delay = payload.get("delay", 2)
        
        messages = []
        
        # Formato JSON estruturado
        if "messages" in payload and isinstance(payload["messages"], list):
            for msg in payload["messages"]:
                if isinstance(msg, str):
                    messages.append({"text": msg, "delay": custom_delay})
                elif isinstance(msg, dict):
                    messages.append({
                        "text": msg.get("text", ""),
                        "delay": msg.get("delay", custom_delay)
                    })
        
        # Texto colado
        elif "text_list" in payload:
            lines = payload["text_list"].strip().split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    messages.append({"text": line, "delay": custom_delay})
        
        # Formato legado N8N
        elif "body" in payload and "testCases" in payload["body"]:
            test_cases = payload["body"]["testCases"]
            for case in test_cases:
                messages.append({"text": case, "delay": custom_delay})
        
        # Lista simples de strings
        elif "testCases" in payload:
            for case in payload["testCases"]:
                messages.append({"text": case, "delay": custom_delay})
        
        else:
            raise ValueError("Formato de payload não reconhecido")
        
        if not messages:
            raise ValueError("Nenhuma mensagem encontrada no payload")
        
        if len(messages) > 1000:
            raise ValueError("Máximo de 1000 mensagens por lote")
        
        return {
            "phone_number": phone_number,
            "messages": messages
        }
    
    def send_messages_batch(self, phone_number, messages):
        """Envia lote de mensagens usando urllib."""
        results = []
        
        logger.info(f"Iniciando envio de {len(messages)} mensagens para {phone_number}")
        
        for i, message in enumerate(messages):
            try:
                # Envia mensagem individual
                result = self.send_single_message(phone_number, message["text"])
                
                results.append({
                    "index": i,
                    "text": message["text"],
                    "status": "sent" if result.get("success") else "failed",
                    "result": result,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
                logger.info(f"Mensagem {i+1}/{len(messages)} enviada")
                
                # Aplica delay
                if i < len(messages) - 1:
                    delay = message.get("delay", 2)
                    time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Erro ao enviar mensagem {i+1}: {e}")
                results.append({
                    "index": i,
                    "text": message["text"],
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        sent_count = sum(1 for r in results if r["status"] == "sent")
        logger.info(f"Envio concluído: {sent_count}/{len(messages)} mensagens enviadas")
        
        return results
    
    def send_single_message(self, phone_number, text):
        """Envia uma única mensagem via WhatsApp usando urllib."""
        
        url = f"{settings.EVOLUTION_API_URL}/message/sendText/{settings.EVOLUTION_INSTANCE}"
        
        # Remove + do número (Evolution não aceita +55, só 5519...)
        clean_number = phone_number.lstrip('+')

        payload = {
            "number": clean_number,
            "text": text
        }
        
        headers = {
            "apikey": settings.EVOLUTION_API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            # Prepara requisição
            data = json.dumps(payload).encode('utf-8')
            req = Request(url, data=data, headers=headers, method='POST')
            
            # Faz requisição
            with urlopen(req, timeout=30) as response:
                response_data = response.read().decode('utf-8')
                
                if response.status in [200, 201]:
                    try:
                        result = json.loads(response_data)
                        return {
                            "success": True,
                            "status": "sent",
                            "response": result,
                            "message_id": result.get("key", {}).get("id")
                        }
                    except:
                        return {
                            "success": True,
                            "status": "sent",
                            "response": response_data
                        }
                else:
                    return {
                        "success": False,
                        "status": "failed",
                        "error": f"HTTP {response.status}: {response_data}"
                    }
                    
        except HTTPError as e:
            return {
                "success": False,
                "status": "failed",
                "error": f"HTTP Error {e.code}: {e.reason}"
            }
        except URLError as e:
            return {
                "success": False,
                "status": "failed",
                "error": f"URL Error: {e.reason}"
            }
        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "error": str(e)
            }
    
    def log_message(self, format, *args):
        """Suprime logs desnecessários."""
        message = format % args
        if "GET /health" not in message and "favicon.ico" not in message:
            logger.info(message)


def start_server():
    """Inicia o servidor standalone."""
    host = settings.WEBHOOK_HOST
    port = settings.WEBHOOK_PORT
    
    server = HTTPServer((host, port), StandaloneHandler)
    
    logger.info(f"🚀 Servidor standalone iniciado em {host}:{port}")
    logger.info(f"📤 Webhook ENVIO: http://{host}:{port}/webhook/tela2")
    logger.info(f"📥 Webhook RECEBIMENTO: http://{host}:{port}/webhook/evolution/messages")
    logger.info(f"📊 Números ativos: http://{host}:{port}/active-numbers")
    logger.info(f"🔧 Evolution API: {settings.EVOLUTION_API_URL}")
    logger.info(f"📞 Instância: {settings.EVOLUTION_INSTANCE}")
    logger.info(f"📋 Google Sheets: {settings.GOOGLE_SHEETS_DOCUMENT_ID}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("🛑 Servidor parado pelo usuário")
        server.shutdown()


if __name__ == "__main__":
    start_server()