# 🔀 Sistema com Webhook Distribuidor

## 📖 Visão Geral

Este sistema permite que **N8N e Python** recebam as mesmas mensagens do WhatsApp simultaneamente, usando um webhook distribuidor.

## 🎯 Problema Resolvido

Antes você tinha:

- N8N recebendo mensagens via webhook
- Python precisava receber as mesmas mensagens
- Evolution API só permite 1 webhook por instância

Agora você tem:

- **Distribuidor** recebe da Evolution API
- **Distribui** para N8N e Python simultaneamente
- **Sem conflitos**, ambos funcionam perfeitamente

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    WhatsApp                             │
│              +55 19 99338-8617                          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Evolution API                              │
│           Instância: TESTE_AUTO_MGI                     │
│    https://evolution.etechats.com.br                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ Webhook configurado
                         ▼
┌─────────────────────────────────────────────────────────┐
│          🔀 Webhook Distribuidor                        │
│              Porta: 9000                                │
│   https://webhook.etechats.com.br:9000/webhook/...     │
└─────────────┬───────────────────────┬───────────────────┘
              │                       │
              ▼                       ▼
┌─────────────────────┐   ┌─────────────────────────────┐
│       N8N           │   │    Sistema Python           │
│   (existente)       │   │      (novo)                 │
│                     │   │                             │
│ webhook/TESTE01     │   │ :8000/webhook/evolution/... │
└─────────────────────┘   └─────────────────────────────┘
```

## 🚀 Início Rápido

### Passo 1: Inicie o Sistema Completo

```bash
python3 START_COMPLETO.py
```

Isso inicia:

- ✅ Webhook Distribuidor (porta 9000)
- ✅ Servidor Python (porta 8000)
- ✅ Interface Web (porta 8080)

### Passo 2: Configure o Webhook na Evolution

Em outro terminal:

```bash
python3 configurar_webhook_distribuidor.py
```

Escolha a opção 1 (Mesma VPS da Evolution) e confirme.

### Passo 3: Teste

```bash
python3 testar_distribuidor.py
```

### Passo 4: Use a Interface

Acesse: http://localhost:8080/whatsapp_final.html

## 📁 Arquivos do Sistema

### Principais

- `webhook_distributor.py` - Servidor distribuidor
- `START_COMPLETO.py` - Inicia tudo de uma vez
- `configurar_webhook_distribuidor.py` - Configura webhook na Evolution
- `testar_distribuidor.py` - Testa se está funcionando

### Documentação

- `README_DISTRIBUIDOR.md` - Este arquivo
- `INICIO_RAPIDO_DISTRIBUIDOR.md` - Guia rápido
- `SETUP_DISTRIBUIDOR.md` - Setup detalhado

### Sistema Python

- `app/standalone_server.py` - Servidor principal
- `app/response_receiver.py` - Processa mensagens recebidas
- `app/session_manager.py` - Gerencia sessões e CSVs
- `app/database.py` - Banco SQLite

### Interface

- `whatsapp_final.html` - Interface completa
- `START.py` - Inicia apenas servidor Python + interface

## ⚙️ Configuração (.env)

```env
# Evolution API
EVOLUTION_API_URL=https://evolution.etechats.com.br
EVOLUTION_API_KEY=sua_api_key
EVOLUTION_INSTANCE=TESTE_AUTO_MGI

# Webhook do N8N (será um dos destinos do distribuidor)
WEBHOOK_RECEPTION_URL=https://webhook.etechats.com.br/webhook/TESTE01

# Servidor Python
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000
```

## 🔍 Verificações

### 1. Distribuidor está rodando?

```bash
curl http://localhost:9000/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "service": "Webhook Distributor",
  "destinations": [...]
}
```

### 2. Servidor Python está rodando?

```bash
curl http://localhost:8000/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "timestamp": "2026-04-01"
}
```

### 3. Webhook configurado na Evolution?

```bash
curl -H "apikey: SUA_API_KEY" \
  https://evolution.etechats.com.br/webhook/find/TESTE_AUTO_MGI
