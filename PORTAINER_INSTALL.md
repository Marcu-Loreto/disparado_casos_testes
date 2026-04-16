# 🐳 INSTALAÇÃO NO PORTAINER

## 📋 Guia Completo para Deploy no Portainer

---

## 🎯 Método 1: Deploy via Stack (Recomendado)

### Passo 1: Acessar Portainer

1. Abra o Portainer no navegador
2. Faça login
3. Selecione seu ambiente (local ou remoto)

### Passo 2: Criar Nova Stack

1. No menu lateral, clique em **"Stacks"**
2. Clique no botão **"+ Add stack"**
3. Dê um nome: `whatsapp-sender`

### Passo 3: Adicionar Configuração

**Opção A: Upload do arquivo**

1. Selecione a aba **"Upload"**
2. Clique em **"Select file"**
3. Escolha o arquivo `portainer-stack.yml`
4. Clique em **"Upload"**

**Opção B: Web editor (copiar e colar)**

1. Selecione a aba **"Web editor"**
2. Cole o conteúdo do arquivo `portainer-stack.yml`

**Opção C: Git repository**

1. Selecione a aba **"Repository"**
2. Cole a URL: `https://github.com/Marcu-Loreto/disparado_casos_testes.git`
3. Compose path: `portainer-stack.yml`

### Passo 4: Configurar Variáveis de Ambiente

Role até a seção **"Environment variables"** e adicione:

```
EVOLUTION_API_URL=https://evolution.etechats.com.br
EVOLUTION_API_KEY=sua_chave_api_aqui
EVOLUTION_INSTANCE=TESTE_AUTO_MGI
LOG_LEVEL=INFO
ENVIRONMENT=production
```

**Variáveis obrigatórias:**

- `EVOLUTION_API_KEY` - Sua chave da Evolution API
- `EVOLUTION_INSTANCE` - Nome da sua instância WhatsApp

**Variáveis opcionais:**

- `GOOGLE_SHEETS_DOCUMENT_ID` - ID do Google Sheets
- `GOOGLE_SHEETS_TESTES_2026_SHEET_ID` - ID da planilha
- `GITHUB_TOKEN` - Token do GitHub

### Passo 5: Deploy

1. Clique no botão **"Deploy the stack"**
2. Aguarde o download das imagens
3. Aguarde os containers iniciarem

### Passo 6: Verificar Status

1. Vá em **"Stacks"** > **"whatsapp-sender"**
2. Verifique se os 2 containers estão **"running"**:
   - `whatsapp-sender-api`
   - `whatsapp-sender-web`

---

## 🎯 Método 2: Deploy via Container Individual

### Para o Container API:

1. Vá em **"Containers"** > **"+ Add container"**
2. Configure:

**Configurações básicas:**

- Name: `whatsapp-sender-api`
- Image: `python:3.11-slim`

**Command & logging:**

- Command: `python3 -m app.standalone_server`

**Network & ports:**

- Port mapping: `8000:8000`

**Env variables:**

```
EVOLUTION_API_URL=https://evolution.etechats.com.br
EVOLUTION_API_KEY=sua_chave_aqui
EVOLUTION_INSTANCE=TESTE_AUTO_MGI
LOG_LEVEL=INFO
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000
```

**Restart policy:**

- Restart policy: `Unless stopped`

3. Clique em **"Deploy the container"**

### Para o Container Web:

1. Vá em **"Containers"** > **"+ Add container"**
2. Configure:

**Configurações básicas:**

- Name: `whatsapp-sender-web`
- Image: `python:3.11-slim`

**Command & logging:**

- Command: `python3 -m http.server 8080`

**Network & ports:**

- Port mapping: `8080:8080`

**Restart policy:**

- Restart policy: `Unless stopped`

3. Clique em **"Deploy the container"**

---

## 🔍 Verificação e Testes

### 1. Verificar Logs

No Portainer:

1. Vá em **"Containers"**
2. Clique no container `whatsapp-sender-api`
3. Clique em **"Logs"**
4. Verifique se não há erros

### 2. Testar Health Check

Abra no navegador:

```
http://SEU_SERVIDOR:8000/health
```

Deve retornar:

```json
{
  "status": "healthy",
  "timestamp": "2026-04-04"
}
```

### 3. Testar Interface Web

Abra no navegador:

```
http://SEU_SERVIDOR:8080
```

### 4. Testar API

Use curl ou Postman:

```bash
curl -X POST http://SEU_SERVIDOR:8000/webhook/tela2 \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+5561999999999",
    "text_list": "Teste via Portainer\nSegunda mensagem"
  }'
```

---

## ⚙️ Configurações Avançadas no Portainer

### Limites de Recursos

Na criação da stack ou container, adicione em **"Resources"**:

**Memory:**

- Reservation: 256 MB
- Limit: 512 MB

**CPU:**

- Reservation: 0.5
- Limit: 1.0

### Volumes Persistentes

Para salvar logs:

1. Vá em **"Volumes"** > **"+ Add volume"**
2. Name: `whatsapp-logs`
3. Driver: `local`

Na stack, adicione em **"Volumes"**:

```yaml
volumes:
  - whatsapp-logs:/app/logs
```

### Health Check

Adicione em **"Health check"**:

