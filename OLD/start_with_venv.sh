#!/bin/bash

# Script para ativar venv e iniciar o sistema
# Uso: ./start_with_venv.sh

echo "🐍 Ativando ambiente virtual..."

# Ativa o ambiente virtual
source venv/bin/activate

# Verifica se ativou corretamente
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Ambiente virtual ativado: $VIRTUAL_ENV"
else
    echo "❌ Falha ao ativar ambiente virtual"
    exit 1
fi

# Mostra versão do Python
echo "🐍 Python: $(python --version)"

# Inicia o sistema
echo "🚀 Iniciando sistema..."
python START.py

# Desativa ao sair
deactivate
echo "👋 Ambiente virtual desativado"