# 📱 WhatsApp Message Dispatcher - Guia do Usuário

## 🚀 Como Iniciar o Sistema

### **Método 1: Script Python (Recomendado)**
```bash
python3 iniciar_sistema.py
```

### **Método 2: Script Bash (Linux/Mac)**
```bash
./start.sh
```

### **Método 3: Manual**
```bash
# Terminal 1 - Servidor API
python3 -m app.simple_webhook_server

# Terminal 2 - Servidor Web
python3 -m http.server 8080
```

## 🌐 Acessando o Sistema

Após iniciar, abra no navegador:
```
http://localhost:8080/whatsapp_sender_page.html
```

## 📋 Como Usar

### **1. 📝 Método "Colar Lista" (Mais Simples)**
1. Cole suas mensagens na caixa de texto (uma por linha)
2. Ajuste o delay entre mensagens (padrão: 2 segundos)
3. Clique em "Enviar Mensagens"

**Exemplo:**
```
Primeira mensagem
Segunda mensagem
Terceira mensagem
```

### **2. ⚙️ Método "JSON Avançado"**
Para controle individual de delays:

```json
[
  {"text": "Primeira mensagem", "delay": 2},
  {"text": "Segunda mensagem", "delay": 5},
  {"text": "Terceira mensagem", "delay": 1}
]
```

### **3. 📄 Método "Upload de Arquivo"**
- **CSV**: Colunas `text` (obrigatória) e `delay` (opcional)
- **XLSX**: Mesma estrutura do CSV

**Exemplo CSV:**
```csv
text,delay
Primeira mensagem,2
Segunda mensagem,3
Terceira mensagem,2
```

## 📱 Configuração do Número

O número padrão é **+556132073332** (já configurado para testes).

Para alterar, edite o arquivo `.env`:
```env
# Número padrão para testes
DEFAULT_PHONE_NUMBER=6132073332
```

## 🔧 Configurações Avançadas

### **Alterar Porta do Sistema**
No arquivo `.env`:
```env
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000
```

### **Configurar WhatsApp API**
```env
EVOLUTION_API_URL=https://evolution.etechats.com.br
EVOLUTION_API_KEY=sua-api-key
EVOLUTION_INSTANCE=sua-instancia
```

## 🛑 Como Parar o Sistema

- **Pressione `Ctrl+C`** no terminal onde iniciou o sistema
- Ou feche o terminal

## 📊 Monitoramento

### **Logs do Sistema**
Os logs aparecem no terminal onde você iniciou o sistema.

### **Status da API**
Verifique se está funcionando:
```bash
curl http://localhost:8000/health
```

### **Teste Rápido**
```bash
curl -X POST http://localhost:8000/webhook/tela2 \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+556132073332",
    "text_list": "Teste rápido via terminal"
  }'
```

## ❓ Solução de Problemas

### **Erro: "Porta já em uso"**
```bash
# Mata processos nas portas
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:8080 | xargs kill -9
```

### **Erro: "Módulo não encontrado"**
```bash
# Instala dependências
pip3 install fastapi uvicorn httpx pydantic-settings
```

### **Interface não carrega**
1. Verifique se ambos servidores estão rodando
2. Acesse: `http://localhost:8080/whatsapp_sender_page.html`
3. Verifique o console do navegador (F12)

### **Mensagens não enviam**
1. Verifique as configurações no `.env`
2. Teste a API diretamente: `curl http://localhost:8000/health`
3. Verifique os logs no terminal

## 🎯 Dicas de Uso

### **Para Listas Grandes**
- Use arquivos CSV/XLSX para mais de 20 mensagens
- Ajuste delays maiores para evitar bloqueios
- Teste com poucas mensagens primeiro

### **Delays Recomendados**
- **Mensagens curtas**: 2-3 segundos
- **Mensagens longas**: 3-5 segundos
- **Listas grandes**: 5-10 segundos

### **Formatos de Número**
Aceitos:
- `11999999999` (será convertido para +5511999999999)
- `5511999999999` (será convertido para +5511999999999)
- `+5511999999999` (formato completo)

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs no terminal
2. Teste com o número padrão primeiro
3. Use a interface web para testes visuais
4. Consulte este guia para soluções comuns

---

**🎉 Sistema pronto para uso! Envie suas mensagens com facilidade!**