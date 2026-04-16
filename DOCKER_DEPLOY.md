# 🐳 GUIA DE DEPLOY COM DOCKER

## 📋 Pré-requisitos

### 1. Instalar Docker

#### Linux (Ubuntu/Debian):

```bash
# Atualizar pacotes
sudo apt-get update

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Reiniciar sessão ou executar
newgrp docker
```

#### macOS:

```bash
# Instalar Docker Desktop
brew install --cask docker
```

#### Windows:

- Baixe Docker Desktop: https://www.docker.com/products/docker-desktop

### 2. Instalar Docker Compose

```bash
# Verificar se já está instalado
docker-compose --version

# Se não estiver, instalar
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

---

## 🚀 Deploy Rápido

### 1. Configurar Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env
```

**Preencha obrigatoriamente:**

- `EVOLUTION_API_URL` - URL da sua Evolution API
- `EVOLUTION_API_KEY` - Chave de API
- `EVOLUTION_INSTANCE` - Nome da instância

### 2. Construir e Iniciar

```bash
# Construir imagem
docker-compose build

# Iniciar containers
docker-compose up -d

# Verificar status
docker-compose ps
```

### 3. Testar Sistema

```bash
# Executar script de teste
chmod +x test_docker.sh
./test_docker.sh
```

---

## 📊 Comandos Úteis

### Gerenciamento de Containers

```bash
# Iniciar containers
docker-compose up -d

# Parar containers
docker-compose down

# Reiniciar containers
docker-compose restart

# Ver status
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f whatsapp-api
docker-compose logs -f whatsapp-web
```

### Manutenção

```bash
# Reconstruir imagem (após mudanças no código)
docker-compose build --no-cache

# Reiniciar após rebuild
docker-compose up -d --force-recreate

# Limpar containers parados
docker-compose down --remove-orphans

# Limpar tudo (containers, volumes, imagens)
docker-compose down -v --rmi all
```

### Monitoramento

```bash
# Ver uso de recursos
docker stats

# Inspecionar container
docker inspect whatsapp-sender-api

# Executar comando dentro do container
docker-compose exec whatsapp-api bash

# Ver health check
docker inspect --format='{{.State.Health.Status}}' whatsapp-sender-api
```

---

## 🌐 Acessar Sistema

Após iniciar os containers:

- **Interface Web**: http://localhost:8080/whatsapp_simple.html
- **API WhatsApp**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

---

## 🔧 Configuração Avançada

### Alterar Portas

Edite `docker-compose.yml`:

```yaml
ports:
  - "9000:8000" # API na porta 9000
  - "9080:8080" # Web na porta 9080
```

### Limites de Recursos

Já configurado em `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: "1"
      memory: 512M
```

### Persistência de Logs

Logs são salvos em `./logs/` automaticamente.

```bash
# Ver logs persistidos
ls -lh logs/

# Limpar logs antigos
rm -rf logs/*.log
```

---

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs detalhados
docker-compose logs whatsapp-api

# Verificar configuração
docker-compose config

# Reconstruir do zero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### API não responde

```bash
# Verificar se container está rodando
docker-compose ps

# Verificar health check
curl http://localhost:8000/health

# Ver logs em tempo real
docker-compose logs -f whatsapp-api

# Reiniciar serviço
docker-compose restart whatsapp-api
```

### Erro de permissão

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Reiniciar sessão
newgrp docker

# Ou executar com sudo
sudo docker-compose up -d
```

### Porta já em uso

```bash
# Verificar o que está usando a porta
sudo lsof -i :8000
sudo lsof -i :8080

# Matar processo
sudo kill -9 <PID>

# Ou alterar porta no docker-compose.yml
```

---

## 🚀 Deploy em Produção

### 1. Servidor VPS/Cloud

```bash
# Conectar ao servidor
ssh user@seu-servidor.com

# Clonar repositório
git clone https://github.com/Marcu-Loreto/disparado_casos_testes.git
cd disparado_casos_testes

# Configurar .env
cp .env.example .env
nano .env

# Iniciar
docker-compose up -d
```

### 2. Usar Nginx como Proxy Reverso

Crie `/etc/nginx/sites-available/whatsapp-sender`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/whatsapp-sender /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. SSL com Let's Encrypt

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovação automática já está configurada
```

### 4. Iniciar Automaticamente no Boot

```bash
# Criar serviço systemd
sudo nano /etc/systemd/system/whatsapp-sender.service
```

```ini
[Unit]
Description=WhatsApp Message Sender
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/caminho/para/disparado_casos_testes
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl enable whatsapp-sender
sudo systemctl start whatsapp-sender
```

---

## 📊 Monitoramento em Produção

### Logs Centralizados

```bash
# Ver logs de todos os serviços
docker-compose logs -f --tail=100

# Exportar logs
docker-compose logs > logs_$(date +%Y%m%d).txt
```

### Alertas de Health Check

```bash
# Script de monitoramento (cron)
#!/bin/bash
if ! curl -f http://localhost:8000/health &> /dev/null; then
    echo "API DOWN!" | mail -s "WhatsApp Sender Alert" admin@email.com
    docker-compose restart whatsapp-api
fi
```

### Backup Automático

```bash
# Backup do .env e logs
tar -czf backup_$(date +%Y%m%d).tar.gz .env logs/
```

---

## 🎯 Checklist de Deploy

- [ ] Docker e Docker Compose instalados
- [ ] Arquivo .env configurado com credenciais
- [ ] Portas 8000 e 8080 disponíveis
- [ ] Firewall configurado (se necessário)
- [ ] Teste executado com sucesso (`./test_docker.sh`)
- [ ] Containers rodando (`docker-compose ps`)
- [ ] Health check OK (`curl http://localhost:8000/health`)
- [ ] Interface acessível no navegador
- [ ] Logs sendo gerados corretamente
- [ ] Backup configurado (produção)
- [ ] Monitoramento ativo (produção)

---

## 📞 Suporte

- **Documentação**: README.md
- **Guia do Usuário**: README_USUARIO.md
- **Issues**: https://github.com/Marcu-Loreto/disparado_casos_testes/issues

---

## 🎉 Pronto!

Seu sistema WhatsApp Message Sender está rodando em Docker!

**URLs:**

- 🌐 Interface: http://localhost:8080/whatsapp_simple.html
- 📡 API: http://localhost:8000
- ❤️ Health: http://localhost:8000/health
