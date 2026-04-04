"""
Workflow execution engine for Disparado_Casos_testes.
Orchestrates the execution of nodes based on the N8N workflow definition.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque

from app.nodes.triggers import WebhookTrigger
from app.nodes.processors import (
    SetNode,
    IfNode,
    CodeNode,
    SplitInBatchesNode,
    SplitOutNode,
    MergeNode,
    WaitNode,
)
from app.nodes.integrations import GoogleSheetsNode, HTTPRequestNode, DataTableNode
from app.security.secrets import SecretManager
from app.utils.logger import get_logger
from app.utils.expressions import ExpressionParser

logger = get_logger(__name__)


class WorkflowExecutor:
    """Executes the Disparado_Casos_testes workflow."""

    def __init__(self, settings):
        self.settings = settings
        self.secret_manager = SecretManager()
        self.expression_parser = ExpressionParser()
        self.nodes = {}
        self.connections = {}
        self.results = {}
        self._initialize_nodes()
        self._initialize_connections()

    def _initialize_nodes(self):
        """Initialize all workflow nodes."""
        # Triggers
        self.nodes["Webhook"] = WebhookTrigger()

        # Processors
        self.nodes["Get row(s) in sheet"] = GoogleSheetsNode(
            operation="get",
            document_id=self.settings.GOOGLE_SHEETS_DOCUMENT_ID,
            sheet_name=self.settings.GOOGLE_SHEETS_TESTES_2026_SHEET_ID,
        )
        self.nodes["Loop Over Items"] = SplitInBatchesNode(batch_size=1)
        self.nodes["Replace Me"] = SetNode()  # Placeholder
        self.nodes["Edit Fields"] = SetNode(
            assignments=[
                {
                    "name": "perguntas",
                    "value": '{{ $item("0").$node["Loop Over Items"].json["perguntas01"] }}',
                }
            ]
        )
        self.nodes["Edit Fields1"] = SetNode(
            assignments=[
                {"name": "instancia", "value": self.settings.EVOLUTION_INSTANCE},
                {"name": "URL", "value": self.settings.EVOLUTION_API_URL},
                {"name": "API_KEY", "value": self.settings.EVOLUTION_API_KEY},
                {
                    "name": "Telefone_bot_+556132073332",
                    "value": '{{ $item("0").$node["Webhook"].json["body"]["chatbotPhone"] }}',
                },
            ]
        )
        self.nodes["Wait"] = WaitNode(amount=1)
        self.nodes["Code in JavaScript"] = CodeNode(
            js_code="""
const numero = Math.floor(Math.random() * 11) + 10;
return [{ json: { numero: numero } }];
"""
        )
        self.nodes["HTTP Request1"] = HTTPRequestNode(
            method="POST",
            url='{{ $item("0").$node["Edit Fields1"].json["URL"] }}/message/sendText/{{ $item("0").$node["Edit Fields1"].json["instancia"] }}',
            headers={
                "apikey": '{{ $item("0").$node["Edit Fields1"].json["API_KEY"] }}',
                "Content-Type": "application/json"
            },
            json_body='{"number": "{{ $item("0").$node["Edit Fields1"].json["Telefone_bot_+556132073332"] }}", "text": "{{ $item("0").$node["Edit Fields"].json["perguntas"] }}"}',
        )
        self.nodes["Edit Fields2"] = SetNode(
            assignments=[
                {
                    "name": "body.testCases",
                    "value": '{{ $item("0").$node["Webhook"].json["body"]["testCases"] }}',
                }
            ]
        )
        self.nodes["Extract from File"] = DataTableNode(operation="xlsx")
        self.nodes["Append row in sheet"] = GoogleSheetsNode(
            operation="append",
            document_id=self.settings.GOOGLE_SHEETS_DOCUMENT_ID,
            sheet_name=self.settings.GOOGLE_SHEETS_TESTES_2026_SHEET_ID,
        )
        self.nodes["Loop Over Items1"] = SplitInBatchesNode(batch_size=1)
        self.nodes["Split Out"] = SplitOutNode(field_to_split_out="body.testCases")
        self.nodes["Wait1"] = WaitNode(amount=4)
        self.nodes["If"] = IfNode(
            conditions=[
                {
                    "leftValue": "{{ $json.body.method }}",
                    "rightValue": "file",
                    "operator": {"type": "string", "operation": "contains"},
                }
            ]
        )
        self.nodes["Append row in sheet1"] = GoogleSheetsNode(
            operation="append",
            document_id=self.settings.GOOGLE_SHEETS_DOCUMENT_ID,
            sheet_name=self.settings.GOOGLE_SHEETS_TESTES_2026_SHEET_ID,
        )
        self.nodes["Loop Over Items2"] = SplitInBatchesNode(batch_size=1)
        self.nodes["Wait2"] = WaitNode(amount=2)
        self.nodes["Wait3"] = WaitNode(
            amount=1, webhook_id="e9a41b72-57dc-45ad-8ea8-9f4983c7fe84"
        )
        self.nodes["Get row(s)"] = DataTableNode(
            operation="get", match_type="allConditions"
        )
        self.nodes["Insert row"] = DataTableNode(operation="insert")
        self.nodes["Insert row1"] = DataTableNode(operation="insert")
        self.nodes["If1"] = IfNode(
            conditions=[
                {
                    "leftValue": '{{ $item("10").$node["Get row(s)"].json["perguntas"] }} {{ $item("0").$node["Get row(s)"].json["perguntas"] }}',
                    "rightValue": "",
                    "operator": {"type": "string", "operation": "equals"},
                }
            ]
        )
        self.nodes["Create a data table"] = DataTableNode(
            resource="table",
            operation="create",
            table_name="teste01",
            columns=[{"name": "perguntas01"}],
        )
        self.nodes["Delete a data table"] = DataTableNode(
            resource="table",
            operation="delete",
            data_table_id='{{ $item("0").$node["List data tables"].json["name"] }}',
        )
        self.nodes["List data tables"] = DataTableNode(
            resource="table", operation="list"
        )
        self.nodes["Edit Fields3"] = SetNode(
            assignments=[
                {
                    "name": "table",
                    "value": '{{ $item("0").$node["List data tables"].json["name"] }}',
                }
            ]
        )
        self.nodes["Delete a data table1"] = DataTableNode(
            resource="table", operation="delete", data_table_id="V9LM1PM9BQFYmOTn"
        )
        self.nodes["Merge"] = MergeNode(mode="append")
        self.nodes["Code in JavaScript1"] = CodeNode(
            js_code="""
