#!/usr/bin/env python3
"""
Servidor webhook para receber listas de mensagens e processar diferentes formatos.
"""

import asyncio
import logging
import json
import csv
import io
import pandas as pd
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from app.workflow import WorkflowExecutor
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models para validação
class MessageItem(BaseModel):
    text: str = Field(..., description="Texto da mensagem")
    delay: Optional[int] = Field(default=2, description="Delay em segundos entre mensagens")

class WebhookPayload(BaseModel):
    phone_number: str = Field(..., description="Número do telefone para envio")
    messages: List[MessageItem] = Field(..., description="Lista de mensagens")
    format_type: str = Field(default="json", description="Tipo do formato: json, csv, xlsx, paste")

# FastAPI app
app = FastAPI(
    title="WhatsApp Message Dispatcher",
    description="Webhook para receber e processar listas de mensagens para WhatsApp",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global settings
settings = Settings()


@app.get("/")
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "message": "WhatsApp Message Dispatcher API",
        "version": "1.0.0",
        "endpoints": {
            "webhook": "/webhook/tela2",
            "upload_csv": "/webhook/tela2/upload/csv",
            "upload_xlsx": "/webhook/tela2/upload/xlsx",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2026-04-01T12:00:00Z"}


@app.post("/webhook/tela2")
async def webhook_tela2(request: Request):
    """
    Webhook principal que aceita diferentes formatos de dados.
    
    Formatos aceitos:
    - JSON com lista de mensagens
    - Texto colado (uma mensagem por linha)
    - Referência a arquivo CSV/XLSX
    """
    try:
        # Obtém o payload
        payload = await request.json()
        logger.info(f"Webhook recebido: {payload}")
        
        # Processa o payload
        processed_data = await process_webhook_payload(payload)
        
        # Executa o workflow
        result = await execute_message_workflow(processed_data)
        
        return {
            "status": "success",
            "message": "Mensagens processadas com sucesso",
            "processed_messages": len(processed_data.get("messages", [])),
            "phone_number": processed_data.get("phone_number"),
            "workflow_result": result
        }
        
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/webhook/tela2/upload/csv")
async def upload_csv(
    phone_number: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload e processamento de arquivo CSV."""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser CSV")
        
        # Lê o conteúdo do arquivo
        content = await file.read()
        csv_data = content.decode('utf-8')
        
        # Processa o CSV
        messages = process_csv_content(csv_data)
        
        # Cria o payload processado
        processed_data = {
            "phone_number": phone_number,
            "messages": messages,
            "format_type": "csv"
        }
        
        # Executa o workflow
        result = await execute_message_workflow(processed_data)
        
        return {
            "status": "success",
            "message": "CSV processado com sucesso",
            "processed_messages": len(messages),
            "phone_number": phone_number,
            "workflow_result": result
        }
        
    except Exception as e:
        logger.error(f"Erro no upload CSV: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/webhook/tela2/upload/xlsx")
async def upload_xlsx(
    phone_number: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload e processamento de arquivo XLSX."""
    try:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Arquivo deve ser XLSX ou XLS")
        
        # Lê o conteúdo do arquivo
        content = await file.read()
        
        # Processa o XLSX
        messages = process_xlsx_content(content)
        
        # Cria o payload processado
        processed_data = {
            "phone_number": phone_number,
            "messages": messages,
            "format_type": "xlsx"
        }
        
        # Executa o workflow
        result = await execute_message_workflow(processed_data)
        
        return {
            "status": "success",
            "message": "XLSX processado com sucesso",
            "processed_messages": len(messages),
            "phone_number": phone_number,
            "workflow_result": result
        }
        
    except Exception as e:
        logger.error(f"Erro no upload XLSX: {e}")
        raise HTTPException(status_code=400, detail=str(e))

async def process_webhook_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processa diferentes tipos de payload do webhook.
    """
    phone_number = payload.get("phone_number") or payload.get("chatbotPhone")
    
    if not phone_number:
        raise ValueError("Número de telefone é obrigatório")
    
    # Detecta o tipo de dados
    if "messages" in payload and isinstance(payload["messages"], list):
        # Formato JSON estruturado
        messages = []
        for msg in payload["messages"]:
            if isinstance(msg, str):
                messages.append({"text": msg, "delay": 2})
            elif isinstance(msg, dict):
                messages.append({
                    "text": msg.get("text", ""),
                    "delay": msg.get("delay", 2)
                })
        
        return {
            "phone_number": phone_number,
            "messages": messages,
            "format_type": "json"
        }
    
    elif "text_list" in payload:
        # Texto colado (uma mensagem por linha)
        text_content = payload["text_list"]
        messages = process_text_content(text_content)
        
        return {
            "phone_number": phone_number,
            "messages": messages,
            "format_type": "paste"
        }
    
    elif "csv_content" in payload:
        # Conteúdo CSV inline
        csv_content = payload["csv_content"]
        messages = process_csv_content(csv_content)
        
        return {
            "phone_number": phone_number,
            "messages": messages,
            "format_type": "csv"
        }
    
    elif "testCases" in payload.get("body", {}):
        # Formato legado do N8N
        test_cases = payload["body"]["testCases"]
        messages = []
        for case in test_cases:
            messages.append({"text": case, "delay": 2})
        
        return {
            "phone_number": phone_number,
            "messages": messages,
            "format_type": "legacy"
        }
    
    else:
        raise ValueError("Formato de payload não reconhecido")


def process_text_content(text_content: str) -> List[Dict[str, Any]]:
    """Processa texto colado (uma mensagem por linha)."""
    lines = text_content.strip().split('\n')
    messages = []
    
    for line in lines:
        line = line.strip()
        if line:  # Ignora linhas vazias
            messages.append({"text": line, "delay": 2})
    
    return messages


def process_csv_content(csv_content: str) -> List[Dict[str, Any]]:
    """Processa conteúdo CSV."""
    messages = []
    
    # Tenta diferentes delimitadores
    for delimiter in [',', ';', '\t']:
        try:
            csv_reader = csv.DictReader(io.StringIO(csv_content), delimiter=delimiter)
            rows = list(csv_reader)
            
            if rows and len(rows) > 0:
                # Encontra a coluna com texto das mensagens
                text_column = None
                delay_column = None
                
                for col in rows[0].keys():
                    col_lower = col.lower()
                    if any(keyword in col_lower for keyword in ['text', 'message', 'mensagem', 'msg']):
                        text_column = col
                    elif any(keyword in col_lower for keyword in ['delay', 'intervalo', 'tempo']):
                        delay_column = col
                
                # Se não encontrou coluna específica, usa a primeira
                if not text_column:
                    text_column = list(rows[0].keys())[0]
                
                for row in rows:
                    text = row.get(text_column, "").strip()
                    if text:
                        delay = 2
                        if delay_column and row.get(delay_column):
                            try:
                                delay = int(row[delay_column])
                            except:
                                delay = 2
                        
                        messages.append({"text": text, "delay": delay})
                
                break  # Se processou com sucesso, para de tentar outros delimitadores
                
        except Exception as e:
            continue  # Tenta próximo delimitador
    
    if not messages:
        # Fallback: trata como texto simples
        lines = csv_content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line:
                messages.append({"text": line, "delay": 2})
    
    return messages


def process_xlsx_content(xlsx_content: bytes) -> List[Dict[str, Any]]:
    """Processa conteúdo XLSX."""
    messages = []
    
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(io.BytesIO(xlsx_content))
        
        # Encontra a coluna com texto das mensagens
        text_column = None
        delay_column = None
        
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['text', 'message', 'mensagem', 'msg']):
                text_column = col
            elif any(keyword in col_lower for keyword in ['delay', 'intervalo', 'tempo']):
                delay_column = col
        
        # Se não encontrou coluna específica, usa a primeira
        if text_column is None:
            text_column = df.columns[0]
        
        for _, row in df.iterrows():
            text = str(row[text_column]).strip()
            if text and text != 'nan':
                delay = 2
                if delay_column is not None and pd.notna(row[delay_column]):
                    try:
                        delay = int(row[delay_column])
                    except:
                        delay = 2
                
                messages.append({"text": text, "delay": delay})
    
    except Exception as e:
        logger.error(f"Erro ao processar XLSX: {e}")
        raise ValueError(f"Erro ao processar arquivo XLSX: {e}")
    
    return messages


async def execute_message_workflow(processed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executa o workflow de envio de mensagens.
    """
    try:
        # Cria o executor do workflow
        executor = WorkflowExecutor(settings)
        
        # Converte para o formato esperado pelo workflow
        webhook_data = {
            "body": {
                "method": "webhook",
                "testCases": [msg["text"] for msg in processed_data["messages"]],
                "chatbotPhone": processed_data["phone_number"],
                "messageDelays": [msg["delay"] for msg in processed_data["messages"]]
            }
        }
        
        logger.info(f"Executando workflow com {len(processed_data['messages'])} mensagens")
        
        # Executa o workflow
        result = await executor.execute(webhook_data)
        
        return {
            "status": "completed",
            "messages_sent": len(processed_data["messages"]),
            "phone_number": processed_data["phone_number"],
            "execution_details": result
        }
        
    except Exception as e:
        logger.error(f"Erro na execução do workflow: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


if __name__ == "__main__":
    # Configuração do servidor
    host = settings.WEBHOOK_HOST
    port = settings.WEBHOOK_PORT
    
    logger.info(f"Iniciando servidor webhook em {host}:{port}")
    logger.info(f"Webhook URL: http://{host}:{port}/webhook/tela2")
    
    uvicorn.run(
        "app.webhook_server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )