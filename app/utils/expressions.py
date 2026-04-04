"""
Expression parser for N8N-style expressions in the Disparado_Casos_testes workflow.
"""

import re
import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class ExpressionParser:
    """Parses and evaluates N8N-style expressions."""

    def __init__(self):
        # Patterns for different expression types
        self.json_pattern = re.compile(r"\{\{\s*\$json\.([^}]+)\s*\}\}")
        self.node_pattern = re.compile(
            r'\{\{\s*\$node\["([^"]+)"\]\.json\.([^}]+)\s*\}\}'
        )
        self.env_pattern = re.compile(r"\{\{\s*\$env\.([^}]+)\s*\}\}")
        self.now_pattern = re.compile(r"\{\{\s*\$now\s*\}\}")
        self.execution_id_pattern = re.compile(r"\{\{\s*\$execution\.id\s*\}\}")

        # Patterns for exact match evaluation (used in evaluate method)
        self.exact_now_pattern = re.compile(r"^\{{\s*\$now\s*\}\}$")
        self.exact_execution_id_pattern = re.compile(r"^\{{\s*\$execution\.id\s*\}\}$")
        self.exact_env_pattern = re.compile(r"^\{{\s*\$env\.([^}]+)\s*\}\}$")
        self.exact_json_pattern = re.compile(r"^\{{\s*\$json\.([^}]+)\s*\}\}$")
        self.exact_node_pattern = re.compile(
            r'^\{{\s*\$node\["([^"]+)"\]\.json\.([^}]+)\s*\}\}$'
        )

    def evaluate(self, expression: str, data: Dict[str, Any] = None) -> Any:
        """
        Evaluate an N8N-style expression to get the raw value.
        Assumes the expression is a single expression (e.g., {{$json.field}}).

        Args:
            expression: Expression string (e.g., {{$json.field}})
            data: Data dictionary to evaluate against

        Returns:
            Evaluated value (raw type) or the original expression if not a single expression
        """
        if not expression or not isinstance(expression, str):
            return expression

        expression = expression.strip()

        # Handle {{$now}} - current timestamp
        match = self.exact_now_pattern.match(expression)
        if match:
            from datetime import datetime

            return datetime.now().isoformat()

        # Handle {{$execution.id}} - generate a pseudo execution ID
        match = self.exact_execution_id_pattern.match(expression)
        if match:
            import uuid

            return str(uuid.uuid4())

        # Handle {{$env.VAR}} - environment variables
        match = self.exact_env_pattern.match(expression)
        if match:
            var_name = match.group(1)
            import os

            return os.environ.get(var_name, "")

        # Handle {{$json.field}} - data from current item
        match = self.exact_json_pattern.match(expression)
        if match:
            field_path = match.group(1).strip()
            return self._get_nested_value(data, field_path)

        # Handle {{$node["Name"].json.field}} - data from specific node
        def replace_node_var(match):
            if not data:
                return match.group(0)  # Return original if no data

            node_name = match.group(1)
            field_path = match.group(2).strip()

            # Get data from the specified node
            node_data = data.get(node_name, {})
            if isinstance(node_data, list) and len(node_data) > 0:
                # If it's a list, take the first item (common in n8n)
                node_data = node_data[0]
            # Get the json part of the node data
            json_data = node_data.get("json", {})
            # Then get the field_path from the json_data
            return self._get_nested_value(json_data, field_path)

        # If not a single expression we recognize, return the original expression
        return expression

    def substitute(self, template: str, data: Dict[str, Any] = None) -> str:
        """
        Substitute all N8N-style expressions in a template string with their string values.

        Args:
            template: Template string containing expressions
            data: Data dictionary to substitute against

        Returns:
            Template string with expressions substituted
        """
        if not template or not isinstance(template, str):
            return template

        # Handle {{$now}} - current timestamp
        if self.now_pattern.search(template):
            from datetime import datetime

            now = datetime.now().isoformat()
            template = self.now_pattern.sub(now, template)

        # Handle {{$execution.id}} - generate a pseudo execution ID
        if self.execution_id_pattern.search(template):
            import uuid

            execution_id = str(uuid.uuid4())
            template = self.execution_id_pattern.sub(execution_id, template)

        # Handle {{$env.VAR}} - environment variables
        def replace_env_var(match):
            var_name = match.group(1)
            import os

            return os.environ.get(var_name, f"{{{{ $env.{var_name} }}}}")

        template = self.env_pattern.sub(replace_env_var, template)

        # Handle {{$json.field}} - data from current item
        def replace_json_var(match):
            if not data:
                return match.group(0)  # Return original if no data

            field_path = match.group(1).strip()
            value = self._get_nested_value(data, field_path)
            return str(value) if value is not None else match.group(0)

        template = self.json_pattern.sub(replace_json_var, template)

        # Handle {{$node["Name"].json.field}} - data from specific node
        def replace_node_var(match):
            if not data:
                return match.group(0)  # Return original if no data

            node_name = match.group(1)
            field_path = match.group(2).strip()

            # Get data from the specified node
            node_data = data.get(node_name, {})
            if isinstance(node_data, list) and len(node_data) > 0:
                # If it's a list, take the first item (common in n8n)
                node_data = node_data[0]

            value = self._get_nested_value(node_data, field_path)
            return str(value) if value is not None else match.group(0)

        template = self.node_pattern.sub(replace_node_var, template)

        return template

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """
        Get nested value from dictionary using dot notation.

        Args:
            data: Dictionary to search
            path: Dot-separated path (e.g., "user.profile.name")

        Returns:
            Value at path or None if not found
        """
        if not path or not data:
            return None

        keys = path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list):
                # Handle array indices
                if key.isdigit() and int(key) < len(current):
                    current = current[int(key)]
                else:
                    # Try to find first matching item if it's a list of objects
                    if isinstance(current[0], dict) and key in current[0]:
                        # Extract the key from all items
                        current = [item.get(key) for item in current if key in item]
                    else:
                        return None
            else:
                return None

        return current

        # Handle {{$now}} - current timestamp
        if self.now_pattern.search(expression):
            from datetime import datetime

            return datetime.now().isoformat()

        # Handle {{$execution.id}} - generate a pseudo execution ID
        if self.execution_id_pattern.search(expression):
            import uuid

            return str(uuid.uuid4())

        # Handle {{$env.VAR}} - environment variables
        def replace_env_var(match):
            var_name = match.group(1)
            import os

            return os.environ.get(var_name, f"{{{{ $env.{var_name} }}}}")

        expression = self.env_pattern.sub(replace_env_var, expression)

        # Handle {{$json.field}} - data from current item
        def replace_json_var(match):
            if not data:
                return match.group(0)  # Return original if no data

            field_path = match.group(1).strip()
            value = self._get_nested_value(data, field_path)
            return str(value) if value is not None else match.group(0)

        expression = self.json_pattern.sub(replace_json_var, expression)

        # Handle {{$node["Name"].json.field}} - data from specific node
        def replace_node_var(match):
            if not data:
                return match.group(0)  # Return original if no data

            node_name = match.group(1)
            field_path = match.group(2).strip()

            # Get data from the specified node
            node_data = data.get(node_name, {})
            if isinstance(node_data, list) and len(node_data) > 0:
                # If it's a list, take the first item (common in n8n)
                node_data = node_data[0]

            # Get the json property from the node data
            json_data = node_data.get("json", {})
            return self._get_nested_value(json_data, field_path)

        expression = self.node_pattern.sub(replace_node_var, expression)

        return expression

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """
        Get nested value from dictionary using dot notation.

        Args:
            data: Dictionary to search
            path: Dot-separated path (e.g., "user.profile.name")

        Returns:
            Value at path or None if not found
        """
        if not path or not data:
            return None

        keys = path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list):
                # Handle array indices
                if key.isdigit() and int(key) < len(current):
                    current = current[int(key)]
                else:
                    # Try to find first matching item if it's a list of objects
                    if isinstance(current[0], dict) and key in current[0]:
                        # Extract the key from all items
                        current = [item.get(key) for item in current if key in item]
                    else:
                        return None
            else:
                return None

        return current


# Global parser instance
expression_parser = ExpressionParser()


def evaluate_expression(expression: str, data: Dict[str, Any] = None) -> Any:
    """
    Convenience function to evaluate an expression.

    Args:
        expression: Expression string
        data: Data dictionary

    Returns:
        Evaluated value
    """
    return expression_parser.evaluate(expression, data)