// Acessa o primeiro item recebido
const data = items[0].json;
// Remove duplicados do array
const unique = [...new Set(data.body.testCases)];
// Atualiza o payload
data.body.testCases = unique;
// Retorna o item corrigido
return [{ json: data }];
"""
        )
        self.nodes["If2"] = IfNode(
            conditions=[
                {
                    "leftValue": '{{ $item("0").$node["List data tables"].json["name"] }}',
                    "rightValue": "teste01",
                    "operator": {"type": "string", "operation": "contains"},
                }
            ]
        )
        self.nodes["Delete a data table2"] = DataTableNode(
            resource="table",
            operation="delete",
            data_table_id='{{ $item("0").$node["List data tables"].json["name"] }}',
        )

    def _initialize_connections(self):
        """Initialize node connections based on the workflow definition."""
        self.connections = {
            "Get row(s) in sheet": {"main": [[]]},
            "Loop Over Items": {
                "main": [
                    [{"node": "Replace Me", "type": "main", "index": 0}],
                    [{"node": "Edit Fields", "type": "main", "index": 0}],
                ]
            },
            "Replace Me": {"main": [[{"node": "If2", "type": "main", "index": 0}]]},
            "Edit Fields": {
                "main": [[{"node": "Edit Fields1", "type": "main", "index": 0}]]
            },
            "Wait": {
                "main": [[{"node": "Loop Over Items", "type": "main", "index": 0}]]
            },
            "Edit Fields1": {
                "main": [[{"node": "HTTP Request1", "type": "main", "index": 0}]]
            },
            "HTTP Request1": {
                "main": [[{"node": "Code in JavaScript", "type": "main", "index": 0}]]
            },
            "Code in JavaScript": {
                "main": [[{"node": "Wait", "type": "main", "index": 0}]]
            },
            "Webhook": {
                "main": [
                    [
                        {"node": "Merge", "type": "main", "index": 1},
                        {"node": "Create a data table", "type": "main", "index": 0},
                    ]
                ]
            },
            "Edit Fields2": {
                "main": [[{"node": "Code in JavaScript1", "type": "main", "index": 0}]]
            },
            "Extract from File": {
                "main": [[{"node": "Loop Over Items2", "type": "main", "index": 0}]]
            },
            "Append row in sheet": {"main": [[]]},
            "Loop Over Items1": {
                "main": [
                    [{"node": "Wait4", "type": "main", "index": 0}],
                    [{"node": "Insert row", "type": "main", "index": 0}],
                ]
            },
            "Split Out": {
                "main": [[{"node": "Loop Over Items1", "type": "main", "index": 0}]]
            },
            "Wait1": {
                "main": [[{"node": "Loop Over Items1", "type": "main", "index": 0}]]
            },
            "If": {
                "main": [
                    [{"node": "Extract from File", "type": "main", "index": 0}],
                    [{"node": "Edit Fields2", "type": "main", "index": 0}],
                ]
            },
            "Append row in sheet1": {"main": [[]]},
            "Loop Over Items2": {
                "main": [
                    [{"node": "Wait3", "type": "main", "index": 0}],
                    [{"node": "Insert row1", "type": "main", "index": 0}],
                ]
            },
            "Wait2": {
                "main": [[{"node": "Loop Over Items2", "type": "main", "index": 0}]]
            },
            "Wait3": {"main": [[{"node": "Get row(s)", "type": "main", "index": 0}]]},
            "Wait4": {"main": [[{"node": "Get row(s)", "type": "main", "index": 0}]]},
            "Insert row": {"main": [[{"node": "Wait1", "type": "main", "index": 0}]]},
            "Get row(s)": {
                "main": [[{"node": "Loop Over Items", "type": "main", "index": 0}]]
            },
            "Insert row1": {"main": [[{"node": "Wait2", "type": "main", "index": 0}]]},
            "If1": {"main": [[]]},
            "Create a data table": {
                "main": [[{"node": "List data tables", "type": "main", "index": 0}]]
            },
            "List data tables": {
                "main": [[{"node": "Edit Fields3", "type": "main", "index": 0}]]
            },
            "Edit Fields3": {"main": [[{"node": "Merge", "type": "main", "index": 0}]]},
            "Merge": {"main": [[{"node": "If", "type": "main", "index": 0}]]},
            "Code in JavaScript1": {
                "main": [[{"node": "Split Out", "type": "main", "index": 0}]]
            },
            "If2": {
                "main": [
                    [
                        {"node": "Delete a data table", "type": "main", "index": 0},
                        {"node": "Delete a data table2", "type": "main", "index": 0},
                    ]
                ]
            },
        }

    async def execute(self, trigger_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the workflow following the topological order.

        Args:
            trigger_data: Initial data from the trigger (webhook, schedule, etc.)

        Returns:
            Dictionary containing results from all executed nodes
        """
        logger.info("Starting workflow execution")

        # Execute trigger nodes first
        if "Webhook" in self.nodes:
            webhook_data = await self.nodes["Webhook"].execute(trigger_data or {})
            self.results["Webhook"] = webhook_data

        # Execute workflow in topological order
        execution_order = self._topological_sort()
        logger.info(f"Execution order: {execution_order}")

        for node_name in execution_order:
            if node_name in self.results:  # Skip already executed nodes (triggers)
                continue

            node = self.nodes[node_name]
            input_data = self._gather_inputs(node_name)

            try:
                logger.info(f"Executing node: {node_name}")
                result = await node.execute(input_data)
                self.results[node_name] = result
                logger.info(f"Node {node_name} executed successfully")
            except Exception as e:
                logger.error(f"Error executing node {node_name}: {e}")
                # Depending on error handling strategy, we might continue or break
                raise

        logger.info("Workflow execution completed")
        return self.results

    def _topological_sort(self) -> List[str]:
        """
        Perform topological sort on the workflow graph to determine execution order.

        Returns:
            List of node names in execution order
        """
        # Build adjacency list and in-degree count
        adj_list = defaultdict(list)
        in_degree = defaultdict(int)

        # Initialize in-degree for all nodes
        for node_name in self.nodes:
            in_degree[node_name] = 0

        # Build graph from connections
        for node_name, connections in self.connections.items():
            for connection_type in ["main"]:  # We mainly care about main connections
                if connection_type in connections:
                    for connection_group in connections[connection_type]:
                        for connection in connection_group:
                            target_node = connection["node"]
                            adj_list[node_name].append(target_node)
                            in_degree[target_node] += 1

        # Kahn's algorithm for topological sort
        queue = deque([node for node in self.nodes if in_degree[node] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in adj_list[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check for cycles
        if len(result) != len(self.nodes):
            logger.warning("Workflow contains cycles, execution order may be incorrect")

        return result

    def _gather_inputs(self, node_name: str) -> Dict[str, Any]:
        """
        Gather input data for a node from its predecessor nodes.

        Args:
            node_name: Name of the node to gather inputs for

        Returns:
            Dictionary containing input data
        """
        inputs = {}

        # Find all nodes that connect to this node
        for source_node, connections in self.connections.items():
            for connection_type in ["main"]:
                if connection_type in connections:
                    for connection_group in connections[connection_type]:
                        for connection in connection_group:
                            if connection["node"] == node_name:
                                # Add data from source node to inputs
                                if source_node in self.results:
                                    inputs[source_node] = self.results[source_node]

        return inputs
