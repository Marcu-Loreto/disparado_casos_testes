# 🚀 GUIA RÁPIDO DE DEPLOY

## 📋 Escolha Sua Plataforma

| Plataforma       | Dificuldade    | Tempo  | Custo    | Arquivo               |
| ---------------- | -------------- | ------ | -------- | --------------------- |
| **Docker Local** | ⭐ Fácil       | 5 min  | Grátis   | `docker-compose.yml`  |
| **Portainer**    | ⭐⭐ Médio     | 10 min | Grátis   | `portainer-stack.yml` |
| **EasyPanel**    | ⭐ Fácil       | 5 min  | ~$10/mês | `easypanel.yml`       |
| **VPS Manual**   | ⭐⭐⭐ Difícil | 30 min | ~$5/mês  | `docker-compose.yml`  |

---

## 🐳 DOCKER LOCAL

### Comandos Rápidos:

```bash
# 1. Configurar
cp .env.example .env
nano .env  # Preencha EVOLUTION_API_KEY

# 2. Iniciar
docker-compose up -d

# 3. Testar
./test_docker.sh

# 4. Acessar
# API: http://localhost:8000
# Web: http://localhost:8080/whatsapp_simple.html
```

**Documentação completa**: `DOCKER_DEPLOY.md`

---

## 🎛️ PORTAINER

### Passo a Passo:

1. **Acesse Portainer** → Stacks → Add stack
2. **Nome**: `whatsapp-sender`
3. **Upload**: `portainer-stack.yml`
4. **Environment variables**:
   ```
   EVOLUTION_API_KEY=sua_chave_aqui
   EVOLUTION_INSTANCE=TESTE_AUTO_MGI
   ```
5. **Deploy the stack**

**URLs após deploy**:

- API: `http://seu-servidor:8000`
- Web: `http://seu-servidor:8080`

**Documentação completa**: `PORTAINER_INSTALL.md`

---

## 🚀 EASYPANEL

### Passo a Passo:

1. **Acesse EasyPanel** → New Service → GitHub
2. **Repositório**: `Marcu-Loreto/disparado_casos_testes`
3. **Branch**: `main`
4. **Build Method**: `Dockerfile`
5. **Port**: `8000`
6. **Environment Variables**:
   ```
   EVOLUTION_API_KEY=sua_chave_aqui
   EVOLUTION_INSTANCE=TESTE_AUTO_MGI
   ```
7. **Deploy**

**URLs após deploy**:

- API: `https://whatsapp-sender-xxx.easypanel.app`
- Health: `https://whatsapp-sender-xxx.easypanel.app/health`

**Documentação completa**: `EASYPANEL_INSTALL.md`

---

## 🖥️ VPS MANUAL (Ubuntu/Debian)

### Comandos Rápidos:

```bash
# 1. Conectar ao servidor
ssh user@seu-servidor.com

# 2. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clonar repositório
git clone https://github.com/Marcu-Loreto/disparado_casos_testes.git
cd disparado_casos_testes

# 5. Configurar
cp .env.example .env
nano .env  # Preencha credenciais

# 6. Iniciar
docker-compose up -d

# 7. Verificar
docker-compose ps
curl http://localhost:8000/health
```

**Documentação completa**: `DOCKER_DEPLOY.md`

---

## ⚙️ VARIÁVEIS DE AMBIENTE OBRIGATÓRIAS

Todas as plataformas precisam destas variáveis:

```env
# OBRIGATÓRIO
EVOLUTION_API_URL=https://evolution.etechats.com.br
EVOLUTION_API_KEY=sua_chave_api_aqui
EVOLUTION_INSTANCE=TESTE_AUTO_MGI

# OPCIONAL
LOG_LEVEL=INFO
ENVIRONMENT=production
GOOGLE_SHEETS_DOCUMENT_ID=
GITHUB_TOKEN=
```

### Como obter EVOLUTION_API_KEY:

1. Acesse seu painel Evolution API
2. Vá em **Configurações** → **API Key**
3. Copie a chave
4. Cole na variável `EVOLUTION_API_KEY`

---

