#!/usr/bin/env python3
"""
Webhook Distribuidor - Recebe da Evolution e distribui para múltiplos destinos
"""

import json
import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import threading
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Carrega configurações do .env
def load_env():
    """Carrega variáveis do arquivo .env"""
    env_path = Path(__file__).parent / '.env'
    env_vars = {}
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars

env = load_env()

# Configuração dos destinos (do .env)
N8N_WEBHOOK = env.get('WEBHOOK_RECEPTION_URL', 'https://webhook.etechats.com.br/webhook/TESTE01')
PYTHON_PORT = env.get('WEBHOOK_PORT', '8000')

DESTINATIONS = [
    {
        "name": "N8N",
        "url": N8N_WEBHOOK,
        "enabled": True
    },
    {
        "name": "Python Local",
        "url": f"http://localhost:{PYTHON_PORT}/webhook/evolution/messages",
        "enabled": True
    }
]


class DistributorHandler(BaseHTTPRequestHandler):
    """Handler que distribui webhooks para múltiplos destinos."""
    
    def do_POST(self):
        """Recebe webhook e distribui para todos os destinos."""
        
        if self.path == '/webhook/distributor':
            try:
                # Lê o payload
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                logger.info("📨 Webhook recebido da Evolution API")
                
                # Parse para validar JSON
                try:
                    payload = json.loads(post_data.decode('utf-8'))
                    logger.info(f"   Evento: {payload.get('event', 'unknown')}")
                except:
                    logger.warning("   Payload não é JSON válido")
                
                # Distribui para todos os destinos em paralelo
                threads = []
                for dest in DESTINATIONS:
                    if dest["enabled"]:
                        thread = threading.Thread(
                            target=self.forward_to_destination,
                            args=(dest, post_data)
                        )
                        thread.start()
                        threads.append(thread)
                
                # Aguarda todos terminarem (com timeout)
                for thread in threads:
                    thread.join(timeout=5)
                
                # Responde sucesso
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "Webhook distribuído",
                    "destinations": len([d for d in DESTINATIONS if d["enabled"]])
                }).encode())
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar webhook: {e}")
                self.send_error(500, str(e))
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "healthy",
                "destinations": DESTINATIONS
            }).encode())
        
        else:
            self.send_error(404)
    
    def do_GET(self):
        """Health check e status."""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "healthy",
                "service": "Webhook Distributor",
                "destinations": DESTINATIONS
            }).encode())
        else:
            self.send_error(404)
    
    def forward_to_destination(self, destination, payload):
        """Encaminha payload para um destino específico."""
        try:
            logger.info(f"   → Enviando para {destination['name']}...")
            
            req = Request(
                destination["url"],
                data=payload,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urlopen(req, timeout=10) as response:
                if response.status in [200, 201]:
                    logger.info(f"   ✅ {destination['name']}: OK")
                else:
                    logger.warning(f"   ⚠️ {destination['name']}: Status {response.status}")
                    
        except HTTPError as e:
            logger.error(f"   ❌ {destination['name']}: HTTP {e.code}")
        except URLError as e:
            logger.error(f"   ❌ {destination['name']}: {e.reason}")
        except Exception as e:
            logger.error(f"   ❌ {destination['name']}: {e}")
    
    def log_message(self, format, *args):
        """Suprime logs desnecessários."""
        pass


def start_distributor(host='0.0.0.0', port=9000):
    """Inicia o servidor distribuidor."""
    server = HTTPServer((host, port), DistributorHandler)
    
    print("=" * 70)
    print("🔀 WEBHOOK DISTRIBUTOR - INICIADO")
    print("=" * 70)
    print()
    print(f"📍 Servidor rodando em: http://{host}:{port}")
    print(f"📥 Endpoint webhook: http://{host}:{port}/webhook/distributor")
    print()
    print("📤 Destinos configurados:")
    for i, dest in enumerate(DESTINATIONS, 1):
        status = "✅ Ativo" if dest["enabled"] else "❌ Desativado"
        print(f"   {i}. {dest['name']}: {dest['url']} - {status}")
    print()
    print("💡 Configure este webhook na Evolution API:")
    print(f"   URL: http://seu-servidor:{port}/webhook/distributor")
    print()
    print("🔍 Health check: http://localhost:{port}/health")
    print("=" * 70)
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado")
        server.shutdown()


if __name__ == "__main__":
    start_distributor()
