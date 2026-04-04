"""
Processor node implementations for the Disparado_Casos_testes workflow.
"""

import logging
import random
import copy
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError, validator
import bleach

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """Base class for all workflow nodes."""

    @abstractmethod
    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the node and return results."""
        pass


class SetNode(BaseNode):
    """Set node implementation (equivalent to n8n's Set node)."""

    def __init__(self, assignments: List[Dict[str, Any]] = None):
        self.assignments = assignments or []

    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Set fields based on assignments."""
        result = data.copy() if data else {}

        for assignment in self.assignments:
            name = assignment.get("name")
            value_template = assignment.get("value")
            value_type = assignment.get("type", "string")

            if name and value_template:
                try:
                    # In a real implementation, we would parse the expression
                    # For now, we'll do simple variable substitution
                    value = self._resolve_expression(value_template, result)
                    result[name] = value
                except Exception as e:
                    logger.warning(f"Failed to set field {name}: {e}")

        return result

    def _resolve_expression(self, expression: str, data: Dict[str, Any]) -> Any:
        """Resolve N8N-style expressions like {{$json.field}} or {{$node[\"Name\"].json.field}}."""
        # Use the global expression parser for consistency
        from app.utils.expressions import expression_parser

        return expression_parser.evaluate(expression, data)

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get nested value from dictionary using dot notation."""
        if not path:
            return data

        keys = path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif (
                isinstance(current, list) and key.isdigit() and int(key) < len(current)
            ):
                current = current[int(key)]
            else:
                return None

        return current


class IfNode(BaseNode):
    """IF node implementation (equivalent to n8n's IF node)."""

    def __init__(self, conditions: List[Dict[str, Any]] = None):
        self.conditions = conditions or []

    def _resolve_expression(self, expression: str, data: Dict[str, Any]) -> Any:
        """Resolve N8N-style expressions like {{$json.field}} or {{$node[\"Name\"].json.field}}."""
        # Use the global expression parser for consistency
        from app.utils.expressions import expression_parser

        return expression_parser.evaluate(expression, data)

    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Evaluate conditions and return appropriate output."""
        result = data.copy() if data else {}

        # Evaluate all conditions
        condition_results = []
        for condition in self.conditions:
            try:
                left_value = self._resolve_expression(
                    condition.get("leftValue", ""), result
                )
                right_value = self._resolve_expression(
                    condition.get("rightValue", ""), result
                )

                operator_info = condition.get("operator", {})
                op_type = operator_info.get("type", "string")
                operation = operator_info.get("operation", "equals")

                # Evaluate based on operation
                condition_result = self._evaluate_condition(
                    left_value, right_value, op_type, operation
                )
                condition_results.append(condition_result)
            except Exception as e:
                logger.warning(f"Error evaluating condition: {e}")
                condition_results.append(False)

        # Apply combinator (AND/OR)
        if self.conditions:
            combinator = self.conditions[0].get("combinator", "and").lower()
            if combinator == "or":
                final_result = any(condition_results)
            else:  # Default to AND
                final_result = all(condition_results)
        else:
            final_result = True

        # Add evaluation result to output
        result["if_result"] = final_result
        result["output_index"] = 0 if final_result else 1  # 0 for true, 1 for false

        return result

    def _evaluate_condition(
        self, left: Any, right: Any, op_type: str, operation: str
    ) -> bool:
        """Evaluate a single condition."""
        try:
            if op_type == "string":
                if operation == "equals":
                    return str(left) == str(right)
                elif operation == "notEqual":
                    return str(left) != str(right)
                elif operation == "contains":
                    return str(right) in str(left)
                elif operation == "notContains":
                    return str(right) not in str(left)
                elif operation == "startsWith":
                    return str(left).startswith(str(right))
                elif operation == "endsWith":
                    return str(left).endswith(str(right))
                elif operation == "empty":
                    return not str(left)
                elif operation == "notEmpty":
                    return bool(str(left))

            elif op_type == "number":
                left_num = float(left) if left is not None else 0
                right_num = float(right) if right is not None else 0

                if operation == "equals":
                    return left_num == right_num
                elif operation == "notEqual":
                    return left_num != right_num
                elif operation == "greaterThan":
                    return left_num > right_num
                elif operation == "greaterOrEqual":
                    return left_num >= right_num
                elif operation == "lessThan":
                    return left_num < right_num
                elif operation == "lessOrEqual":
                    return left_num <= right_num

            elif op_type == "date":
                # Simplified date comparison
                if operation == "equals":
                    return str(left) == str(right)
                elif operation == "notEqual":
                    return str(left) != str(right)
                elif operation == "greaterThan":
                    return str(left) > str(right)  # Simplified
                elif operation == "greaterOrEqual":
                    return str(left) >= str(right)  # Simplified
                elif operation == "lessThan":
                    return str(left) < str(right)  # Simplified
                elif operation == "lessOrEqual":
                    return str(left) <= str(right)  # Simplified

            return False
        except Exception as e:
            logger.warning(f"Error in condition evaluation: {e}")
            return False


class CodeNode(BaseNode):
    """Code node implementation (equivalent to n8n's Code node)."""

    def __init__(self, js_code: str = ""):
        self.js_code = js_code

    async def execute(self, data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute JavaScript code (conceptually - in Python we'd execute equivalent Python)."""
        # For security reasons, we don't actually execute arbitrary JS
        # Instead, we simulate the behavior of specific known code snippets

        result = data.copy() if data else {}

        # Handle specific known code patterns from the workflow
        if "Math.floor(Math.random() * 11) + 10" in self.js_code:
            # This is the random number generator from the workflow
            numero = random.randint(10, 20)
            result["numero"] = numero
            return [{"json": result}]

        elif "Remove duplicados do array" in self.js_code:
            # This is the deduplication code
            if "body" in result and "testCases" in result["body"]:
                test_cases = result["body"]["testCases"]
                if isinstance(test_cases, list):
                    # Remove duplicates while preserving order
                    seen = set()
                    unique = []
                    for item in test_cases:
                        if item not in seen:
                            seen.add(item)
                            unique.append(item)
                    result["body"]["testCases"] = unique
            return [{"json": result}]

        # For unknown code, return data unchanged (with warning)
        logger.warning(f"Unknown code pattern in CodeNode: {self.js_code[:50]}...")
        return [{"json": result}]


class SplitInBatchesNode(BaseNode):
    """SplitInBatches node implementation."""

    def __init__(self, batch_size: int = 1):
        self.batch_size = batch_size

    async def execute(self, data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Split data into batches."""
        if not data:
            return [{}]

        # For simplicity, we'll treat the input as a single item to be batched
        # In a real implementation, this would split arrays/lists
        return [data]


class SplitOutNode(BaseNode):
    """SplitOut node implementation."""

    def __init__(self, field_to_split_out: str = ""):
        self.field_to_split_out = field_to_split_out

    async def execute(self, data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Split a field into multiple items."""
        if not data or not self.field_to_split_out:
            return [data or {}]

        # Extract the field to split
        field_value = self._get_nested_value(data, self.field_to_split_out)

        if not isinstance(field_value, list):
            # If it's not a list, treat it as a single-item list
            field_value = [field_value]

        # Create one item per element in the list
        results = []
        for i, item in enumerate(field_value):
            item_data = copy.deepcopy(data)
            # Set the split field to the current item
            self._set_nested_value(item_data, self.field_to_split_out, item)
            # Add index information
            item_data["$itemIndex"] = i
            results.append(item_data)

        return results

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get nested value from dictionary using dot notation."""
        if not path:
            return data

        keys = path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif (
                isinstance(current, list) and key.isdigit() and int(key) < len(current)
            ):
                current = current[int(key)]
            else:
                return None

        return current

    def _set_nested_value(self, data: Dict[str, Any], path: str, value: Any) -> None:
        """Set nested value in dictionary using dot notation."""
        if not path:
            return

        keys = path.split(".")
        current = data

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value


class MergeNode(BaseNode):
    """Merge node implementation."""

    def __init__(self, mode: str = "append"):
        self.mode = mode

    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Merge data from multiple sources."""
        # In a real implementation, this would merge data from different branches
        # For now, we'll just return the data as-is
        return data or {}


class WaitNode(BaseNode):
    """Wait node implementation."""

    def __init__(self, amount: int = 1, unit: str = "seconds", webhook_id: str = None):
        self.amount = amount
        self.unit = unit
        self.webhook_id = webhook_id

    async def execute(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Wait for specified amount of time."""
        import asyncio

        # Convert to seconds
        delay_seconds = self.amount
        if self.unit == "minutes":
            delay_seconds *= 60
        elif self.unit == "hours":
            delay_seconds *= 3600

        # Actually wait
        await asyncio.sleep(delay_seconds)

        return data or {}
