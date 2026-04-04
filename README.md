# Disparado_Casos_testes Workflow

Sistema automatizado para envio de mensagens via WhatsApp com suporte a múltiplos formatos de entrada.

## 🚀 Funcionalidades

- **Webhook Integrado**: Recebe listas de mensagens via HTTP
- **Múltiplos Formatos**: JSON, texto colado, CSV, XLSX
- **Delays Configuráveis**: Controle do intervalo entre mensagens
- **API Evolution**: Integração com WhatsApp via Evolution API
- **Interface Web**: Página de teste incluída
- **Validação**: Verificação automática de formatos e dados

## 📋 Endpoints Disponíveis

### Webhook Principal
```
POST http://localhost:8000/webhook/tela2
```

### Upload de Arquivos
```
POST http://localhost:8000/webhook/tela2/upload/csv
POST http://localhost:8000/webhook/tela2/upload/xlsx
```

### Utilitários
```
GET http://localhost:8000/health
GET http://localhost:8000/docs
```

## 🔧 Instalação e Configuração

1. **Clone o repositório**
```bash
git clone <repository-url>
cd disparado_casos_testes
```

2. **Crie o ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp config/.env.example .env
# Edite o arquivo .env com suas credenciais
```

5. **Inicie o servidor**
```bash
python start_webhook_server.py
```

## 📱 Formatos de Entrada Suportados

### 1. JSON Estruturado
```json
{
  "phone_number": "+5511999999999",
  "messages": [
    {"text": "Primeira mensagem", "delay": 2},
    {"text": "Segunda mensagem", "delay": 3}
  ]
}
```

### 2. Texto Colado
```json
{
  "phone_number": "+5511999999999",
  "text_list": "Primeira mensagem\nSegunda mensagem\nTerceira mensagem"
}
```

### 3. CSV Inline
```json
{
  "phone_number": "+5511999999999",
  "csv_content": "text,delay\nPrimeira mensagem,2\nSegunda mensagem,3"
}
```

### 4. Formato Legado (N8N)
```json
{
  "phone_number": "+5511999999999",
  "body": {
    "method": "webhook",
    "testCases": ["Mensagem 1", "Mensagem 2"],
    "chatbotPhone": "+5511999999999"
  }
}
```

## 📄 Upload de Arquivos

### CSV
- Coluna obrigatória: `text` ou `message`
- Coluna opcional: `delay` (em segundos)
- Delimitadores suportados: `,`, `;`, `\t`

### XLSX
- Primeira planilha será processada
- Coluna obrigatória: `text` ou `message`
- Coluna opcional: `delay` (em segundos)

## 🧪 Testes

### Teste Automático
```bash
python test_webhook_integration.py
```

### Página de Teste Web
Abra `webhook_test_page.html` no navegador ou use:
```bash
python start_webhook_server.py
# Escolha 's' para abrir a página automaticamente
```

### Teste Manual com cURL
```bash
# Teste JSON
curl -X POST http://localhost:8000/webhook/tela2 \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+5511999999999",
    "messages": [
      {"text": "Teste via cURL", "delay": 2}
    ]
  }'

# Teste CSV Upload
curl -X POST http://localhost:8000/webhook/tela2/upload/csv \
  -F "phone_number=+5511999999999" \
  -F "file=@examples/messages.csv"
```

## ⚙️ Configuração da Evolution API

No arquivo `.env`, configure:

```env
# Evolution API Configuration
EVOLUTION_API_URL=https://evolution.etechats.com.br
EVOLUTION_API_KEY=sua-api-key-aqui
EVOLUTION_INSTANCE=sua-instancia-aqui

# Webhook Configuration
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000
```

## 🔍 Monitoramento e Logs

O sistema gera logs detalhados para:
- Recebimento de webhooks
- Processamento de arquivos
- Envio de mensagens
- Erros e exceções

Logs são exibidos no console durante a execução.

## 🛡️ Segurança

- Validação de entrada em todos os endpoints
- Sanitização de dados
- Timeouts configuráveis
- Rate limiting (pode ser configurado)
- Headers de segurança

## 📊 Limitações

- Máximo de 100 mensagens por lote
- Texto máximo de 4096 caracteres por mensagem
- Delay máximo de 60 segundos entre mensagens
- Arquivos CSV/XLSX até 10MB

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Verifique os logs do sistema
- Teste os endpoints com a página web incluída
- Consulte a documentação da API em `/docs`