```

Deve mostrar a URL do distribuidor.

## 📊 Monitoramento

### Logs do Distribuidor

Quando uma mensagem chega:

```
📨 Webhook recebido da Evolution API
   Evento: messages.upsert
   → Enviando para N8N...
   ✅ N8N: OK
   → Enviando para Python Local...
   ✅ Python Local: OK
```

### Logs do Servidor Python

Quando processa uma mensagem:

```
INFO - Mensagem recebida da Evolution API
INFO - Resposta processada e salva
INFO - Sessão atualizada: 1/10 mensagens
```

## 🎨 Interface Web

### Aba Enviar

- Cole números (um por linha)
- Cole mensagens (uma por linha)
- Clique em "Enviar Mensagens"

### Aba Recepção

- Veja respostas em tempo real
- Contador incremental (X/Total)
- Última resposta destacada
- Atualização automática a cada 3 segundos

### Aba Histórico

- Lista de sessões anteriores
- Download de CSVs
- Estatísticas de envio/recepção

## 📁 Onde as Respostas São Salvas

### CSV por Sessão

```
sessions/respostas_5519993388617_20260404_143022.csv
```

Formato:

```csv
timestamp,phone_number,message
2026-04-04 14:30:25,+5519993388617,Resposta do usuário
```

### Banco SQLite

```
whatsapp_responses.db
```

Tabelas:

- `responses` - Todas as respostas
- `exports` - Histórico de exportações

## 🔧 Troubleshooting

### Distribuidor não inicia

**Erro**: `Address already in use`

**Solução**:

```bash
# Encontre o processo na porta 9000
lsof -i :9000

# Mate o processo
kill -9 <PID>

# Inicie novamente
python3 webhook_distributor.py
```

### N8N não recebe mensagens

**Verificações**:

1. URL do N8N está correta no `.env`?
2. N8N está rodando?
3. Teste manualmente:
   ```bash
   curl -X POST https://webhook.etechats.com.br/webhook/TESTE01 \
     -H "Content-Type: application/json" \
     -d '{"test": true}'
   ```

### Python não recebe mensagens

**Verificações**:

1. Servidor Python está rodando?
   ```bash
   curl http://localhost:8000/health
   ```
2. Veja os logs do servidor
3. Verifique se o distribuidor está enviando:
   - Logs devem mostrar: `✅ Python Local: OK`

### Webhook não chega no distribuidor

**Verificações**:

1. Distribuidor está rodando?
2. Webhook configurado corretamente na Evolution?
3. Porta 9000 está aberta no firewall?
4. Teste com `testar_distribuidor.py`

## 🔄 Comandos Úteis

### Iniciar tudo

```bash
python3 START_COMPLETO.py
```

### Iniciar apenas distribuidor

```bash
python3 webhook_distributor.py
```

### Iniciar apenas Python

```bash
python3 START.py
```

### Testar distribuidor

```bash
python3 testar_distribuidor.py
```

### Configurar webhook

```bash
python3 configurar_webhook_distribuidor.py
```

### Ver sessões ativas

```bash
curl http://localhost:8000/sessions
```

### Ver respostas

```bash
curl http://localhost:8000/responses
```

### Exportar para CSV

```bash
curl http://localhost:8000/export
```

## 🎉 Benefícios

- ✅ N8N continua funcionando normalmente
- ✅ Python recebe as mesmas mensagens
- ✅ Mesma instância Evolution
- ✅ Mesmo número WhatsApp
- ✅ Sem conflitos
- ✅ Fácil de adicionar mais destinos
- ✅ Logs detalhados
- ✅ Fácil de monitorar

## 📞 Suporte

Para mais informações, consulte:

- `INICIO_RAPIDO_DISTRIBUIDOR.md` - Guia rápido
- `SETUP_DISTRIBUIDOR.md` - Setup detalhado
- `SISTEMA_COMPLETO_README.md` - Documentação completa do sistema
