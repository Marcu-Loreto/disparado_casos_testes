#!/bin/bash

echo "======================================================================="
echo "🚀 INICIANDO SISTEMA WHATSAPP - MODO ROBUSTO"
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
    echo "   ❌ Erro ao iniciar distribuidor"
    echo "   Veja o log: tail /tmp/distribuidor.log"
    exit 1
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
    echo "   ❌ Erro ao iniciar servidor Python"
    echo "   Veja o log: tail /tmp/servidor_python.log"
    exit 1
fi
echo ""

# Inicia Interface Web
echo "4️⃣  Iniciando Interface Web (porta 8084)..."
python3 -m http.server 8084 > /tmp/interface_web.log 2>&1 &
WEB_PID=$!
sleep 1

if ps -p $WEB_PID > /dev/null; then
    echo "   ✅ Interface Web iniciada (PID: $WEB_PID)"
else
    echo "   ❌ Erro ao iniciar interface web"
    kill $DIST_PID $SERVER_PID 2>/dev/null
    exit 1
fi
echo ""

# Testa se os serviços estão respondendo
echo "5️⃣  Testando serviços..."
sleep 2

# Testa Distribuidor
if curl -s http://localhost:9000/health > /dev/null 2>&1; then
    echo "   ✅ Distribuidor respondendo"
else
    echo "   ⚠️  Distribuidor não responde"
fi

# Testa Servidor Python
if curl -s http://localhost:8004/health > /dev/null 2>&1; then
    echo "   ✅ Servidor Python respondendo"
else
    echo "   ⚠️  Servidor Python não responde"
fi

# Testa Interface Web
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
echo "   🔀 Webhook Distribuidor (PID: $DIST_PID)"
echo "      http://localhost:9000/webhook/distributor"
echo "      Health: http://localhost:9000/health"
echo ""
echo "   🐍 Servidor Python (PID: $SERVER_PID)"
echo "      http://localhost:8004"
echo "      Envio: http://localhost:8004/webhook/tela2"
echo "      Recepção: http://localhost:8004/webhook/evolution/messages"
echo ""
echo "   🌐 Interface Web (PID: $WEB_PID)"
echo "      http://localhost:8084/whatsapp_final.html"
echo ""
echo "======================================================================="
echo ""
echo "📝 Logs disponíveis em:"
echo "   - Distribuidor: tail -f /tmp/distribuidor.log"
echo "   - Servidor Python: tail -f /tmp/servidor_python.log"
echo "   - Interface Web: tail -f /tmp/interface_web.log"
echo ""
echo "🛑 Para parar todos os serviços:"
echo "   kill $DIST_PID $SERVER_PID $WEB_PID"
echo ""
echo "💡 Próximo passo:"
echo "   python3 configurar_webhook_distribuidor.py"
echo ""
echo "======================================================================="

# Salva PIDs para fácil acesso
echo "$DIST_PID $SERVER_PID $WEB_PID" > /tmp/whatsapp_pids.txt
echo ""
echo "PIDs salvos em: /tmp/whatsapp_pids.txt"
