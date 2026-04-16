# 📥 CONFIGURAR WEBHOOK PARA RECEBER RESPOSTAS

## 🎯 Objetivo

Configurar a Evolution API para enviar mensagens recebidas para o nosso sistema, que irá:

1. ✅ Verificar se a mensagem é do número que enviamos
2. ✅ Salvar a resposta no Google Sheets
3. ✅ Ignorar mensagens de outros números

---

## 🔧 Passo 1: Configurar Webhook na Evolution API

### Opção A: Via Painel Web

1. Acesse o painel da Evolution API
2. Vá em **Instâncias** → Selecione `TESTE_AUTO_MGI`
3. Clique em **Configurações** ou **Webhooks**
4. Configure:

```
URL do Webhook: http://SEU_SERVIDOR:8000/webhook/evolution/messages
Eventos: messages.upsert (ou "Mensagens Recebidas")
Método: POST
Headers: (deixe padrão)
```

5. Clique em **Salvar** ou **Ativar**

### Opção B: Via API (cURL)

```bash
curl -X POST "https://evolution.etechats.com.br/webhook/set/TESTE_AUTO_MGI" \
  -H "apikey: 43248376731B-4E40-9799-0C45BDF43A55" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://SEU_SERVIDOR:8000/webhook/evolution/messages",
    "webhook_by_events": true,
    "events": [
      "messages.upsert"
    ]
  }'
```

### Opção C: Via API (Python)

```python
import requests

url = "https://evolution.etechats.com.br/webhook/set/TESTE_AUTO_MGI"
headers = {
    "apikey": "43248376731B-4E40-9799-0C45BDF43A55",
    "Content-Type": "application/json"
}
data = {
    "url": "http://SEU_SERVIDOR:8000/webhook/evolution/messages",
    "webhook_by_events": True,
    "events": ["messages.upsert"]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

---

## 🌐 Passo 2: Expor Servidor Localmente (Desenvolvimento)

Se estiver testando localmente, use **ngrok** ou **localtunnel**:

### Usando ngrok:

```bash
# Instalar ngrok
# https://ngrok.com/download

# Expor porta 8000
ngrok http 8000

# Copie a URL gerada (ex: https://abc123.ngrok.io)
# Use: https://abc123.ngrok.io/webhook/evolution/messages
```

### Usando localtunnel:

```bash
# Instalar
npm install -g localtunnel

# Expor porta 8000
lt --port 8000

# Use a URL gerada
```

---

## 🧪 Passo 3: Testar Webhook

### 1. Iniciar o servidor:

```bash
python3 START.py
```

### 2. Enviar mensagens de teste:

Acesse: http://localhost:8080/whatsapp_simple.html

Envie algumas mensagens para um número de teste.

### 3. Responder pelo WhatsApp:

No celular com o número que recebeu as mensagens, responda qualquer coisa.

### 4. Verificar logs:

No terminal onde o servidor está rodando, você verá:

```
INFO:app.response_receiver:Resposta recebida de 5561999999999: Olá, recebi sua mensagem!
INFO:app.google_sheets_handler:Salvando resposta de 5561999999999 no Google Sheets
```

### 5. Verificar números ativos:

```bash
curl http://localhost:8000/active-numbers
```

Resposta:

```json
{
  "status": "success",
  "active_numbers": {
    "5561999999999": {
      "registered_at": "2026-04-04T10:30:00",
      "phone_number": "+5561999999999",
      "responses_count": 3
    }
  },
  "count": 1
}
```

---

## 📊 Passo 4: Configurar Google Sheets API (Opcional)

Para salvar realmente no Google Sheets, você precisa:

### 1. Criar Projeto no Google Cloud:

1. Acesse: https://console.cloud.google.com
2. Crie um novo projeto
3. Ative a **Google Sheets API**

### 2. Criar Credenciais:

1. Vá em **APIs & Services** → **Credentials**
2. Clique em **Create Credentials** → **Service Account**
3. Baixe o arquivo JSON de credenciais
4. Salve como `credentials.json` na raiz do projeto

### 3. Compartilhar Planilha:

1. Abra sua planilha do Google Sheets
2. Clique em **Compartilhar**
3. Adicione o email da service account (está no credentials.json)
4. Dê permissão de **Editor**

### 4. Instalar biblioteca:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 5. Atualizar código:

O arquivo `app/google_sheets_handler.py` já está preparado, só precisa adicionar a implementação real da API.

---

## 🔍 Como Funciona

### Fluxo Completo:

```
1. Usuário envia mensagens via interface web
   ↓
