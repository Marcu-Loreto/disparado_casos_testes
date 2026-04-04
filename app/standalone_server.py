#!/usr/bin/env python3
"""
Servidor standalone usando apenas bibliotecas padrão do Python.
"""

import json
import logging
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global settings
settings = Settings()


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
                    "webhook": "/webhook/tela2",
                    "health": "/health"
                }
            }
            self.send_json_response(response)
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
                    "results": results[:5]  # Limita resposta para não sobrecarregar
                }
                
                self.send_json_response(response)
                
            except Exception as e:
                logger.error(f"Erro no webhook: {e}")
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
        
        payload = {
            "number": phone_number,
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
    logger.info(f"📱 Webhook URL: http://{host}:{port}/webhook/tela2")
    logger.info(f"🔧 Evolution API: {settings.EVOLUTION_API_URL}")
    logger.info(f"📞 Instância: {settings.EVOLUTION_INSTANCE}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("🛑 Servidor parado pelo usuário")
        server.shutdown()


if __name__ == "__main__":
    start_server()