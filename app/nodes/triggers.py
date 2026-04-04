"""
Trigger node implementations for the Disparado_Casos_testes workflow.
"""

import json
import logging
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException
import uvicorn
import asyncio
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseTrigger(ABC):
    """Base class for all trigger nodes."""

    @abstractmethod
    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the trigger and return initial data."""
        pass


class WebhookTrigger(BaseTrigger):
    """Webhook trigger node implementation."""

    def __init__(self):
        self.app = FastAPI(title="Disparado_Casos_testes Webhook")
        self._setup_routes()
        self.received_data = None
        self._event = asyncio.Event()

    def _setup_routes(self):
        """Setup FastAPI routes for the webhook."""

        @self.app.post("/webhook/:test_cases_auto")
        async def webhook_endpoint(request: Request):
            try:
                body = await request.json()
                self.received_data = body
                self._event.set()
                logger.info("Webhook received data")
                return {"status": "success"}
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON")
            except Exception as e:
                logger.error(f"Webhook error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the webhook trigger.

        In a real implementation, this would start the webhook server and wait for data.
        For simplicity in this conversion, we'll simulate receiving data.
        """
        # For standalone execution, we'll use provided data or simulate
        if data:
            self.received_data = data
            self._event.set()

        # Wait for data (with timeout for demo purposes)
        try:
            await asyncio.wait_for(self._event.wait(), timeout=30.0)
        except asyncio.TimeoutError:
            logger.warning("Webhook timeout - using sample data")
            # Provide sample data for demonstration
            self.received_data = {
                "body": {
                    "method": "file",
                    "testCases": ["Sample test case 1", "Sample test case 2"],
                    "chatbotPhone": "+556199999999",
                }
            }

        return self.received_data or {}
