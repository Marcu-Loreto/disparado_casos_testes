# 🔀 Setup do Webhook Distribuidor

## 📋 O que é?

Um servidor intermediário que recebe webhooks da Evolution API e distribui para múltiplos destinos (N8N + Python).

## ✅ Vantagens

- Usa a mesma instância Evolution que você já tem
- N8N continua funcionando normalmente
- Python recebe as mesmas mensagens
- Fácil de gerenciar

## 🚀 Passo a Passo

### 1. Inicie o Distribuidor

```bash
# Terminal 1 - Distribuidor (porta 9000)
python3 webhook_distributor.py
```

Saída esperada:

```
🔀 WEBHOOK DISTRIBUTOR - INICIADO
📍 Servidor rodando em: http://0.0.0.0:9000
📥 Endpoint webhook: http://0.0.0.0:9000/webhook/distributor

📤 Destinos configurados:
   1. N8N: https://webhook.etechats.com.br/webhook/TESTE01 - ✅ Ativo
   2. Python Local: http://localhost:8000/webhook/evolution/messages - ✅ Ativo
```

### 2. Inicie o Sistema Python

```bash
# Terminal 2 - Sistema Python (porta 8000)
python3 START.py
```

### 3. Configure o Webhook na Evolution

**IMPORTANTE**: Isso vai alterar o webhook atual do N8N!

Você tem 2 opções:

#### Opção A: Distribuidor na mesma VPS (Recomendado)

Se o distribuidor está na mesma VPS que a Evolution:

```bash
python3 configurar_webhook_distribuidor.py
```

Vai configurar: `https://webhook.etechats.com.br:9000/webhook/distributor`

#### Opção B: Distribuidor local (apenas testes)

Se está testando localmente, precisa de ngrok ou similar:

```bash
# Em outro terminal
ngrok http 9000

# Use a URL do ngrok no configurador
```

### 4. Teste o Fluxo

1. Envie uma mensagem de teste pelo WhatsApp
2. Veja os logs do distribuidor:
   ```
   📨 Webhook recebido da Evolution API
      → Enviando para N8N...
      ✅ N8N: OK
      → Enviando para Python Local...
      ✅ Python Local: OK
   ```

## 🔧 Configuração Avançada

### Desabilitar um Destino

Edite `webhook_distributor.py`:

```python
DESTINATIONS = [
    {
        "name": "N8N",
        "url": "https://webhook.etechats.com.br/webhook/TESTE01",
        "enabled": True  # Mude para False para desabilitar
    },
    {
        "name": "Python Local",
        "url": "http://localhost:8000/webhook/evolution/messages",
        "enabled": True
    }
]
```

### Adicionar Mais Destinos

```python
DESTINATIONS = [
    # ... destinos existentes ...
    {
        "name": "Outro Sistema",
        "url": "https://outro-sistema.com/webhook",
        "enabled": True
    }
]
```

### Mudar Porta do Distribuidor

```python
# No final do arquivo webhook_distributor.py
if __name__ == "__main__":
    start_distributor(port=9000)  # Mude aqui
```

## 🔍 Monitoramento

### Health Check

```bash
curl http://localhost:9000/health
```

Resposta:

```json
{
  "status": "healthy",
  "service": "Webhook Distributor",
  "destinations": [...]
}
```

### Logs em Tempo Real

O distribuidor mostra logs de cada webhook recebido e distribuído:

```
📨 Webhook recebido da Evolution API
   Evento: messages.upsert
   → Enviando para N8N...
   ✅ N8N: OK
   → Enviando para Python Local...
   ✅ Python Local: OK
```

## ⚠️ Troubleshooting

### Distribuidor não recebe webhooks

1. Verifique se está rodando:

   ```bash
   curl http://localhost:9000/health
   ```

2. Verifique o webhook na Evolution:
   ```bash
   curl -H "apikey: SUA_API_KEY" \
     https://evolution.etechats.com.br/webhook/find/TESTE_AUTO_MGI
   ```

### N8N para de receber

1. Verifique se o distribuidor está rodando
2. Verifique se a URL do N8N está correta em `DESTINATIONS`
3. Teste manualmente:
   ```bash
   curl -X POST https://webhook.etechats.com.br/webhook/TESTE01 \
     -H "Content-Type: application/json" \
     -d '{"test": true}'
   ```

### Python não recebe

1. Verifique se o servidor Python está rodando (porta 8000)
2. Teste manualmente:
   ```bash
   curl -X POST http://localhost:8000/webhook/evolution/messages \
     -H "Content-Type: application/json" \
     -d '{"test": true}'
   ```

## 🔄 Reverter para N8N Direto

Se quiser voltar ao setup anterior (apenas N8N):

1. Pare o distribuidor (Ctrl+C)
2. Reconfigure o webhook:
   ```bash
   curl -X POST https://evolution.etechats.com.br/webhook/set/TESTE_AUTO_MGI \
     -H "apikey: SUA_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://webhook.etechats.com.br/webhook/TESTE01",
       "webhook_by_events": true,
       "events": ["messages.upsert"]
     }'
   ```

## 📊 Arquitetura Final

```
┌─────────────────────────┐
│   WhatsApp              │
│   +55 19 99338-8617     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Evolution API         │
│   TESTE_AUTO_MGI        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Webhook Distribuidor  │
│   Porta 9000            │
└─────┬──────────┬────────┘
      │          │
      ▼          ▼
┌─────────┐  ┌──────────┐
│   N8N   │  │  Python  │
│  TESTE01│  │  :8000   │
└─────────┘  └──────────┘
```

## 🎉 Pronto!

Agora você tem:

- ✅ N8N recebendo mensagens (como antes)
- ✅ Python recebendo mensagens (novo)
- ✅ Mesma instância Evolution
- ✅ Mesmo número WhatsApp
- ✅ Sem conflitos
