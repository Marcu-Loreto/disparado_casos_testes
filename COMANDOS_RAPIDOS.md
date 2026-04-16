# ⚡ Comandos Rápidos

## 🚀 Iniciar Sistema

```bash
# Tudo de uma vez (recomendado)
python3 START_COMPLETO.py

# Ou separadamente:
python3 webhook_distribuidor.py  # Terminal 1
python3 START.py                 # Terminal 2
```

## 🔧 Configurar

```bash
# Configurar webhook na Evolution
python3 configurar_webhook_distribuidor.py
```

## 🧪 Testar

```bash
# Teste completo
python3 testar_distribuidor.py

# Health checks
curl http://localhost:9000/health  # Distribuidor
curl http://localhost:8000/health  # Python
```

## 🔍 Monitorar

```bash
# Ver sessões ativas
curl http://localhost:8000/sessions

# Ver respostas
curl http://localhost:8000/responses

# Ver números ativos
curl http://localhost:8000/active-numbers
```

## 📊 Exportar

```bash
# Exportar para CSV
curl http://localhost:8000/export

# Ver histórico de exportações
curl http://localhost:8000/export-history
```

## 🌐 Acessar Interface

```bash
# Abrir no navegador
xdg-open http://localhost:8080/whatsapp_final.html

# Ou acesse manualmente:
# http://localhost:8080/whatsapp_final.html
```

## 🔄 Verificar Webhook Evolution

```bash
# Ver webhook configurado
curl -H "apikey: SUA_API_KEY" \
  https://evolution.etechats.com.br/webhook/find/TESTE_AUTO_MGI
```

## 🛑 Parar Sistema

```bash
# Se usou START_COMPLETO.py
Ctrl+C

# Se iniciou separadamente
Ctrl+C em cada terminal
```

## 🔧 Troubleshooting

```bash
# Ver processos nas portas
lsof -i :9000  # Distribuidor
lsof -i :8000  # Python
lsof -i :8080  # Interface

# Matar processo
kill -9 <PID>

# Ver logs em tempo real
tail -f logs/*.log  # Se tiver logs configurados
```

## 📁 Ver Arquivos

```bash
# Ver CSVs gerados
ls -lh sessions/

# Ver último CSV
ls -lt sessions/ | head -2

# Ver conteúdo do último CSV
cat $(ls -t sessions/*.csv | head -1)
```

## 🔍 Debug

```bash
# Testar configurações
python3 -c "from config.settings import Settings; s = Settings(); print(s.WEBHOOK_RECEPTION_URL)"

# Testar imports
python3 -c "from app.standalone_server import *; print('OK')"

# Testar distribuidor
python3 -c "import webhook_distributor; print('OK')"
```

## 📊 Estatísticas

```bash
# Contar CSVs
ls sessions/*.csv | wc -l

# Contar respostas no último CSV
wc -l $(ls -t sessions/*.csv | head -1)

# Ver tamanho total dos CSVs
du -sh sessions/
```

## 🔄 Reiniciar

```bash
# Parar tudo
pkill -f webhook_distributor
pkill -f standalone_server
pkill -f "http.server 8080"

# Iniciar novamente
python3 START_COMPLETO.py
```

## 📝 Logs Úteis

```bash
# Ver últimas 50 linhas de log (se configurado)
tail -50 logs/app.log

# Seguir logs em tempo real
tail -f logs/app.log

# Buscar erros
grep -i error logs/app.log
```

## 🎯 Teste Rápido Completo

```bash
# 1. Inicia
python3 START_COMPLETO.py &

# 2. Aguarda 5 segundos
sleep 5

# 3. Testa
python3 testar_distribuidor.py

# 4. Verifica health
curl http://localhost:9000/health && echo ""
curl http://localhost:8000/health && echo ""

# 5. Abre interface
xdg-open http://localhost:8080/whatsapp_final.html
```

## 🔐 Segurança

```bash
# Ver permissões dos arquivos
ls -la *.py

# Tornar executável
chmod +x webhook_distribuidor.py
chmod +x START_COMPLETO.py

# Ver .env (cuidado!)
cat .env | grep -v "KEY\|TOKEN"  # Oculta chaves
```

## 📦 Backup

```bash
# Backup dos CSVs
tar -czf backup_sessions_$(date +%Y%m%d).tar.gz sessions/

# Backup do banco
cp whatsapp_responses.db whatsapp_responses_$(date +%Y%m%d).db.bak

# Backup completo
tar -czf backup_completo_$(date +%Y%m%d).tar.gz \
  sessions/ \
  whatsapp_responses.db \
  .env
```

## 🚀 Deploy

```bash
# Criar serviço systemd (exemplo)
sudo nano /etc/systemd/system/webhook-distribuidor.service

# Recarregar systemd
sudo systemctl daemon-reload

# Iniciar serviço
sudo systemctl start webhook-distribuidor

# Habilitar no boot
sudo systemctl enable webhook-distribuidor

# Ver status
sudo systemctl status webhook-distribuidor
```

## 📊 Monitoramento Contínuo

```bash
# Watch health checks
watch -n 5 'curl -s http://localhost:9000/health | jq'

# Watch sessões
watch -n 10 'curl -s http://localhost:8000/sessions | jq'

# Watch processos
watch -n 5 'ps aux | grep -E "webhook|standalone"'
```
