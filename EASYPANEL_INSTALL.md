# 🚀 INSTALAÇÃO NO EASYPANEL

## 📋 Guia Completo para Deploy no EasyPanel

EasyPanel é uma plataforma moderna de deploy com interface intuitiva. Este guia mostra como fazer deploy do WhatsApp Message Sender.

---

## 🎯 Método 1: Deploy via GitHub (Recomendado)

### Passo 1: Preparar Repositório

1. Certifique-se que o código está no GitHub:

   ```
   https://github.com/Marcu-Loreto/disparado_casos_testes.git
   ```

2. Verifique se os arquivos estão presentes:
   - ✅ `Dockerfile`
   - ✅ `docker-compose.yml`
   - ✅ `.env.example`

### Passo 2: Acessar EasyPanel

1. Acesse seu EasyPanel: `https://seu-easypanel.com`
2. Faça login
3. Selecione seu projeto ou crie um novo

### Passo 3: Criar Novo Serviço

1. Clique em **"+ New Service"**
2. Selecione **"GitHub"**
3. Conecte sua conta GitHub (se ainda não conectou)
4. Selecione o repositório: `Marcu-Loreto/disparado_casos_testes`
5. Branch: `main`

### Passo 4: Configurar Build

**Build Settings:**

- Build Method: `Dockerfile`
- Dockerfile Path: `./Dockerfile`
- Build Context: `.`

**Port Configuration:**

- Container Port: `8000`
- Public Port: `8000` (ou deixe automático)

### Passo 5: Configurar Variáveis de Ambiente

Clique em **"Environment Variables"** e adicione:

```env
EVOLUTION_API_URL=https://evolution.etechats.com.br
EVOLUTION_API_KEY=sua_chave_api_aqui
EVOLUTION_INSTANCE=TESTE_AUTO_MGI
LOG_LEVEL=INFO
ENVIRONMENT=production
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000
WEBHOOK_PATH=/webhook/:test_cases_auto
```

**Variáveis obrigatórias:**

- `EVOLUTION_API_KEY` ⚠️ IMPORTANTE
- `EVOLUTION_INSTANCE`

**Variáveis opcionais:**

- `GOOGLE_SHEETS_DOCUMENT_ID`
- `GOOGLE_SHEETS_TESTES_2026_SHEET_ID`
- `GITHUB_TOKEN`

### Passo 6: Configurar Domínio (Opcional)

1. Clique em **"Domains"**
2. Adicione seu domínio:
   - `api.whatsapp-sender.seudominio.com`
3. EasyPanel configura SSL automaticamente

### Passo 7: Deploy

1. Clique em **"Deploy"**
2. Aguarde o build (pode levar 2-5 minutos)
3. Acompanhe os logs em tempo real

### Passo 8: Verificar

1. Acesse a URL gerada pelo EasyPanel
2. Teste o health check: `https://sua-url/health`
3. Deve retornar: `{"status": "healthy"}`

---

## 🎯 Método 2: Deploy via Docker Image

### Passo 1: Build Local

```bash
# Build da imagem
docker build -t whatsapp-sender:latest .

# Tag para registry
docker tag whatsapp-sender:latest seu-registry/whatsapp-sender:latest

# Push para registry
docker push seu-registry/whatsapp-sender:latest
```

### Passo 2: Criar Serviço no EasyPanel

1. Clique em **"+ New Service"**
2. Selecione **"Docker Image"**
3. Image: `seu-registry/whatsapp-sender:latest`
4. Port: `8000`

### Passo 3: Configurar

Adicione as mesmas variáveis de ambiente do Método 1.

### Passo 4: Deploy

Clique em **"Deploy"** e aguarde.

---

## 🎯 Método 3: Deploy via Docker Compose

### Passo 1: Criar Serviço

1. Clique em **"+ New Service"**
2. Selecione **"Docker Compose"**

### Passo 2: Colar Configuração

Cole o conteúdo do `docker-compose.yml`:

