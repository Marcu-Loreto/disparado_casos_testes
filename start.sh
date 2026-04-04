#!/bin/bash

# Script para iniciar o WhatsApp Message Dispatcher
# Uso: ./start.sh

echo "📱 WHATSAPP MESSAGE DISPATCHER"
echo "=============================="
echo "🚀 Iniciando sistema..."
echo ""

# Verifica se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale o Python3 primeiro."
    exit 1
fi

# Verifica se os arquivos existem
if [ ! -f "app/simple_webhook_server.py" ]; then
    echo "❌ Arquivo app/simple_webhook_server.py não encontrado"
    exit 1
fi

if [ ! -f "whatsapp_sender_page.html" ]; then
    echo "❌ Arquivo whatsapp_sender_page.html não encontrado"
    exit 1
fi

echo "✅ Arquivos verificados"

# Inicia o servidor webhook em background
echo "🚀 Iniciando servidor webhook..."
python3 -m app.simple_webhook_server &
WEBHOOK_PID=$!

# Aguarda um pouco
sleep 3

# Inicia o servidor web em background
echo "🌐 Iniciando servidor web..."
python3 -m http.server 8080 &
WEB_PID=$!

# Aguarda um pouco
sleep 2

echo ""
echo "✅ SISTEMA INICIADO COM SUCESSO!"
echo ""
echo "📡 API Webhook: http://localhost:8000"
echo "🌍 Interface Web: http://localhost:8080/whatsapp_sender_page.html"
echo ""
echo "📋 COMO USAR:"
echo "1. Abra: http://localhost:8080/whatsapp_sender_page.html"
echo "2. Informe o número do WhatsApp"
echo "3. Cole suas mensagens ou faça upload de arquivo"
echo "4. Clique em 'Enviar Mensagens'"
echo ""
echo "⚠️  Para parar o sistema, pressione Ctrl+C"
echo ""

# Função para limpar processos ao sair
cleanup() {
    echo ""
    echo "🛑 Parando sistema..."
    kill $WEBHOOK_PID 2>/dev/null
    kill $WEB_PID 2>/dev/null
    echo "✅ Sistema parado com sucesso!"
    exit 0
}

# Captura Ctrl+C
trap cleanup SIGINT

# Mantém o script rodando
while true; do
    sleep 1
done