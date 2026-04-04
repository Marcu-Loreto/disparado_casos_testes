"""
Unit tests for workflow nodes.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

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
from app.utils.expressions import ExpressionParser


class TestSetNode:
    """Test SetNode functionality."""

    @pytest.mark.asyncio
    async def test_set_node_basic_assignment(self):
        """Test basic field assignment."""
        node = SetNode(assignments=[{"name": "new_field", "value": "static_value"}])

        result = await node.execute({"existing": "value"})

        assert result["existing"] == "value"
        assert result["new_field"] == "static_value"

    @pytest.mark.asyncio
    async def test_set_node_expression_resolution(self):
        """Test expression resolution in SetNode."""
        node = SetNode(
            assignments=[
                {"name": "copied_field", "value": "{{ $json.existing_field }}"}
            ]
        )

        input_data = {"existing_field": "test_value"}
        result = await node.execute(input_data)

        assert result["copied_field"] == "test_value"

    @pytest.mark.asyncio
    async def test_set_node_multiple_assignments(self):
        """Test multiple field assignments."""
        node = SetNode(
            assignments=[
                {"name": "field1", "value": "value1"},
                {"name": "field2", "value": "value2"},
            ]
        )

        result = await node.execute({})

        assert result["field1"] == "value1"
        assert result["field2"] == "value2"


class TestIfNode:
    """Test IfNode functionality."""

    @pytest.mark.asyncio
    async def test_if_node_true_condition(self):
        """Test IF node with true condition."""
        node = IfNode(
            conditions=[
                {
                    "leftValue": "{{ $json.status }}",
                    "rightValue": "active",
                    "operator": {"type": "string", "operation": "equals"},
                }
            ]
        )

        result = await node.execute({"status": "active"})

        assert result["if_result"] is True
        assert result["output_index"] == 0

    @pytest.mark.asyncio
    async def test_if_node_false_condition(self):
        """Test IF node with false condition."""
        node = IfNode(
            conditions=[
                {
                    "leftValue": "{{ $json.status }}",
                    "rightValue": "active",
                    "operator": {"type": "string", "operation": "equals"},
                }
            ]
        )

        result = await node.execute({"status": "inactive"})

        assert result["if_result"] is False
        assert result["output_index"] == 1

    @pytest.mark.asyncio
    async def test_if_node_multiple_conditions_and(self):
        """Test IF node with multiple AND conditions."""
        node = IfNode(
            conditions=[
                {
                    "leftValue": "{{ $json.status }}",
                    "rightValue": "active",
                    "operator": {"type": "string", "operation": "equals"},
                },
                {
                    "leftValue": "{{ $json.count }}",
                    "rightValue": "5",
                    "operator": {"type": "number", "operation": "greaterThan"},
                },
            ]
        )

        # Both conditions true
        result = await node.execute({"status": "active", "count": 10})
        assert result["if_result"] is True

        # First condition false
        result = await node.execute({"status": "inactive", "count": 10})
        assert result["if_result"] is False

        # Second condition false
        result = await node.execute({"status": "active", "count": 3})
        assert result["if_result"] is False


class TestCodeNode:
    """Test CodeNode functionality."""

    @pytest.mark.asyncio
    async def test_code_node_random_number(self):
        """Test CodeNode that generates random numbers."""
        node = CodeNode(
            js_code="""
