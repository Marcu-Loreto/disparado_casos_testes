#!/usr/bin/env python3
"""
Wrapper para iniciar o servidor standalone
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa e executa o servidor
from app.standalone_server import start_server

if __name__ == "__main__":
    start_server()