```yaml
version: "3.8"

services:
  whatsapp-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: whatsapp-sender-api
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - whatsapp-network

  whatsapp-web:
    image: python:3.11-slim
    container_name: whatsapp-sender-web
    restart: unless-stopped
    command: python3 -m http.server 8080
    working_dir: /app
    ports:
      - "8080:8080"
    volumes:
      - ./whatsapp_simple.html:/app/whatsapp_simple.html:ro
    depends_on:
      whatsapp-api:
        condition: service_healthy
    networks:
      - whatsapp-network

networks:
  whatsapp-network:
    driver: bridge

volumes:
  logs:
    driver: local
```

### Passo 3: Configurar Variáveis

Adicione as variáveis de ambiente na seção apropriada.

### Passo 4: Deploy

Clique em **"Deploy"**.

---

## ⚙️ Configurações Avançadas no EasyPanel

### Auto Deploy (CI/CD)

1. Vá em **"Settings"** do serviço
2. Ative **"Auto Deploy"**
3. Selecione a branch: `main`
4. Agora cada push no GitHub faz deploy automático

### Recursos (CPU/Memória)

1. Vá em **"Resources"**
2. Configure:
   - **CPU**: 1 core
   - **Memory**: 512 MB
   - **Replicas**: 1

### Health Check

1. Vá em **"Health Check"**
2. Configure:
   - **Path**: `/health`
   - **Port**: `8000`
   - **Interval**: `30s`
   - **Timeout**: `10s`
   - **Retries**: `3`

### Volumes Persistentes

1. Vá em **"Volumes"**
2. Clique em **"+ Add Volume"**
3. Configure:
   - **Name**: `whatsapp-logs`
   - **Mount Path**: `/app/logs`
   - **Size**: `1 GB`

### Domínio Customizado

