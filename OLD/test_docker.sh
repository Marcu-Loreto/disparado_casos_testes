#!/bin/bash

# ========================================
# TESTE DO DOCKER - WHATSAPP SENDER
# ========================================

set -e  # Para na primeira falha

echo "🐳 TESTE DO DOCKER - WHATSAPP MESSAGE SENDER"
echo "=============================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para mensagens de sucesso
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Função para mensagens de erro
error() {
    echo -e "${RED}❌ $1${NC}"
}

# Função para mensagens de aviso
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Função para mensagens de info
info() {
    echo -e "ℹ️  $1"
}

# 1. Verificar se Docker está instalado
echo "1️⃣  Verificando Docker..."
if ! command -v docker &> /dev/null; then
    error "Docker não está instalado!"
    exit 1
fi
success "Docker instalado: $(docker --version)"
echo ""

# 2. Verificar se Docker Compose está instalado
echo "2️⃣  Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    error "Docker Compose não está instalado!"
    exit 1
fi
success "Docker Compose instalado"
echo ""

# 3. Verificar se .env existe
echo "3️⃣  Verificando arquivo .env..."
if [ ! -f .env ]; then
    error "Arquivo .env não encontrado!"
    warning "Copie .env.example para .env e configure suas credenciais"
    exit 1
fi
success "Arquivo .env encontrado"
echo ""

# 4. Parar containers existentes
echo "4️⃣  Parando containers existentes..."
docker-compose down 2>/dev/null || true
success "Containers parados"
echo ""

# 5. Build da imagem
echo "5️⃣  Construindo imagem Docker..."
if docker-compose build --no-cache; then
    success "Imagem construída com sucesso"
else
    error "Falha ao construir imagem"
    exit 1
fi
echo ""

# 6. Iniciar containers
echo "6️⃣  Iniciando containers..."
if docker-compose up -d; then
    success "Containers iniciados"
else
    error "Falha ao iniciar containers"
    exit 1
fi
echo ""

# 7. Aguardar containers ficarem prontos
echo "7️⃣  Aguardando containers ficarem prontos..."
sleep 10
success "Containers prontos"
echo ""

# 8. Verificar status dos containers
echo "8️⃣  Verificando status dos containers..."
if docker-compose ps | grep -q "Up"; then
    success "Containers rodando"
    docker-compose ps
else
    error "Containers não estão rodando"
    docker-compose logs
    exit 1
fi
echo ""

# 9. Testar health check da API
echo "9️⃣  Testando health check da API..."
sleep 5
if curl -f http://localhost:8000/health &> /dev/null; then
    success "API respondendo no health check"
else
    error "API não está respondendo"
    warning "Verificando logs..."
    docker-compose logs whatsapp-api
    exit 1
fi
echo ""

# 10. Testar endpoint principal da API
echo "🔟 Testando endpoint principal da API..."
API_RESPONSE=$(curl -s http://localhost:8000/)
if echo "$API_RESPONSE" | grep -q "WhatsApp"; then
    success "API respondendo corretamente"
    info "Resposta: $API_RESPONSE"
else
    error "API não está respondendo corretamente"
    exit 1
fi
echo ""

# 11. Testar interface web
echo "1️⃣1️⃣  Testando interface web..."
if curl -f http://localhost:8080/whatsapp_simple.html &> /dev/null; then
    success "Interface web acessível"
else
    error "Interface web não está acessível"
    exit 1
fi
echo ""

# 12. Verificar logs
echo "1️⃣2️⃣  Verificando logs (últimas 10 linhas)..."
echo "--- Logs API ---"
docker-compose logs --tail=10 whatsapp-api
echo ""
echo "--- Logs Web ---"
docker-compose logs --tail=10 whatsapp-web
echo ""

# 13. Teste de envio (opcional - comentado por padrão)
# echo "1️⃣3️⃣  Testando envio de mensagem..."
# TEST_PAYLOAD='{"phone_number":"+556132073332","text_list":"🧪 Teste Docker\n✅ Sistema funcionando"}'
# SEND_RESPONSE=$(curl -s -X POST http://localhost:8000/webhook/tela2 \
#   -H "Content-Type: application/json" \
#   -d "$TEST_PAYLOAD")
# if echo "$SEND_RESPONSE" | grep -q "success"; then
#     success "Teste de envio bem-sucedido"
#     info "Resposta: $SEND_RESPONSE"
# else
#     warning "Teste de envio falhou (verifique credenciais no .env)"
#     info "Resposta: $SEND_RESPONSE"
# fi
# echo ""

# Resumo final
echo "=============================================="
echo "🎉 TODOS OS TESTES PASSARAM!"
echo "=============================================="
echo ""
success "Sistema está funcionando corretamente!"
echo ""
info "URLs disponíveis:"
echo "  📡 API WhatsApp: http://localhost:8000"
echo "  🌐 Interface Web: http://localhost:8080/whatsapp_simple.html"
echo "  ❤️  Health Check: http://localhost:8000/health"
echo ""
info "Comandos úteis:"
echo "  Ver logs: docker-compose logs -f"
echo "  Parar: docker-compose down"
echo "  Reiniciar: docker-compose restart"
echo "  Status: docker-compose ps"
echo ""
warning "Para parar os containers, execute: docker-compose down"
echo ""
