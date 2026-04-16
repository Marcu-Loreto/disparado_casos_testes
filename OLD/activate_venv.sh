#!/bin/bash

# ========================================
# ATIVAR AMBIENTE VIRTUAL
# ========================================

echo "🐍 Ativando ambiente virtual..."
echo ""

# Verifica se venv existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
    echo ""
fi

# Ativa o ambiente virtual
source venv/bin/activate

# Verifica se ativou
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Ambiente virtual ativado com sucesso!"
    echo ""
    echo "📍 Localização: $VIRTUAL_ENV"
    echo "🐍 Python: $(which python3)"
    echo "📦 Versão: $(python3 --version)"
    echo ""
    echo "💡 Para desativar, execute: deactivate"
    echo ""
else
    echo "❌ Falha ao ativar ambiente virtual"
    exit 1
fi

# Mantém o shell ativo com venv
exec bash --rcfile <(echo ". ~/.bashrc; PS1='(venv) \u@\h:\w\$ '")