1. Vá em **"Domains"**
2. Clique em **"+ Add Domain"**
3. Digite: `api.seudominio.com`
4. EasyPanel configura SSL automaticamente (Let's Encrypt)
5. Aguarde propagação DNS (pode levar até 24h)

### Variáveis de Ambiente Secretas

1. Vá em **"Environment"**
2. Para variáveis sensíveis, marque **"Secret"**
3. Elas não aparecerão nos logs

---

## 🔍 Monitoramento no EasyPanel

### Logs em Tempo Real

1. Vá no seu serviço
2. Clique em **"Logs"**
3. Veja logs em tempo real
4. Use filtros para buscar erros

### Métricas

1. Clique em **"Metrics"**
2. Veja gráficos de:
   - CPU Usage
   - Memory Usage
   - Network I/O
   - Request Rate

### Alertas

1. Vá em **"Alerts"**
2. Configure alertas para:
   - CPU > 80%
   - Memory > 90%
   - Service Down
   - Health Check Failed

---

## 🔄 Atualização e Rollback

### Atualizar Serviço

**Método 1: Auto Deploy (se configurado)**

```bash
# Faça mudanças no código
git add .
git commit -m "Atualização"
git push origin main

# EasyPanel faz deploy automático
```

**Método 2: Manual**

1. Vá no serviço
2. Clique em **"Redeploy"**
3. Aguarde o build

### Rollback

1. Vá em **"Deployments"**
2. Veja histórico de deploys
3. Clique em **"Rollback"** no deploy anterior
4. Confirme

---

## 🧪 Testes Após Deploy

### 1. Health Check

```bash
curl https://sua-url.easypanel.app/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "timestamp": "2026-04-04"
}
```

### 2. Endpoint Principal

```bash
curl https://sua-url.easypanel.app/
```

Resposta esperada:

```json
{
  "message": "WhatsApp Message Dispatcher - Standalone",
  "version": "1.0.0",
  "status": "running"
}
```

### 3. Teste de Envio

```bash
curl -X POST https://sua-url.easypanel.app/webhook/tela2 \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+5561999999999",
    "text_list": "🧪 Teste EasyPanel\n✅ Deploy funcionando"
  }'
```

---

## 🐛 Troubleshooting

### Build Falha

**Problema**: Build não completa

**Solução**:

1. Verifique logs do build
2. Certifique-se que `Dockerfile` está correto
3. Verifique se todas as dependências estão no `requirements.txt`
4. Tente rebuild: **"Redeploy"** > **"Clear Cache"**

### Container Não Inicia

**Problema**: Container para logo após iniciar

**Solução**:

1. Veja logs: **"Logs"** > últimas 100 linhas
2. Verifique variáveis de ambiente
3. Teste localmente: `docker-compose up`
4. Verifique health check

### Health Check Falha

**Problema**: Health check sempre falha

**Solução**:

1. Verifique se porta está correta (8000)
2. Teste endpoint: `curl http://localhost:8000/health`
3. Aumente timeout do health check
4. Verifique logs da aplicação

### Erro 502 Bad Gateway

**Problema**: Erro ao acessar URL

**Solução**:

1. Verifique se container está rodando
2. Verifique porta exposta (8000)
3. Veja logs do serviço
4. Reinicie o serviço

### Variáveis de Ambiente Não Funcionam

**Problema**: API não conecta com Evolution

**Solução**:

1. Vá em **"Environment"**
2. Verifique se `EVOLUTION_API_KEY` está preenchida
3. Verifique se não há espaços extras
4. Redeploy após alterar variáveis

---

## 🔐 Segurança no EasyPanel

### HTTPS Automático

EasyPanel configura SSL automaticamente com Let's Encrypt.

### Variáveis Secretas

Marque variáveis sensíveis como **"Secret"**:

- `EVOLUTION_API_KEY`
- `GITHUB_TOKEN`
- `GOOGLE_SHEETS_DOCUMENT_ID`

### Firewall

EasyPanel já tem firewall configurado. Apenas portas expostas são acessíveis.

### Backup

1. Vá em **"Backups"**
2. Configure backup automático
3. Frequência: Diária
4. Retenção: 7 dias

---

## 📊 Escalabilidade

### Aumentar Recursos

1. Vá em **"Resources"**
2. Aumente:
   - CPU: 2 cores
   - Memory: 1 GB

### Múltiplas Réplicas

1. Vá em **"Scaling"**
2. Replicas: `2` ou mais
3. EasyPanel faz load balancing automático

### Auto Scaling

1. Vá em **"Auto Scaling"**
2. Configure:
   - Min replicas: 1
   - Max replicas: 5
   - CPU threshold: 70%

---

## 💰 Custos

EasyPanel cobra por:

- **Recursos usados** (CPU/Memory)
- **Tráfego** (bandwidth)
- **Armazenamento** (volumes)

Estimativa para este projeto:

- **CPU**: 1 core = ~$5-10/mês
- **Memory**: 512 MB = ~$2-5/mês
- **Total**: ~$7-15/mês

---

## 🎯 Checklist de Deploy

- [ ] Conta EasyPanel criada
- [ ] Repositório GitHub conectado
- [ ] Variáveis de ambiente configuradas
- [ ] `EVOLUTION_API_KEY` preenchida
- [ ] Serviço criado no EasyPanel
- [ ] Build concluído com sucesso
- [ ] Container rodando
- [ ] Health check OK
- [ ] Logs sem erros
- [ ] Teste de envio bem-sucedido
- [ ] Domínio configurado (opcional)
- [ ] SSL ativo (automático)
- [ ] Auto deploy configurado
- [ ] Backup configurado
- [ ] Alertas configurados

---

## 📱 URLs Após Deploy

EasyPanel gera URLs automáticas:

- **Serviço API**: `https://whatsapp-sender-api-xxx.easypanel.app`
- **Health Check**: `https://whatsapp-sender-api-xxx.easypanel.app/health`
- **Webhook**: `https://whatsapp-sender-api-xxx.easypanel.app/webhook/tela2`

Ou use seu domínio customizado:

- **API**: `https://api.seudominio.com`
- **Web**: `https://whatsapp.seudominio.com`

---

## 🎉 Pronto!

Seu sistema está rodando no EasyPanel com:

✅ Deploy automático via GitHub
✅ SSL configurado automaticamente
✅ Health checks ativos
✅ Logs em tempo real
✅ Métricas e monitoramento
✅ Backup automático
✅ Escalabilidade fácil

---

## 📞 Suporte

- **Documentação**: README.md
- **Docker**: DOCKER_DEPLOY.md
- **Portainer**: PORTAINER_INSTALL.md
- **Issues**: https://github.com/Marcu-Loreto/disparado_casos_testes/issues
- **EasyPanel Docs**: https://easypanel.io/docs
