#!/usr/bin/env python3
"""
Main entry point for the Disparado_Casos_testes workflow.
"""

import asyncio
import logging
import sys
from typing import Dict, Any

from app.workflow import WorkflowExecutor
from config.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main application entry point."""
    try:
        # Load settings
        settings = Settings()
        logger.info("Starting Disparado_Casos_testes workflow")

        # Initialize workflow executor
        executor = WorkflowExecutor(settings)

        # Execute workflow (waiting for webhook trigger)
        # In a real application, this would be triggered by an HTTP request
        # For now, we'll demonstrate with sample data
        sample_data = {
            "body": {
                "method": "file",
                "testCases": ["Test case 1", "Test case 2", "Test case 3"],
                "chatbotPhone": "+556199999999",
            }
        }

        result = await executor.execute(sample_data)
        logger.info(f"Workflow completed successfully: {result}")

    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
