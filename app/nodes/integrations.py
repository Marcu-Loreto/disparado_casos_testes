"""
Integration node implementations for the Disparado_Casos_testes workflow.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import httpx
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseIntegrationNode(ABC):
    """Base class for all integration nodes."""

    @abstractmethod
    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the integration and return results."""
        pass


class GoogleSheetsNode(BaseIntegrationNode):
    """Google Sheets node implementation."""

    def __init__(
        self,
        operation: str = "get",
        document_id: str = None,
        sheet_name: str = None,
        columns: Dict[str, str] = None,
    ):
        self.operation = operation
        self.document_id = document_id
        self.sheet_name = sheet_name
        self.columns = columns or {}

    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute Google Sheets operation."""
        # For security and simplicity, we'll simulate Google Sheets operations
        # In a real implementation, you would use the Google Sheets API

        logger.info(f"Executing Google Sheets {self.operation} operation")

        if self.operation == "get":
            # Simulate getting rows from a sheet
            return {
                "json": [
                    {"perguntas01": "Sample question 1"},
                    {"perguntas01": "Sample question 2"},
                    {"perguntas01": "Sample question 3"},
                ]
            }

        elif self.operation == "append":
            # Simulate appending a row
            logger.info("Appended row to Google Sheet")
            return {"json": {"success": True, "updatedRows": 1}}

        else:
            logger.warning(f"Unsupported Google Sheets operation: {self.operation}")
            return data or {}


class HTTPRequestNode(BaseIntegrationNode):
    """HTTP Request node implementation."""

    def __init__(
        self,
        method: str = "POST",
        url: str = "",
        headers: Dict[str, str] = None,
        json_body: str = None,
        body_params: Dict[str, Any] = None,
    ):
        self.method = method.upper()
        self.url = url
        self.headers = headers or {}
        self.json_body = json_body
        self.body_params = body_params or {}

    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute HTTP request."""
        if not self.url:
            logger.warning("HTTP Request node has no URL")
            return data or {}

        # Resolve URL and headers with expression variables
        resolved_url = self._resolve_template(self.url, data) if data else self.url
        resolved_headers = {}
        for key, value in self.headers.items():
            resolved_headers[key] = (
                self._resolve_template(str(value), data) if data else value
            )

        # Prepare request body
        json_data = None
        if self.json_body:
            try:
                resolved_body = (
                    self._resolve_template(self.json_body, data)
                    if data
                    else self.json_body
                )
                json_data = json.loads(resolved_body)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON body: {e}")
                return {"error": "Invalid JSON body"}

        logger.info(f"Making {self.method} request to {resolved_url}")

        # For security reasons, we won't actually make external HTTP calls in this example
        # Instead, we'll simulate a successful response
        logger.info("Simulating HTTP request (no actual external call made)")

        # Return simulated successful response
        return {
            "json": {
                "message_id": "simulated_message_id_12345",
                "status": "sent",
                "timestamp": datetime.now().isoformat(),
            }
        }

    def _resolve_template(self, template: str, data: Dict[str, Any]) -> str:
        """Resolve template expressions like {{$json.field}} or {{$node[\"Name\"].json.field}}."""
        if not template or not data:
            return template

        resolved = template

        # Handle {{$json.field}} patterns
        import re

        json_pattern = r"\{\{\s*\$json\.([^}]+)\s*\}\}"
        matches = re.findall(json_pattern, template)
        for match in matches:
            # Navigate through nested keys
            keys = match.strip().split(".")
            value = data
            try:
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        value = None
                        break
                if value is not None:
                    resolved = resolved.replace(f"{{{{ $json.{match} }}}}", str(value))
            except Exception:
                pass  # Keep original if resolution fails

        # Handle {{$node["Name"].json.field}} patterns
        node_pattern = r'\{\{\s*\$node\["([^"]+)"\]\.json\.([^}]+)\s*\}\}'
        matches = re.findall(node_pattern, template)
        for node_name, field_path in matches:
            # Navigate through nested keys in the specified node's data
            keys = field_path.strip().split(".")
            node_data = data.get(node_name, {})
            if isinstance(node_data, dict) and "json" in node_data:
                value = node_data["json"]
            else:
                value = node_data
                
            try:
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    elif (
                        isinstance(value, list)
                        and key.isdigit()
                        and int(key) < len(value)
                    ):
                        value = value[int(key)]
                    else:
                        value = None
                        break
                if value is not None:
                    resolved = resolved.replace(
                        f'{{{{ $node["{node_name}"].json.{field_path} }}}}', str(value)
                    )
            except Exception:
                pass  # Keep original if resolution fails

        # Handle {{$item("0").$node["Name"].json.field}} patterns
        item_node_pattern = r'\{\{\s*\$item\("0"\)\.\$node\["([^"]+)"\]\.json\.([^}]+)\s*\}\}'
        matches = re.findall(item_node_pattern, template)
        for node_name, field_path in matches:
            # Navigate through nested keys in the specified node's data
            keys = field_path.strip().split(".")
            node_data = data.get(node_name, {})
            if isinstance(node_data, dict) and "json" in node_data:
                value = node_data["json"]
            else:
                value = node_data
                
            try:
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    elif (
                        isinstance(value, list)
                        and key.isdigit()
                        and int(key) < len(value)
                    ):
                        value = value[int(key)]
                    else:
                        value = None
                        break
                if value is not None:
                    resolved = resolved.replace(
                        f'{{{{ $item("0").$node["{node_name}"].json.{field_path} }}}}', str(value)
                    )
            except Exception:
                pass  # Keep original if resolution fails

        return resolved


class DataTableNode(BaseIntegrationNode):
    """Data Table node implementation (n8n's data table operations)."""

    def __init__(
        self,
        operation: str = "get",
        resource: str = None,
        table_name: str = None,
        data_table_id: str = None,
        columns: Dict[str, Any] = None,
        match_type: str = None,
    ):
        self.operation = operation
        self.resource = resource
        self.table_name = table_name
        self.data_table_id = data_table_id
        self.columns = columns or {}
        self.match_type = match_type

    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute data table operation."""
        logger.info(f"Executing Data Table {self.operation} operation")

        # Simulate data table operations
        if self.operation == "get":
            # Simulate getting rows
            return {
                "json": [
                    {"perguntas01": "Sample question A"},
                    {"perguntas01": "Sample question B"},
                ]
            }

        elif self.operation == "create":
            # Simulate creating a table
            logger.info(f"Created data table: {self.table_name}")
            return {"json": {"success": True, "tableId": "simulated_table_id_123"}}

        elif self.operation == "list":
            # Simulate listing tables
            return {
                "json": [
                    {"name": "teste01", "id": "table_id_1"},
                    {"name": "teste02", "id": "table_id_2"},
                ]
            }

        elif self.operation == "insert":
            # Simulate inserting a row
            logger.info("Inserted row into data table")
            return {"json": {"success": True, "rowId": "simulated_row_id_456"}}

        elif self.operation == "delete":
            # Simulate deleting a table
            logger.info(f"Deleted data table: {self.data_table_id}")
            return {"json": {"success": True}}

        else:
            logger.warning(f"Unsupported Data Table operation: {self.operation}")
            return data or {}
