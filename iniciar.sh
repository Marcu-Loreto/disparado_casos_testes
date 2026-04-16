#!/bin/bash

echo "======================================================================="
echo "🚀 INICIANDO SISTEMA WHATSAPP COMPLETO"
echo "======================================================================="
echo ""

# Função para matar processos em uma porta
kill_port() {
    local port=$1
    local pids=$(lsof -ti :$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo "🔧 Liberando porta $port..."
        kill -9 $pids 2>/dev/null
        sleep 1
    fi
}

# Limpa portas
echo "1️⃣  Limpando portas..."
kill_port 9000
kill_port 8004
kill_port 8084
echo "   ✅ Portas liberadas"
echo ""

# Inicia Distribuidor
echo "2️⃣  Iniciando Webhook Distribuidor (porta 9000)..."
python3 webhook_distributor.py > /tmp/distribuidor.log 2>&1 &
DIST_PID=$!
sleep 2

if ps -p $DIST_PID > /dev/null; then
    echo "   ✅ Distribuidor iniciado (PID: $DIST_PID)"
else
    echo "   ⚠️  Distribuidor não iniciou (pode ser opcional)"
    DIST_PID=""
fi
echo ""

# Inicia Servidor Python
echo "3️⃣  Iniciando Servidor Python (porta 8004)..."
python3 start_server.py > /tmp/servidor_python.log 2>&1 &
SERVER_PID=$!
sleep 3

if ps -p $SERVER_PID > /dev/null; then
    echo "   ✅ Servidor Python iniciado (PID: $SERVER_PID)"
else
    echo "   ❌ ERRO: Servidor Python não iniciou"
    echo "   Log: tail /tmp/servidor_python.log"
    [ ! -z "$DIST_PID" ] && kill $DIST_PID 2>/dev/null
    exit 1
fi
echo ""

# Inicia Interface Web
echo "4️⃣  Iniciando Interface Web (porta 8084)..."
cd "$(dirname "$0")"
python3 -m http.server 8084 > /tmp/interface_web.log 2>&1 &
WEB_PID=$!
sleep 2

if ps -p $WEB_PID > /dev/null; then
    echo "   ✅ Interface Web iniciada (PID: $WEB_PID)"
else
    echo "   ❌ ERRO: Interface Web não iniciou"
    [ ! -z "$DIST_PID" ] && kill $DIST_PID 2>/dev/null
    kill $SERVER_PID 2>/dev/null
    exit 1
fi
echo ""

# Testa serviços
echo "5️⃣  Testando serviços..."
sleep 2

if [ ! -z "$DIST_PID" ]; then
    if curl -s http://localhost:9000/health > /dev/null 2>&1; then
        echo "   ✅ Distribuidor respondendo"
    else
        echo "   ⚠️  Distribuidor não responde"
    fi
fi

if curl -s http://localhost:8004/health > /dev/null 2>&1; then
    echo "   ✅ Servidor Python respondendo"
else
    echo "   ⚠️  Servidor Python não responde"
fi

if curl -s http://localhost:8084/ > /dev/null 2>&1; then
    echo "   ✅ Interface Web respondendo"
else
    echo "   ⚠️  Interface Web não responde"
fi

echo ""
echo "======================================================================="
echo "✅ SISTEMA INICIADO COM SUCESSO"
echo "======================================================================="
echo ""
echo "📊 Serviços rodando:"
echo ""

if [ ! -z "$DIST_PID" ]; then
    echo "   🔀 Webhook Distribuidor (PID: $DIST_PID)"
    echo "      http://localhost:9000/webhook/distributor"
    echo ""
fi

echo "   🐍 Servidor Python (PID: $SERVER_PID)"
echo "      http://localhost:8004"
echo "      Envio: http://localhost:8004/webhook/tela2"
echo ""
echo "   🌐 Interface Web (PID: $WEB_PID)"
echo "      http://localhost:8084/whatsapp_final.html"
echo ""
echo "======================================================================="
echo ""
echo "🌐 ABRINDO INTERFACE NO NAVEGADOR..."
echo ""

# Abre o navegador automaticamente
if command -v xdg-open > /dev/null; then
    xdg-open "http://localhost:8084/whatsapp_final.html" 2>/dev/null &
elif command -v gnome-open > /dev/null; then
    gnome-open "http://localhost:8084/whatsapp_final.html" 2>/dev/null &
elif command -v open > /dev/null; then
    open "http://localhost:8084/whatsapp_final.html" 2>/dev/null &
else
    echo "   ⚠️  Não foi possível abrir o navegador automaticamente"
    echo "   Acesse manualmente: http://localhost:8084/whatsapp_final.html"
fi

sleep 1
echo ""
echo "======================================================================="
echo ""
echo "📝 Logs disponíveis:"
echo "   - Distribuidor: tail -f /tmp/distribuidor.log"
echo "   - Servidor Python: tail -f /tmp/servidor_python.log"
echo "   - Interface Web: tail -f /tmp/interface_web.log"
echo ""
echo "🛑 Para parar todos os serviços:"
if [ ! -z "$DIST_PID" ]; then
    echo "   kill $DIST_PID $SERVER_PID $WEB_PID"
    echo "$DIST_PID $SERVER_PID $WEB_PID" > /tmp/whatsapp_pids.txt
else
    echo "   kill $SERVER_PID $WEB_PID"
    echo "$SERVER_PID $WEB_PID" > /tmp/whatsapp_pids.txt
fi
echo "   ou execute: bash parar_sistema.sh"
echo ""
echo "======================================================================="
echo ""
echo "✨ Sistema pronto! Interface aberta no navegador."
echo ""