```
Test: curl -f http://localhost:8000/health || exit 1
Interval: 30s
Timeout: 10s
Retries: 3
Start period: 40s
```

### Rede Customizada

1. Vá em **"Networks"** > **"+ Add network"**
2. Name: `whatsapp-network`
3. Driver: `bridge`

Conecte os containers a esta rede.

---

## 🔄 Atualização da Stack

### Método 1: Via Portainer UI

1. Vá em **"Stacks"** > **"whatsapp-sender"**
2. Clique em **"Editor"**
3. Faça as alterações necessárias
4. Clique em **"Update the stack"**
5. Marque **"Re-pull image and redeploy"**
6. Clique em **"Update"**

### Método 2: Via Git (se configurado)

1. Faça push das alterações no GitHub
2. No Portainer, vá em **"Stacks"** > **"whatsapp-sender"**
3. Clique em **"Pull and redeploy"**

---

## 🐛 Troubleshooting no Portainer

### Container não inicia

1. Vá em **"Containers"** > container com problema
2. Clique em **"Logs"**
3. Verifique erros
4. Clique em **"Inspect"** para ver configuração
5. Clique em **"Stats"** para ver uso de recursos

### Erro de porta em uso

1. Vá em **"Containers"**
2. Verifique se há outro container usando a porta
3. Pare o container conflitante ou mude a porta

### Variáveis de ambiente não funcionam

1. Vá em **"Stacks"** > **"whatsapp-sender"**
2. Clique em **"Editor"**
3. Verifique a seção **"Environment variables"**
4. Adicione/corrija as variáveis
5. Clique em **"Update the stack"**

### Reiniciar Stack

1. Vá em **"Stacks"** > **"whatsapp-sender"**
2. Clique em **"Stop"**
3. Aguarde parar
4. Clique em **"Start"**

### Remover e Recriar

1. Vá em **"Stacks"** > **"whatsapp-sender"**
2. Clique em **"Delete this stack"**
3. Confirme
4. Crie novamente seguindo o Passo 2

---

## 📊 Monitoramento no Portainer

### Dashboard

1. Vá em **"Dashboard"**
2. Veja estatísticas gerais:
   - Containers rodando
   - Uso de CPU
   - Uso de memória
   - Uso de rede

### Logs em Tempo Real

1. Vá em **"Containers"** > container
2. Clique em **"Logs"**
3. Ative **"Auto-refresh logs"**
4. Ajuste **"Lines"** para ver mais linhas

### Estatísticas

1. Vá em **"Containers"** > container
2. Clique em **"Stats"**
3. Veja gráficos de:
   - CPU usage
   - Memory usage
   - Network I/O
   - Block I/O

### Console Interativo

1. Vá em **"Containers"** > container
2. Clique em **"Console"**
3. Selecione **"/bin/bash"** ou **"/bin/sh"**
4. Clique em **"Connect"**
5. Execute comandos dentro do container

---

## 🔐 Segurança no Portainer

### Secrets (Recomendado para produção)

1. Vá em **"Secrets"** > **"+ Add secret"**
2. Name: `evolution_api_key`
3. Secret: Cole sua chave API
4. Clique em **"Create secret"**

Na stack, use:

```yaml
secrets:
  - evolution_api_key

environment:
  - EVOLUTION_API_KEY_FILE=/run/secrets/evolution_api_key
```

### Acesso Restrito

1. Vá em **"Users"** > **"+ Add user"**
2. Crie usuários com permissões limitadas
3. Atribua apenas à stack necessária

---

## 📱 Acesso Externo

### Configurar Proxy Reverso

Se usar Nginx Proxy Manager no Portainer:

1. Vá em **"Containers"** > **"+ Add container"**
2. Deploy Nginx Proxy Manager
3. Configure proxy para:
   - `api.seudominio.com` → `whatsapp-sender-api:8000`
   - `web.seudominio.com` → `whatsapp-sender-web:8080`

### Configurar SSL

No Nginx Proxy Manager:

1. Adicione certificado SSL (Let's Encrypt)
2. Force HTTPS
3. Configure HSTS

---

## 🎯 Checklist de Instalação

- [ ] Portainer instalado e acessível
- [ ] Arquivo `portainer-stack.yml` preparado
- [ ] Variáveis de ambiente configuradas
- [ ] Stack criada no Portainer
- [ ] Containers rodando (2/2)
- [ ] Health check OK
- [ ] Logs sem erros
- [ ] API respondendo (porta 8000)
- [ ] Web respondendo (porta 8080)
- [ ] Teste de envio bem-sucedido
- [ ] Monitoramento configurado
- [ ] Backup configurado (produção)

---

## 📞 URLs Importantes

Após deploy no Portainer:

- **Interface Web**: `http://SEU_SERVIDOR:8080`
- **API WhatsApp**: `http://SEU_SERVIDOR:8000`
- **Health Check**: `http://SEU_SERVIDOR:8000/health`
- **Webhook**: `http://SEU_SERVIDOR:8000/webhook/tela2`

---

## 🎉 Pronto!

Seu sistema está rodando no Portainer!

Para suporte:

- 📚 Documentação: README.md
- 🐳 Docker: DOCKER_DEPLOY.md
- 💬 Issues: https://github.com/Marcu-Loreto/disparado_casos_testes/issues
