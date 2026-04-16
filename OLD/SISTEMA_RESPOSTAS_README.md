# 📥 SISTEMA DE RECEBIMENTO DE RESPOSTAS

## 🎯 Funcionalidades Implementadas

✅ **Recebimento Automático de Respostas**

- Webhook configurável na Evolution API
- Processa mensagens recebidas automaticamente
- Filtra apenas números que enviaram mensagens

✅ **Filtro Inteligente**

- Só processa respostas de números ativos
- Ignora mensagens de outros números
- Valida remoteJid automaticamente

✅ **Salvamento no Google Sheets**

- Salva timestamp, número e mensagem
- Modo append (sempre nova linha)
- Não sobrescreve dados existentes

✅ **Gerenciamento de Números Ativos**

- Registra automaticamente ao enviar mensagens
- Contador de respostas por número
- API para consultar números ativos

---

## 🚀 Como Usar

### 1. Iniciar o Sistema

```bash
python3 START.py
```

### 2. Configurar Webhook na Evolution API

Acesse o painel da Evolution API e configure:

```
URL: http://SEU_SERVIDOR:8000/webhook/evolution/messages
Evento: messages.upsert
Método: POST
```

**Documentação completa**: `CONFIGURAR_WEBHOOK_EVOLUTION.md`

### 3. Enviar Mensagens

Acesse: http://localhost:8080/whatsapp_simple.html

Cole suas mensagens e envie para o número desejado.

### 4. Receber Respostas

Quando o destinatário responder pelo WhatsApp:

- ✅ Sistema recebe automaticamente
- ✅ Verifica se é do número correto
- ✅ Salva no Google Sheets
- ✅ Atualiza contador

---

## 📡 Endpoints Disponíveis

### POST /webhook/tela2

**Enviar mensagens**

```bash
curl -X POST http://localhost:8000/webhook/tela2 \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+5561999999999",
    "text_list": "Mensagem 1\nMensagem 2"
  }'
```

### POST /webhook/evolution/messages

**Receber respostas (Evolution API)**

```bash
curl -X POST http://localhost:8000/webhook/evolution/messages \
  -H "Content-Type: application/json" \
  -d '{
    "event": "messages.upsert",
    "data": {
      "key": {
        "remoteJid": "5561999999999@s.whatsapp.net",
        "fromMe": false
      },
      "message": {
        "conversation": "Resposta do usuário"
      }
    }
  }'
```

### GET /active-numbers

**Ver números ativos**

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
      "responses_count": 5
    }
  },
  "count": 1
}
```

---

## 🧪 Testar Sistema

Execute o script de teste:

```bash
python3 test_response_receiver.py
```

O teste irá:

1. ✅ Verificar se servidor está rodando
2. ✅ Registrar número de teste
3. ✅ Verificar números ativos
4. ✅ Simular recebimento de mensagem
5. ✅ Testar filtro (número não ativo)
6. ✅ Verificar contador de respostas

---

## 📊 Estrutura do Google Sheets

As respostas são salvas com esta estrutura:

| Coluna       | Descrição             | Exemplo                     |
| ------------ | --------------------- | --------------------------- |
| Timestamp    | Data/hora da resposta | 2026-04-04 10:30:15         |
| Phone Number | Número que respondeu  | +5561999999999              |
| Response     | Texto da resposta     | "Olá, recebi sua mensagem!" |

**Modo de inserção**: Sempre adiciona nova linha (append)

---

## 🔍 Como Funciona

### Fluxo Completo:

```
┌─────────────────────────────────────────────────────────┐
│ 1. Usuário envia mensagens via interface web           │
│    → Sistema registra número como "ativo"               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Mensagens são enviadas via Evolution API            │
│    → WhatsApp entrega para destinatário                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Destinatário responde pelo WhatsApp                  │
│    → Evolution API recebe a mensagem                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Evolution API envia webhook para nosso servidor     │
│    → POST /webhook/evolution/messages                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Sistema processa mensagem recebida                  │
│    → Extrai remoteJid e texto                          │
│    → Normaliza número de telefone                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. Sistema verifica se número está ativo               │
│    ┌─────────────────┬─────────────────┐              │
│    │ SIM             │ NÃO             │              │
│    │ ↓               │ ↓               │              │
│    │ Processa        │ Ignora          │              │
│    └─────────────────┴─────────────────┘              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 7. Salva resposta no Google Sheets                     │
│    → Adiciona nova linha (append)                       │
│    → Atualiza contador de respostas                    │
└─────────────────────────────────────────────────────────┘
```

### Validação de Número:

```python
# Mensagem recebida de: 556132073332@s.whatsapp.net
# Sistema extrai: 556132073332
# Normaliza: 556132073332 (remove +, espaços, etc)

# Número registrado: +55 61 3207-3332
# Normaliza: 556132073332

# Comparação: 556132073332 == 556132073332 ✅
# Resultado: PROCESSA
```

---

## 📁 Arquivos Criados

| Arquivo                           | Descrição                       |
| --------------------------------- | ------------------------------- |
| `app/response_receiver.py`        | Recebe e processa mensagens     |
| `app/google_sheets_handler.py`    | Salva no Google Sheets          |
| `app/standalone_server.py`        | Servidor atualizado com webhook |
| `test_response_receiver.py`       | Script de teste                 |
| `CONFIGURAR_WEBHOOK_EVOLUTION.md` | Guia de configuração            |
| `SISTEMA_RESPOSTAS_README.md`     | Este arquivo                    |

---

## 🐛 Troubleshooting

### Respostas não estão sendo recebidas

1. Verifique se webhook está configurado na Evolution API
2. Teste manualmente:
   ```bash
   curl -X POST http://localhost:8000/webhook/evolution/messages \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```
3. Verifique logs do servidor
4. Verifique se número está ativo:
   ```bash
   curl http://localhost:8000/active-numbers
   ```

### Mensagens de outros números estão sendo processadas

Isso NÃO deve acontecer. O sistema filtra automaticamente.

Se acontecer:

1. Verifique logs
2. Execute teste: `python3 test_response_receiver.py`
3. Verifique normalização de números

### Google Sheets não está salvando

1. Verifique se Google Sheets API está configurada
2. Verifique credenciais (`credentials.json`)
3. Verifique se planilha está compartilhada
4. Veja logs para erros específicos

---

## 🎯 Checklist

- [ ] Sistema iniciado (`python3 START.py`)
- [ ] Webhook configurado na Evolution API
- [ ] Teste executado (`python3 test_response_receiver.py`)
- [ ] Mensagens enviadas via interface
- [ ] Resposta recebida pelo WhatsApp
- [ ] Logs mostram processamento
- [ ] Google Sheets API configurada
- [ ] Respostas salvas na planilha

---

## 📚 Documentação Relacionada

- **Configurar Webhook**: `CONFIGURAR_WEBHOOK_EVOLUTION.md`
- **Guia do Usuário**: `README_USUARIO.md`
- **Deploy Docker**: `DOCKER_DEPLOY.md`
- **Deploy Portainer**: `PORTAINER_INSTALL.md`
- **Deploy EasyPanel**: `EASYPANEL_INSTALL.md`

---

## 🎉 Pronto!

Seu sistema agora:

- ✅ Envia mensagens automatizadas
- ✅ Recebe respostas automaticamente
- ✅ Filtra apenas números corretos
- ✅ Salva no Google Sheets
- ✅ Ignora mensagens indesejadas
- ✅ Conta respostas por número

**Sistema 100% automatizado!** 🚀
