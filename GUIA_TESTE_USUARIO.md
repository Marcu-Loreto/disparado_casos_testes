# 🧪 GUIA DE TESTE DE USUÁRIO

## 📋 Pré-requisitos

- [ ] Python 3.x instalado
- [ ] Servidor rodando (`python3 START.py`)
- [ ] Navegador aberto em `http://localhost:8080/whatsapp_final.html`

---

## 🎯 TESTE 1: Envio de Mensagens

### Objetivo

Verificar se o sistema envia mensagens e cria sessão corretamente.

### Passos

1. **Acesse a aba "📤 Enviar"**
   - Deve estar ativa por padrão

2. **Preencha o número**
   - Campo: "Número do WhatsApp"
   - Digite: `19993388617` (sem +55)
   - ✅ Verificar: Prefixo +55 aparece automaticamente

3. **Cole as mensagens de teste**
   - Campo: "Cole suas mensagens"
   - Cole:
     ```
     🧪 Teste 1 - Primeira mensagem
     📱 Teste 2 - Segunda mensagem
     ✅ Teste 3 - Terceira mensagem
     ```

4. **Clique em "📤 Enviar Mensagens"**
   - ✅ Botão muda para "⏳ Enviando..."
   - ✅ Aguarde 6-9 segundos (3 msgs x 3 seg delay)

5. **Verifique a resposta**
   - ✅ Mensagem verde de sucesso
   - ✅ Mostra: "3 mensagens enviadas!"
   - ✅ Mostra: Session ID
   - ✅ Mostra: Nome do CSV
   - ✅ Botão "📥 Ver Recepção" aparece

### Resultado Esperado

```
✅ 3 mensagens enviadas!
🆔 Sessão: 5519993388617_20260404_123045
📄 CSV: respostas_5519993388617_20260404_123045.csv
[📥 Ver Recepção]
```

---

## 🎯 TESTE 2: Visualização de Recepção

### Objetivo

Verificar se a aba de recepção mostra o progresso corretamente.

### Passos

1. **Clique no botão "📥 Ver Recepção"**
   - Ou clique na aba "📥 Recepção"

2. **Verifique o cabeçalho de progresso**
   - ✅ Contador mostra: `0/3`
   - ✅ Barra de progresso em 0%
   - ✅ Status: "🔄 Recebendo respostas..."

3. **Verifique a seção "Última Resposta"**
   - ✅ Mostra: "Nenhuma resposta recebida ainda"

4. **Verifique o botão de atualização**
   - ✅ Botão "🔄 Atualizar" visível

### Resultado Esperado

```
┌─────────────────────────────────────┐
│ 0/3        [░░░░░░░░░░░░] 0%       │
│ 🔄 Recebendo respostas...           │
└─────────────────────────────────────┘

📨 Última Resposta Recebida
┌─────────────────────────────────────┐
│ Nenhuma resposta recebida ainda     │
└─────────────────────────────────────┘
```

---

## 🎯 TESTE 3: Simulação de Respostas

### Objetivo

Simular recebimento de respostas e verificar atualização em tempo real.

### Passos

1. **Abra um novo terminal** (mantenha o servidor rodando)

2. **Execute o script de simulação**

   ```bash
   python3 test_complete_system.py
   ```

3. **Volte para o navegador**
   - A página deve atualizar automaticamente a cada 3 segundos

4. **Observe as mudanças**
   - ✅ Contador incrementa: `1/3` → `2/3` → `3/3`
   - ✅ Barra de progresso avança: 33% → 66% → 100%
   - ✅ Última resposta atualiza com cada nova mensagem
   - ✅ Status muda para: "✅ Task Completa!"

5. **Verifique a tabela de respostas**
   - ✅ Tabela aparece abaixo
   - ✅ Mostra 3 linhas (uma por resposta)
   - ✅ Colunas: #, Data/Hora, Número, Resposta

### Resultado Esperado

