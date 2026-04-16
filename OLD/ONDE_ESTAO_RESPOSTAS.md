# 📊 ONDE AS RESPOSTAS ESTÃO SENDO ARMAZENADAS?

## 🎯 Resposta Rápida

Por padrão, as respostas estão sendo salvas em:

```
📁 responses.csv
```

Localização: **Raiz do projeto**

---

## 📂 Opções de Armazenamento

### 1. **CSV Local** (Padrão - Ativo)

✅ **Vantagens:**

- Funciona imediatamente
- Não precisa configuração
- Fácil de visualizar (Excel, LibreOffice)
- Backup simples

📁 **Arquivo:** `responses.csv`

📊 **Formato:**

```csv
Timestamp,Phone Number,Response
2026-04-04 10:30:15,+556132073332,Olá, recebi sua mensagem!
2026-04-04 10:31:22,+556132073332,Tudo bem, obrigado!
```

🔍 **Ver respostas:**

```bash
# Via API
curl http://localhost:8000/responses

# Via arquivo
cat responses.csv

# Abrir no Excel/LibreOffice
xdg-open responses.csv
```

---

### 2. **Google Sheets** (Requer configuração)

📊 **Planilha:**

- ID: `1xpK1xFnkETsLBk5jCOnEzV9xrplSPigmlaATUZweTCM`
- Sheet ID: `882495635`

⚙️ **Como ativar:**

1. Instale dependências:

```bash
pip install google-auth google-api-python-client
```

2. Configure credenciais (veja seção abaixo)

3. Altere em `app/standalone_server.py`:

```python
sheets_handler = GoogleSheetsHandler(storage_type="sheets")
```

---

### 3. **SQLite** (Banco de dados local)

🗄️ **Banco:** `responses.db`

⚙️ **Como ativar:**

Altere em `app/standalone_server.py`:

```python
sheets_handler = GoogleSheetsHandler(storage_type="sqlite")
```

🔍 **Ver respostas:**

```bash
sqlite3 responses.db "SELECT * FROM responses;"
```

---

## 🔍 Como Ver as Respostas

### Opção 1: Via API (Recomendado)

```bash
curl http://localhost:8000/responses
```

Resposta:

```json
{
  "status": "success",
  "responses": [
    {
      "Timestamp": "2026-04-04 10:30:15",
      "Phone Number": "+556132073332",
      "Response": "Olá, recebi sua mensagem!"
    }
  ],
  "count": 1,
  "storage": "csv",
  "file": "responses.csv"
}
```

### Opção 2: Abrir Arquivo CSV

```bash
# Linux
xdg-open responses.csv

# Mac
open responses.csv

# Windows
start responses.csv

# Ou use Excel/LibreOffice/Google Sheets
```

### Opção 3: Via Terminal

```bash
# Ver todas
cat responses.csv

# Ver últimas 10
tail -10 responses.csv

# Buscar por número
grep "+556132073332" responses.csv

# Contar respostas
wc -l responses.csv
```

---

## ⚙️ Configurar Google Sheets (Opcional)

### Passo 1: Criar Projeto no Google Cloud

1. Acesse: https://console.cloud.google.com
2. Crie novo projeto: "WhatsApp Responses"
3. Ative **Google Sheets API**

### Passo 2: Criar Service Account

1. Vá em **APIs & Services** → **Credentials**
2. **Create Credentials** → **Service Account**
3. Nome: "whatsapp-bot"
4. Clique em **Create and Continue**
5. Role: **Editor**
6. Clique em **Done**

### Passo 3: Baixar Credenciais

1. Clique na service account criada
2. Aba **Keys**
3. **Add Key** → **Create new key**
4. Tipo: **JSON**
5. Salve como `credentials.json` na raiz do projeto

### Passo 4: Compartilhar Planilha

1. Abra sua planilha do Google Sheets
2. Clique em **Compartilhar**
3. Adicione o email da service account
   - Está em `credentials.json`: `"client_email"`
   - Exemplo: `whatsapp-bot@projeto.iam.gserviceaccount.com`
4. Permissão: **Editor**
5. Clique em **Compartilhar**

### Passo 5: Criar Aba "Respostas"

1. Na planilha, crie uma nova aba chamada **"Respostas"**
2. Adicione cabeçalhos na primeira linha:
   - A1: `Timestamp`
   - B1: `Phone Number`
   - C1: `Response`

### Passo 6: Ativar no Código

Edite `app/standalone_server.py`:

```python
# Linha 17, altere de:
sheets_handler = GoogleSheetsHandler()

# Para:
sheets_handler = GoogleSheetsHandler(storage_type="sheets")
```

Reinicie o servidor:

```bash
pkill -f standalone_server
python3 START.py
```

---

## 📊 Estrutura dos Dados

Independente do método de armazenamento, os dados têm esta estrutura:

| Campo        | Tipo   | Exemplo             | Descrição             |
| ------------ | ------ | ------------------- | --------------------- |
| Timestamp    | String | 2026-04-04 10:30:15 | Data/hora da resposta |
| Phone Number | String | +556132073332       | Número que respondeu  |
| Response     | String | Olá, recebi!        | Texto da mensagem     |

---

## 🔄 Migrar Entre Formatos

### CSV → Google Sheets

1. Abra `responses.csv` no Excel/LibreOffice
2. Copie todos os dados
3. Cole na planilha do Google Sheets
4. Ou use importação automática do Google Sheets

### CSV → SQLite

```python
import csv
import sqlite3

conn = sqlite3.connect('responses.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        phone_number TEXT,
        response TEXT
    )
''')

with open('responses.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute(
            'INSERT INTO responses (timestamp, phone_number, response) VALUES (?, ?, ?)',
            (row['Timestamp'], row['Phone Number'], row['Response'])
        )

conn.commit()
conn.close()
```

---

## 📈 Estatísticas

### Ver total de respostas:

```bash
# CSV
wc -l responses.csv

# API
curl http://localhost:8000/responses | jq '.count'
```

### Respostas por número:

```bash
# CSV
cut -d',' -f2 responses.csv | sort | uniq -c
```

### Últimas 5 respostas:

```bash
# CSV
tail -5 responses.csv

# API
curl http://localhost:8000/responses | jq '.responses[-5:]'
```

---

## 🗑️ Limpar Respostas

### Backup antes de limpar:

```bash
cp responses.csv responses_backup_$(date +%Y%m%d).csv
```

### Limpar arquivo:

```bash
# Manter cabeçalho
head -1 responses.csv > responses_temp.csv
mv responses_temp.csv responses.csv

# Ou deletar tudo
rm responses.csv
# Será recriado automaticamente
```

---

## 🎯 Resumo

| Método            | Arquivo/Local   | Configuração         | Recomendado Para           |
| ----------------- | --------------- | -------------------- | -------------------------- |
| **CSV**           | `responses.csv` | ✅ Nenhuma           | Desenvolvimento, testes    |
| **Google Sheets** | Planilha online | ⚙️ API + Credenciais | Produção, compartilhamento |
| **SQLite**        | `responses.db`  | ✅ Nenhuma           | Produção local, queries    |

---

## 📞 Endpoints Úteis

```bash
# Ver todas as respostas
curl http://localhost:8000/responses

# Ver números ativos
curl http://localhost:8000/active-numbers

# Health check
curl http://localhost:8000/health

# Info do servidor
curl http://localhost:8000/
```

---

## 🎉 Pronto!

Suas respostas estão sendo salvas em **`responses.csv`** por padrão!

Para visualizar:

```bash
cat responses.csv
```

Ou via API:

```bash
curl http://localhost:8000/responses
```