## 🧪 TESTES APÓS DEPLOY

### 1. Health Check

```bash
curl http://seu-servidor:8000/health
```

✅ Resposta esperada:

```json
{ "status": "healthy", "timestamp": "2026-04-04" }
```

### 2. Endpoint Principal

```bash
curl http://seu-servidor:8000/
```

✅ Resposta esperada:

```json
{
  "message": "WhatsApp Message Dispatcher - Standalone",
  "version": "1.0.0",
  "status": "running"
}
```

### 3. Teste de Envio

```bash
curl -X POST http://seu-servidor:8000/webhook/tela2 \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+5561999999999",
    "text_list": "Teste 1\nTeste 2\nTeste 3"
  }'
```

✅ Resposta esperada:

```json
{
  "status": "success",
  "message": "3 mensagens enviadas com sucesso",
  "total_messages": 3,
  "sent_messages": 3
}
```

---

## 🐛 TROUBLESHOOTING RÁPIDO

### Container não inicia

```bash
# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Rebuild
docker-compose down
docker-compose up -d --build
```

### API não responde

```bash
# Verificar se está rodando
docker-compose ps

# Verificar porta
sudo lsof -i :8000

# Testar localmente
curl http://localhost:8000/health
```

### Erro de credenciais

```bash
# Verificar .env
cat .env

# Recarregar variáveis
docker-compose down
docker-compose up -d
```

---

## 📊 MONITORAMENTO

### Ver Logs

```bash
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f whatsapp-api

# Últimas 100 linhas
docker-compose logs --tail=100
```

### Ver Status

```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats

# Health check
docker inspect --format='{{.State.Health.Status}}' whatsapp-sender-api
```

---

## 🔄 ATUALIZAÇÃO

### Docker Local / VPS

```bash
# 1. Baixar atualizações
git pull origin main

# 2. Rebuild
docker-compose down
docker-compose up -d --build

# 3. Verificar
docker-compose ps
```

### Portainer

1. Vá em **Stacks** → **whatsapp-sender**
2. Clique em **Editor**
3. Clique em **Update the stack**
4. Marque **"Re-pull image and redeploy"**

### EasyPanel

1. Push no GitHub (se auto-deploy ativo)
2. Ou clique em **"Redeploy"** no EasyPanel

---

## 🛑 PARAR SISTEMA

### Docker Local / VPS

```bash
# Parar containers
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Parar e remover tudo
docker-compose down -v --rmi all
```

### Portainer

1. Vá em **Stacks** → **whatsapp-sender**
2. Clique em **"Stop this stack"**

### EasyPanel

1. Vá no serviço
2. Clique em **"Stop"**

---

## 📞 URLS IMPORTANTES

### Documentação

- **README Principal**: `README.md`
- **Guia do Usuário**: `README_USUARIO.md`
- **Docker**: `DOCKER_DEPLOY.md`
- **Portainer**: `PORTAINER_INSTALL.md`
- **EasyPanel**: `EASYPANEL_INSTALL.md`

### Arquivos de Configuração

- **Docker Compose**: `docker-compose.yml`
- **Portainer Stack**: `portainer-stack.yml`
- **EasyPanel**: `easypanel.yml`
- **Dockerfile**: `Dockerfile`
- **Env Example**: `.env.example`

### Scripts

- **Iniciar Local**: `START.py`
- **Testar Docker**: `test_docker.sh`

---

## 🎯 CHECKLIST GERAL

- [ ] Plataforma escolhida
- [ ] Docker instalado (se necessário)
- [ ] Repositório clonado (se necessário)
- [ ] Arquivo `.env` configurado
- [ ] `EVOLUTION_API_KEY` preenchida
- [ ] Deploy executado
- [ ] Containers rodando
- [ ] Health check OK
- [ ] Logs sem erros
- [ ] Teste de envio bem-sucedido
- [ ] URLs acessíveis
- [ ] Monitoramento configurado

---

## 🎉 PRONTO!

Escolha sua plataforma e siga o guia correspondente!

**Dúvidas?** Consulte a documentação completa de cada plataforma.
