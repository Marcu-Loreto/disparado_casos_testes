# 🚀 Início Rápido - Webhook Distribuidor

## 📋 O que você vai fazer

Configurar um distribuidor que permite N8N e Python receberem as mesmas mensagens do WhatsApp.

## ⚡ Início Rápido (3 comandos)

### Opção 1: Tudo de uma vez (Recomendado)

```bash
# Inicia distribuidor + servidor Python + interface web
python3 START_COMPLETO.py
```

Depois, em outro terminal:

```bash
# Configura o webhook na Evolution
python3 configurar_webhook_distribuidor.py
```

### Opção 2: Passo a passo

```bash
# Terminal 1 - Distribuidor
python3 webhook_distributor.py

# Terminal 2 - Servidor Python
python3 START.py

# Terminal 3 - Configurar webhook
python3 configurar_webhook_distribuidor.py
```

## 🎯 Fluxo Completo

```
1. Inicia distribuidor (porta 9000)
   ↓
2. Inicia servidor Python (porta 8000)
   ↓
3. Configura webhook na Evolution
   ↓
4. Testa enviando mensagem
   ↓
5. N8N e Python recebem!
```

## 📊 Arquitetura

```
WhatsApp (+55 19 99338-8617)
         ↓
Evolution API (TESTE_AUTO_MGI)
         ↓
Webhook Distribuidor (:9000)
         ├─→ N8N (webhook.etechats.com.br/webhook/TESTE01)
         └─→ Python (:8000/webhook/evolution/messages)
```

## ✅ Checklist de Verificação

Antes de configurar, certifique-se:

- [ ] Distribuidor rodando (porta 9000)
- [ ] Servidor Python rodando (porta 8000)
- [ ] Porta 9000 aberta no firewall (se VPS)
- [ ] N8N funcionando normalmente

## 🔍 Como Verificar se Está Funcionando

### 1. Health Check do Distribuidor

```bash
curl http://localhost:9000/health
```

Deve retornar:

```json
{
  "status": "healthy",
  "service": "Webhook Distributor",
  "destinations": [...]
}
```

### 2. Health Check do Python

```bash
curl http://localhost:8000/health
```

Deve retornar:

```json
{
  "status": "healthy",
  "timestamp": "2026-04-01"
}
```

### 3. Teste Completo

1. Envie mensagem pelo WhatsApp para o número configurado
2. Veja nos logs do distribuidor:
   ```
   📨 Webhook recebido da Evolution API
      → Enviando para N8N...
      ✅ N8N: OK
      → Enviando para Python Local...
      ✅ Python Local: OK
   ```

## 🎨 Interface Web

Acesse: `http://localhost:8080/whatsapp_final.html`

- **Aba Enviar**: Cole números e mensagens
- **Aba Recepção**: Veja respostas em tempo real
- **Aba Histórico**: Baixe CSVs anteriores

## ⚙️ Configuração do Webhook

Ao executar `configurar_webhook_distribuidor.py`, escolha:

**Opção 1: Mesma VPS da Evolution** (Recomendado)

- URL: `https://webhook.etechats.com.br:9000/webhook/distributor`
- Certifique-se de que a porta 9000 está aberta

**Opção 2: Localhost com ngrok** (Para testes)

- Execute: `ngrok http 9000`
- Use a URL fornecida pelo ngrok

**Opção 3: Outro servidor**

- Digite a URL do servidor onde o distribuidor está rodando

## 🔧 Configurações no .env

O distribuidor lê automaticamente do `.env`:

```env
# Webhook do N8N (será um dos destinos)
WEBHOOK_RECEPTION_URL=https://webhook.etechats.com.br/webhook/TESTE01

# Porta do servidor Python
WEBHOOK_PORT=8000
```

## 📝 Logs Importantes

### Distribuidor recebeu webhook:

```
📨 Webhook recebido da Evolution API
   Evento: messages.upsert
```

### Distribuiu com sucesso:

```
   → Enviando para N8N...
   ✅ N8N: OK
   → Enviando para Python Local...
   ✅ Python Local: OK
```

### Erro ao distribuir:

```
   ❌ N8N: HTTP 404
   ❌ Python Local: Connection refused
```

## 🆘 Troubleshooting

### Distribuidor não inicia

```bash
# Verifique se a porta 9000 está livre
lsof -i :9000

# Se estiver ocupada, mate o processo
kill -9 <PID>
```

### N8N não recebe

1. Verifique se a URL está correta no `.env`
2. Teste manualmente:
   ```bash
   curl -X POST https://webhook.etechats.com.br/webhook/TESTE01 \
     -H "Content-Type: application/json" \
     -d '{"test": true}'
   ```

### Python não recebe

1. Verifique se está rodando:

   ```bash
   curl http://localhost:8000/health
   ```

2. Veja os logs do servidor Python

### Webhook não chega no distribuidor

1. Verifique o webhook configurado na Evolution:

   ```bash
   curl -H "apikey: SUA_API_KEY" \
     https://evolution.etechats.com.br/webhook/find/TESTE_AUTO_MGI
   ```

2. Deve mostrar a URL do distribuidor

## 🔄 Reverter Configuração

Para voltar ao N8N direto (sem distribuidor):

```bash
# Pare o distribuidor (Ctrl+C)

# Reconfigure o webhook
curl -X POST https://evolution.etechats.com.br/webhook/set/TESTE_AUTO_MGI \
  -H "apikey: SUA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://webhook.etechats.com.br/webhook/TESTE01",
    "webhook_by_events": true,
    "events": ["messages.upsert"]
  }'
```

## 🎉 Pronto!

Agora você tem:

- ✅ N8N recebendo mensagens (como antes)
- ✅ Python recebendo mensagens (novo)
- ✅ Mesma instância Evolution
- ✅ Mesmo número WhatsApp
- ✅ Sem conflitos

## 📞 Próximos Passos

1. Execute `python3 START_COMPLETO.py`
2. Execute `python3 configurar_webhook_distribuidor.py`
3. Acesse `http://localhost:8080/whatsapp_final.html`
4. Envie mensagens de teste
5. Veja as respostas chegando em tempo real!