```
┌─────────────────────────────────────┐
│ 3/3        [██████████████] 100%   │
│ ✅ Task Completa!                   │
└─────────────────────────────────────┘

📨 Última Resposta Recebida
┌─────────────────────────────────────┐
│ Resposta 3: Recebi 'Teste 3...'    │
│ 📞 +5519993388617 • 🕐 12:30:45    │
└─────────────────────────────────────┘

┌───┬──────────────┬─────────────────┬──────────────┐
│ # │ Data/Hora    │ Número          │ Resposta     │
├───┼──────────────┼─────────────────┼──────────────┤
│ 1 │ 12:30:15     │ +5519993388617  │ Resposta 1...│
│ 2 │ 12:30:30     │ +5519993388617  │ Resposta 2...│
│ 3 │ 12:30:45     │ +5519993388617  │ Resposta 3...│
└───┴──────────────┴─────────────────┴──────────────┘
```

---

## 🎯 TESTE 4: Histórico de Sessões

### Objetivo

Verificar se o histórico mostra todas as sessões e permite download.

### Passos

1. **Clique na aba "📁 Histórico"**

2. **Clique em "🔄 Atualizar Histórico"**

3. **Verifique os cards de sessão**
   - ✅ Pelo menos 1 card aparece
   - ✅ Card mostra:
     - Número de telefone
     - Session ID
     - Nome do CSV
     - Quantidade de respostas
     - Status
     - Botão "📥 Baixar CSV"

4. **Clique em "📥 Baixar CSV"**
   - ✅ Download inicia automaticamente
   - ✅ Arquivo salvo: `respostas_*.csv`

5. **Abra o CSV baixado**
   - ✅ Abre no Excel/LibreOffice
   - ✅ Contém cabeçalho: Timestamp, Phone Number, Response, Session ID
   - ✅ Contém 3 linhas de dados

### Resultado Esperado

```
┌─────────────────────────────────────┐
│ 📱 +5519993388617          3 respostas│
│ 🆔 5519993388617_20260404_123045    │
│ 📄 respostas_5519993388617_...csv   │
│ 🎯 Status: completed                │
│ [📥 Baixar CSV]                     │
└─────────────────────────────────────┘
```

---

## 🎯 TESTE 5: Múltiplas Sessões

### Objetivo

Verificar se o sistema gerencia múltiplas sessões corretamente.

### Passos

1. **Volte para aba "📤 Enviar"**

2. **Envie novas mensagens**
   - Número: `19993388617` (mesmo número)
   - Mensagens:
     ```
     🔥 Nova sessão - Teste 1
     ⚡ Nova sessão - Teste 2
     ```

3. **Verifique que nova sessão foi criada**
   - ✅ Novo Session ID (timestamp diferente)
   - ✅ Novo CSV gerado

4. **Vá para "📥 Recepção"**
   - ✅ Mostra progresso da sessão mais recente
   - ✅ Contador: `0/2`

5. **Vá para "📁 Histórico"**
   - ✅ Mostra 2 sessões agora
   - ✅ Cada uma com seu CSV próprio

### Resultado Esperado

```
Histórico mostra:

┌─────────────────────────────────────┐
│ Sessão 1: 3 respostas (completed)   │
│ CSV: respostas_..._123045.csv       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Sessão 2: 0 respostas (active)      │
│ CSV: respostas_..._150230.csv       │
└─────────────────────────────────────┘
```

---

## 🎯 TESTE 6: Filtro de Números

### Objetivo

Verificar se o sistema ignora mensagens de números não registrados.

### Passos

1. **Simule mensagem de número diferente**

   ```bash
   curl -X POST http://localhost:8000/webhook/evolution/messages \
     -H "Content-Type: application/json" \
     -d '{
       "event": "messages.upsert",
       "data": {
         "key": {
           "remoteJid": "5511999999999@s.whatsapp.net",
           "fromMe": false
         },
         "message": {
           "conversation": "Mensagem de número não registrado"
         }
       }
     }'
   ```

2. **Verifique a resposta**
   - ✅ Status: "ignored"
   - ✅ Mensagem: "Mensagem ignorada (não é de número ativo)"

3. **Verifique na interface**
   - ✅ Contador NÃO incrementa
   - ✅ Última resposta NÃO atualiza
   - ✅ Tabela NÃO adiciona linha

### Resultado Esperado

```json
{
  "status": "ignored",
  "message": "Mensagem ignorada (não é de número ativo)"
}
```

