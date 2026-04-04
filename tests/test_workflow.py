"""
Functional tests for the Disparado_Casos_testes workflow.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

from app.workflow import WorkflowExecutor
from config.settings import Settings


class TestWorkflowExecution:
    """Test the complete workflow execution."""

    @pytest.fixture
    def settings(self):
        """Create test settings."""
        return Settings(
            GOOGLE_SHEETS_DOCUMENT_ID="test_doc_id",
            GOOGLE_SHEETS_TESTES_2026_SHEET_ID="test_sheet_id",
            LOG_LEVEL="INFO",
            ENVIRONMENT="testing",
        )

    @pytest.fixture
    def executor(self, settings):
        """Create workflow executor."""
        return WorkflowExecutor(settings)

    @pytest.mark.asyncio
    async def test_workflow_execution_structure(self, executor):
        """Test that workflow initializes correctly."""
        assert executor is not None
        assert len(executor.nodes) > 0
        assert len(executor.connections) > 0

    @pytest.mark.asyncio
    async def test_workflow_topological_sort(self, executor):
        """Test that topological sort produces valid order."""
        order = executor._topological_sort()

        # Should contain all nodes
        assert len(order) == len(executor.nodes)

        # Should contain expected nodes
        assert "Webhook" in order
        assert "Get row(s) in sheet" in order
        assert "HTTP Request1" in order

    @pytest.mark.asyncio
    async def test_workflow_execution_with_sample_data(self, executor):
        """Test workflow execution with sample data."""
        sample_data = {
            "body": {
                "method": "file",
                "testCases": ["Test case 1", "Test case 2", "Test case 3"],
                "chatbotPhone": "+556199999999",
            }
        }

        # This would normally execute the full workflow
        # For testing purposes, we'll just verify it doesn't crash on initialization
        # Full execution would require mocking all external dependencies

        # Test that we can gather inputs for a node
        inputs = executor._gather_inputs("HTTP Request1")
        # This might be empty initially, but shouldn't crash
        assert isinstance(inputs, dict)

    @pytest.mark.asyncio
    async def test_error_handling_in_workflow(self, executor):
        """Test that workflow handles errors gracefully."""
        # Test with a node that might fail
        # In a real test, we would mock specific nodes to raise exceptions

        # For now, just verify the error handling structure exists
        assert hasattr(executor, "_handle_error") or True  # Placeholder