const numero = Math.floor(Math.random() * 11) + 10;
return [{ json: { numero: numero } }];
"""
        )

        result = await node.execute({})

        assert len(result) == 1
        assert "numero" in result[0]["json"]
        numero = result[0]["json"]["numero"]
        assert 10 <= numero <= 20

    @pytest.mark.asyncio
    async def test_code_node_deduplication(self):
        """Test CodeNode that removes duplicates."""
        node = CodeNode(
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

        input_data = {
            "body": {"testCases": ["test1", "test2", "test1", "test3", "test2"]}
        }

        result = await node.execute(input_data)

        assert len(result) == 1
        test_cases = result[0]["json"]["body"]["testCases"]
        assert len(test_cases) == 3
        assert "test1" in test_cases
        assert "test2" in test_cases
        assert "test3" in test_cases
        # Check no duplicates
        assert len(test_cases) == len(set(test_cases))


class TestSplitInBatchesNode:
    """Test SplitInBatchesNode functionality."""

    @pytest.mark.asyncio
    async def test_split_in_batches_node(self):
        """Test SplitInBatches node."""
        node = SplitInBatchesNode(batch_size=1)

        result = await node.execute({"data": "test"})

        assert len(result) == 1
        assert result[0]["data"] == "test"


class TestSplitOutNode:
    """Test SplitOutNode functionality."""

    @pytest.mark.asyncio
    async def test_split_out_node(self):
        """Test SplitOut node."""
        node = SplitOutNode(field_to_split_out="body.testCases")

        input_data = {"body": {"testCases": ["case1", "case2", "case3"]}}

        result = await node.execute(input_data)

        assert len(result) == 3
        assert result[0]["body"]["testCases"] == "case1"
        assert result[0]["$itemIndex"] == 0
        assert result[1]["body"]["testCases"] == "case2"
        assert result[1]["$itemIndex"] == 1
        assert result[2]["body"]["testCases"] == "case3"
        assert result[2]["$itemIndex"] == 2


class TestMergeNode:
    """Test MergeNode functionality."""

    @pytest.mark.asyncio
    async def test_merge_node(self):
        """Test Merge node."""
        node = MergeNode(mode="append")

        result = await node.execute({"existing": "data"})

        assert result["existing"] == "data"


class TestWaitNode:
    """Test WaitNode functionality."""

    @pytest.mark.asyncio
    async def test_wait_node_short_delay(self):
        """Test Wait node with short delay."""
        node = WaitNode(amount=0.01)  # 10ms delay

        result = await node.execute({"test": "data"})

        assert result["test"] == "data"


class TestGoogleSheetsNode:
    """Test GoogleSheetsNode functionality."""

    @pytest.mark.asyncio
    async def test_google_sheets_get_operation(self):
        """Test Google Sheets get operation."""
        node = GoogleSheetsNode(
            operation="get", document_id="test_doc_id", sheet_name="test_sheet"
        )

        result = await node.execute({})

        assert "json" in result
        assert isinstance(result["json"], list)
        assert len(result["json"]) > 0
        assert "perguntas01" in result["json"][0]

    @pytest.mark.asyncio
    async def test_google_sheets_append_operation(self):
        """Test Google Sheets append operation."""
        node = GoogleSheetsNode(
            operation="append", document_id="test_doc_id", sheet_name="test_sheet"
        )

        result = await node.execute({})

        assert "json" in result
        assert result["json"]["success"] is True


class TestHTTPRequestNode:
    """Test HTTPRequestNode functionality."""

    @pytest.mark.asyncio
    async def test_http_request_node(self):
        """Test HTTP Request node."""
        node = HTTPRequestNode(
            method="POST",
            url="https://api.example.com/endpoint",
            headers={"Authorization": "Bearer {{$env.API_TOKEN}}"},
            json_body='{"message": "Hello {{$json.name}}"}',
        )

        # Mock environment variable
        with patch.dict("os.environ", {"API_TOKEN": "test_token"}):
            result = await node.execute({"name": "World"})

            assert "json" in result
            assert result["json"]["status"] == "sent"
            assert "message_id" in result["json"]


class TestDataTableNode:
    """Test DataTableNode functionality."""

    @pytest.mark.asyncio
    async def test_data_table_get_operation(self):
        """Test Data Table get operation."""
        node = DataTableNode(operation="get")

        result = await node.execute({})

        assert "json" in result
        assert isinstance(result["json"], list)
        assert len(result["json"]) > 0
        assert "perguntas01" in result["json"][0]

    @pytest.mark.asyncio
    async def test_data_table_create_operation(self):
        """Test Data Table create operation."""
        node = DataTableNode(
            resource="table",
            operation="create",
            table_name="test_table",
            columns=[{"name": "test_column"}],
        )

        result = await node.execute({})

        assert "json" in result
        assert result["json"]["success"] is True
        assert "tableId" in result["json"]


class TestExpressionParser:
    """Test ExpressionParser functionality."""

    def test_expression_parser_now(self):
        """Test {{$now}} expression."""
        parser = ExpressionParser()
        result = parser.evaluate("{{$now}}")

        # Should be a timestamp string
        assert isinstance(result, str)
        assert len(result) > 0

    def test_expression_parser_json_field(self):
        """Test {{$json.field}} expression."""
        parser = ExpressionParser()
        data = {"user": {"name": "John", "age": 30}}

        result = parser.evaluate("{{$json.user.name}}", data)
        assert result == "John"

        result = parser.evaluate("{{$json.user.age}}", data)
        assert result == 30

    def test_expression_parser_node_field(self):
        """Test {{$node[\"Name\"].json.field}} expression."""
        parser = ExpressionParser()
        data = {
            "Node1": {"json": {"value": "test1"}},
            "Node2": {"json": {"value": "test2"}},
        }

        result = parser.evaluate('{{$node["Node1"].json.value}}', data)
        assert result == "test1"

        result = parser.evaluate('{{$node["Node2"].json.value}}', data)
        assert result == "test2"

    def test_expression_parser_env_var(self):
        """Test {{$env.VAR}} expression."""
        parser = ExpressionParser()

        with patch.dict("os.environ", {"TEST_VAR": "test_value"}):
            result = parser.evaluate("{{$env.TEST_VAR}}")
            assert result == "test_value"

    def test_expression_parser_execution_id(self):
        """Test {{$execution.id}} expression."""
        parser = ExpressionParser()
        result = parser.evaluate("{{$execution.id}}")

        # Should be a UUID-like string
        assert isinstance(result, str)
        assert len(result) > 0
        # Basic UUID format check
        assert "-" in result