---

## 🎯 TESTE 7: Auto-Refresh

### Objetivo

Verificar se a interface atualiza automaticamente.

### Passos

1. **Esteja na aba "📥 Recepção"**

2. **Envie uma resposta via API** (outro terminal)

   ```bash
   curl -X POST http://localhost:8000/webhook/evolution/messages \
     -H "Content-Type: application/json" \
     -d '{
       "event": "messages.upsert",
       "data": {
         "key": {
           "remoteJid": "5519993388617@s.whatsapp.net",
           "fromMe": false
         },
         "message": {
           "conversation": "Resposta de teste auto-refresh"
         }
       }
     }'
   ```

3. **Observe a interface** (NÃO clique em atualizar)
   - ✅ Após 3 segundos, contador incrementa automaticamente
   - ✅ Última resposta atualiza automaticamente
   - ✅ Tabela adiciona nova linha automaticamente

4. **Mude para outra aba**
   - ✅ Auto-refresh para quando sai da aba "Recepção"

5. **Volte para aba "Recepção"**
   - ✅ Auto-refresh reinicia automaticamente

### Resultado Esperado

Interface atualiza sozinha a cada 3 segundos quando na aba "Recepção".

---

## 🎯 TESTE 8: Responsividade Mobile

### Objetivo

Verificar se a interface funciona em dispositivos móveis.

### Passos

1. **Abra DevTools** (F12)

2. **Ative modo responsivo** (Ctrl+Shift+M)

3. **Selecione dispositivo**
   - iPhone 12 Pro
   - Samsung Galaxy S20
   - iPad

4. **Teste todas as abas**
   - ✅ Layout se adapta
   - ✅ Botões são clicáveis
   - ✅ Texto é legível
   - ✅ Tabelas têm scroll horizontal

5. **Teste formulário de envio**
   - ✅ Campos são acessíveis
   - ✅ Teclado virtual não cobre botões

### Resultado Esperado

Interface totalmente funcional em telas pequenas.

---

## 📊 CHECKLIST FINAL

### Funcionalidades Básicas

- [ ] Envio de mensagens funciona
- [ ] Sessão é criada corretamente
- [ ] CSV é gerado com timestamp
- [ ] Número é registrado para receber respostas

### Recepção

- [ ] Contador incremental funciona (X/Total)
- [ ] Barra de progresso atualiza
- [ ] Última resposta é exibida
- [ ] Status "Task Completa" aparece
- [ ] Tabela de respostas é populada
- [ ] Auto-refresh funciona (3 segundos)

### Filtros

- [ ] Aceita respostas do número correto
- [ ] Ignora mensagens de outros números
- [ ] Ignora mensagens enviadas por você

### Histórico

- [ ] Lista todas as sessões
- [ ] Mostra informações corretas
- [ ] Download de CSV funciona
- [ ] CSVs contêm dados corretos

### Interface

- [ ] Navegação entre abas funciona
- [ ] Design é responsivo
- [ ] Cores e ícones são adequados
- [ ] Mensagens de erro são claras

### Performance

- [ ] Carregamento é rápido
- [ ] Atualizações são suaves
- [ ] Não trava com muitas respostas
- [ ] Auto-refresh não sobrecarrega

---

## 🐛 Problemas Comuns

### "Nenhuma sessão ativa"

**Causa:** Não enviou mensagens ainda
**Solução:** Vá para aba "Enviar" e envie mensagens primeiro

### Contador não atualiza

**Causa:** Auto-refresh não está ativo
**Solução:** Saia e volte para aba "Recepção"

### CSV não baixa

**Causa:** Bloqueador de pop-ups
**Solução:** Permita downloads do localhost

### Interface não carrega

**Causa:** Servidor não está rodando
**Solução:** Execute `python3 START.py`

---

## ✅ TESTE CONCLUÍDO

Se todos os testes passaram:

- ✅ Sistema está 100% funcional
- ✅ Pronto para uso em produção
- ✅ Pode configurar webhook real da Evolution API

**Próximo passo:** Configure o webhook para receber respostas reais do WhatsApp!

Veja: `CONFIGURAR_WEBHOOK_EVOLUTION.md`
