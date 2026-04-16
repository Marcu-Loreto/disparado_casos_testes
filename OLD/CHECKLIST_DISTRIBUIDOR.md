# ✅ Checklist - Webhook Distribuidor

## 📋 Antes de Começar

- [ ] Arquivo `.env` configurado com credenciais corretas
- [ ] N8N está funcionando normalmente
- [ ] Você tem acesso à Evolution API
- [ ] Porta 9000 disponível (ou escolha outra)
- [ ] Porta 8000 disponível para o servidor Python

## 🚀 Passo 1: Iniciar o Sistema

### Opção A: Tudo de uma vez (Recomendado)

```bash
python3 START_COMPLETO.py
```

Aguarde ver:

- [ ] ✅ Distribuidor iniciado
- [ ] ✅ Servidor Python iniciado
- [ ] ✅ Interface Web iniciada

### Opção B: Passo a passo

Terminal 1:

```bash
python3 webhook_distributor.py
```

- [ ] Vê mensagem: "🔀 WEBHOOK DISTRIBUTOR - INICIADO"

Terminal 2:

```bash
python3 START.py
```

- [ ] Vê mensagem: "🚀 Servidor standalone iniciado"

## 🔧 Passo 2: Configurar Webhook na Evolution

Em outro terminal:

```bash
python3 configurar_webhook_distribuidor.py
```

Escolhas:

- [ ] Opção 1: Mesma VPS da Evolution (se estiver na VPS)
- [ ] Opção 2: Localhost com ngrok (se estiver testando local)
- [ ] Opção 3: Outro servidor (se distribuidor está em outro lugar)

Confirme:

- [ ] Digite 's' para confirmar
- [ ] Vê mensagem: "✅ WEBHOOK CONFIGURADO COM SUCESSO!"

## 🧪 Passo 3: Testar

```bash
python3 testar_distribuidor.py
```

Verificações:

- [ ] ✅ Distribuidor respondeu
- [ ] ✅ Distribuidor está saudável
- [ ] ✅ Servidor Python está rodando

## 🔍 Passo 4: Verificações Manuais

### 4.1 Health Check do Distribuidor

```bash
curl http://localhost:9000/health
```

- [ ] Retorna status "healthy"
- [ ] Mostra 2 destinos configurados

### 4.2 Health Check do Python

```bash
curl http://localhost:8000/health
```

- [ ] Retorna status "healthy"

### 4.3 Webhook na Evolution

```bash
curl -H "apikey: SUA_API_KEY" \
  https://evolution.etechats.com.br/webhook/find/TESTE_AUTO_MGI
```

- [ ] Mostra URL do distribuidor
- [ ] URL contém ":9000/webhook/distributor"

## 📱 Passo 5: Teste Real com WhatsApp

### 5.1 Acesse a Interface

```
http://localhost:8080/whatsapp_final.html
```

- [ ] Interface carrega corretamente
- [ ] Vê 3 abas: Enviar, Recepção, Histórico

### 5.2 Envie Mensagem de Teste

Na aba "Enviar":

- [ ] Cole um número de teste (ex: +5519993388617)
- [ ] Cole uma mensagem de teste
- [ ] Clique em "Enviar Mensagens"
- [ ] Vê mensagem de sucesso

### 5.3 Verifique os Logs

**Logs do Distribuidor:**

- [ ] Vê: "📨 Webhook recebido da Evolution API"
- [ ] Vê: "✅ N8N: OK"
- [ ] Vê: "✅ Python Local: OK"

**Logs do Servidor Python:**

- [ ] Vê: "Mensagem recebida da Evolution API"
- [ ] Vê: "Resposta processada e salva"

### 5.4 Responda pelo WhatsApp

- [ ] Responda a mensagem pelo WhatsApp
- [ ] Aguarde alguns segundos

### 5.5 Verifique a Recepção

**Na Interface (aba Recepção):**

- [ ] Contador incrementa (1/1, 2/2, etc)
- [ ] Última resposta aparece destacada
- [ ] Tabela mostra todas as respostas

**No Sistema de Arquivos:**

```bash
ls -la sessions/
```

- [ ] Existe arquivo `respostas_*.csv`
- [ ] Arquivo contém as respostas

**No N8N:**

- [ ] N8N também recebeu a mensagem
- [ ] Workflow do N8N funcionou normalmente

## ✅ Checklist Final

- [ ] Distribuidor está rodando e saudável
- [ ] Servidor Python está rodando e saudável
- [ ] Webhook configurado na Evolution API
- [ ] Mensagens de teste enviadas com sucesso
- [ ] Respostas recebidas no Python
- [ ] Respostas recebidas no N8N
- [ ] CSVs sendo gerados corretamente
- [ ] Interface web funcionando

## 🎉 Tudo Funcionando!

Se todos os itens acima estão marcados, seu sistema está 100% operacional!

## 🔧 Se Algo Falhou

### Distribuidor não inicia

- Verifique se porta 9000 está livre: `lsof -i :9000`
- Mate processo se necessário: `kill -9 <PID>`

### Python não inicia

- Verifique se porta 8000 está livre: `lsof -i :8000`
- Verifique dependências: `python3 -c "from config.settings import Settings"`

### Webhook não configura

- Verifique credenciais no `.env`
- Teste conexão com Evolution API
- Verifique se instância existe e está conectada

### N8N não recebe

- Verifique URL do N8N no `.env`
- Teste manualmente com curl
- Veja logs do distribuidor

### Python não recebe

- Verifique se servidor está rodando
- Veja logs do servidor Python
- Veja logs do distribuidor

## 📞 Próximos Passos

Após tudo funcionando:

1. **Produção**: Configure para iniciar automaticamente
   - Crie serviço systemd
   - Configure supervisor
   - Use PM2

2. **Monitoramento**: Configure alertas
   - Health checks periódicos
   - Logs centralizados
   - Alertas de falha

3. **Backup**: Configure backup automático
   - CSVs em cloud storage
   - Backup do banco SQLite
   - Logs históricos

4. **Escalabilidade**: Se precisar de mais capacidade
   - Load balancer para distribuidor
   - Múltiplas instâncias Python
   - Redis para cache

## 🎊 Parabéns!

Você configurou com sucesso um sistema de webhook distribuidor que permite N8N e Python receberem as mesmas mensagens do WhatsApp simultaneamente!