2. Sistema registra número como "ativo"
   ↓
3. Mensagens são enviadas via Evolution API
   ↓
4. Destinatário responde pelo WhatsApp
   ↓
5. Evolution API envia webhook para nosso servidor
   ↓
6. Sistema verifica se número está na lista ativa
   ↓
7. Se SIM: Salva resposta no Google Sheets
   Se NÃO: Ignora mensagem
```

### Exemplo de Webhook Recebido:

```json
{
  "event": "messages.upsert",
  "instance": "TESTE_AUTO_MGI",
  "data": {
    "key": {
      "remoteJid": "5561999999999@s.whatsapp.net",
      "fromMe": false,
      "id": "ABC123"
    },
    "message": {
      "conversation": "Olá, recebi sua mensagem!"
    },
    "messageTimestamp": 1712217600
  }
}
```

### Dados Salvos no Google Sheets:

| Timestamp           | Phone Number   | Response                  |
| ------------------- | -------------- | ------------------------- |
| 2026-04-04 10:30:15 | +5561999999999 | Olá, recebi sua mensagem! |
| 2026-04-04 10:31:22 | +5561999999999 | Tudo bem, obrigado!       |
| 2026-04-04 10:32:45 | +5561999999999 | Até logo!                 |

---

## 🐛 Troubleshooting

### Webhook não está sendo chamado:

1. Verifique se configurou corretamente na Evolution API
2. Teste a URL manualmente:
   ```bash
   curl -X POST http://SEU_SERVIDOR:8000/webhook/evolution/messages \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```
3. Verifique logs do servidor
4. Verifique firewall/portas

### Mensagens não estão sendo salvas:

1. Verifique se número está na lista ativa:
   ```bash
   curl http://localhost:8000/active-numbers
   ```
2. Verifique logs do servidor
3. Verifique se Google Sheets API está configurada

### Mensagens de outros números estão sendo salvas:

Isso NÃO deve acontecer. O sistema só salva mensagens de números que:

1. Foram registrados ao enviar mensagens
2. Estão na lista `active_numbers`

Se isso acontecer, verifique os logs.

---

## 📝 Endpoints Disponíveis

| Endpoint                      | Método | Descrição          |
| ----------------------------- | ------ | ------------------ |
| `/webhook/tela2`              | POST   | Enviar mensagens   |
| `/webhook/evolution/messages` | POST   | Receber respostas  |
| `/active-numbers`             | GET    | Ver números ativos |
| `/health`                     | GET    | Health check       |
| `/`                           | GET    | Info do servidor   |

---

## 🎯 Checklist de Configuração

- [ ] Servidor iniciado (`python3 START.py`)
- [ ] Webhook configurado na Evolution API
- [ ] URL do webhook acessível (ngrok se local)
- [ ] Teste de envio realizado
- [ ] Resposta enviada pelo WhatsApp
- [ ] Logs mostram resposta recebida
- [ ] Google Sheets API configurada (opcional)
- [ ] Resposta salva no Google Sheets

---

## 🎉 Pronto!

Agora seu sistema:

- ✅ Envia mensagens automatizadas
- ✅ Recebe respostas automaticamente
- ✅ Filtra apenas números que você enviou
- ✅ Salva respostas no Google Sheets
- ✅ Ignora mensagens de outros números

**Documentação completa**: README.md
