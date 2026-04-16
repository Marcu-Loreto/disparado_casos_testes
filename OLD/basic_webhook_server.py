#!/usr/bin/env python3
"""
Servidor webhook básico usando apenas bibliotecas padrão do Python.
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import asyncio
from app.message_processor import WhatsAppMessageProcessor
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global settings
settings = Settings()
message_processor = WhatsAppMessageProcessor(settings)


class WebhookHandler(BaseHTTPRequestHandler):
    """Handler para requisições HTTP."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "healthy", "timestamp": "2026-04-01"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "message": "WhatsApp Message Dispatcher - Basic",
                "version": "1.0.0",
                "status": "running",
                "endpoints": {
                    "webhook": "/webhook/tela2",
                    "health": "/health"
                }
            }
            self.wfile.write(json.dumps(response).encode())
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
                logger.info(f"Webhook recebido: {payload}")
                
                # Processa o payload
                processed_data = self.process_webhook_payload(payload)
                
                # Executa o envio de mensagens de forma síncrona
                results = self.send_messages_sync(
                    phone_number=processed_data["phone_number"],
                    messages=processed_data["messages"]
                )
                
                # Conta sucessos
                sent_count = sum(1 for r in results if r["status"] == "sent")
                
                response = {
                    "status": "success",
                    "message": f"{sent_count} mensagens enviadas com sucesso",
                    "total_messages": len(results),
                    "sent_messages": sent_count,
                    "phone_number": processed_data["phone_number"],
                    "results": results
                }
                
                # Envia resposta
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                logger.error(f"Erro no webhook: {e}")
                self.send_error(400, str(e))
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
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
        
        messages = []
        
        # Formato JSON estruturado
        if "messages" in payload and isinstance(payload["messages"], list):
            for msg in payload["messages"]:
                if isinstance(msg, str):
                    messages.append({"text": msg, "delay": 2})
                elif isinstance(msg, dict):
                    messages.append({
                        "text": msg.get("text", ""),
                        "delay": msg.get("delay", 2)
                    })
        
        # Texto colado
        elif "text_list" in payload:
            lines = payload["text_list"].strip().split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    messages.append({"text": line, "delay": 2})
        
        # Formato legado N8N
        elif "body" in payload and "testCases" in payload["body"]:
            test_cases = payload["body"]["testCases"]
            for case in test_cases:
                messages.append({"text": case, "delay": 2})
        
        # Lista simples de strings
        elif "testCases" in payload:
            for case in payload["testCases"]:
                messages.append({"text": case, "delay": 2})
        
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
    
    def send_messages_sync(self, phone_number, messages):
        """Envia mensagens de forma síncrona."""
        import asyncio
        
        # Cria um novo loop para esta thread
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Executa o envio assíncrono
            results = loop.run_until_complete(
                message_processor.send_message_batch(phone_number, messages)
            )
            
            loop.close()
            return results
            
        except Exception as e:
            logger.error(f"Erro no envio síncrono: {e}")
            return [{"status": "error", "error": str(e)}]
    
    def log_message(self, format, *args):
        """Suprime logs desnecessários."""
        if "GET /health" not in format % args:
            logger.info(format % args)


def start_server():
    """Inicia o servidor webhook."""
    host = settings.WEBHOOK_HOST
    port = settings.WEBHOOK_PORT
    
    server = HTTPServer((host, port), WebhookHandler)
    
    logger.info(f"🚀 Servidor webhook básico iniciado em {host}:{port}")
    logger.info(f"📱 Webhook URL: http://{host}:{port}/webhook/tela2")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("🛑 Servidor parado pelo usuário")
        server.shutdown()


if __name__ == "__main__":
    start_server()