# ========================================
# WHATSAPP MESSAGE SENDER - DOCKERFILE
# ========================================
# Multi-stage build para otimizar tamanho da imagem

# Stage 1: Base
FROM python:3.11-slim as base

# Metadados
LABEL maintainer="Marcu-Loreto"
LABEL description="WhatsApp Message Sender - Sistema de envio automatizado"
LABEL version="1.0.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Stage 2: Dependencies
FROM base as dependencies

# Instala dependências do sistema (se necessário)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas requirements para cache de layer
COPY requirements.txt .

# Instala dependências Python (se existirem)
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Stage 3: Application
FROM base as application

# Copia dependências instaladas
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Cria usuário não-root para segurança
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copia código da aplicação
COPY --chown=appuser:appuser . .

# Muda para usuário não-root
USER appuser

# Expõe portas
EXPOSE 8000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando padrão
CMD ["python3", "-m", "app.standalone_server"]
