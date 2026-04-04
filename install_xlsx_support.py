#!/usr/bin/env python3
"""
Instala suporte para arquivos XLSX
"""

import subprocess
import sys

def install_openpyxl():
    """Instala openpyxl para suporte a XLSX."""
    try:
        print("📦 Instalando suporte para XLSX...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
        print("✅ Suporte XLSX instalado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao instalar openpyxl: {e}")
        return False

if __name__ == "__main__":
    install_openpyxl()