#!/bin/bash

echo "🛑 Parando sistema WhatsApp..."
echo ""

# Mata processos por porta
for port in 9000 8004 8084; do
    pids=$(lsof -ti :$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo "   Parando serviço na porta $port..."
        kill -9 $pids 2>/dev/null
    fi
done

# Mata processos salvos
if [ -f /tmp/whatsapp_pids.txt ]; then
    pids=$(cat /tmp/whatsapp_pids.txt)
    if [ ! -z "$pids" ]; then
        echo "   Parando processos salvos..."
        kill -9 $pids 2>/dev/null
    fi
    rm /tmp/whatsapp_pids.txt
fi

echo ""
echo "✅ Sistema parado"
