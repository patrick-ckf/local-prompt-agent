# -*- coding: utf-8 -*-
"""
Calculator tool for mathematical operations.

Simple, safe calculator using Python's eval with restrictions.
"""

import ast
import operator
from typing import Any, Dict

from local_prompt_agent.tools.base import Tool


class CalculatorTool(Tool):
    """
    Calculator tool for mathematical operations.

    Safe evaluation of math expressions.
    """

    # Safe operators
    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def __init__(self):
        """Initialize calculator tool."""
        super().__init__(
            name="calculator",
            description="Calculate mathematical expressions. "
            "Supports +, -, *, /, ** (power). Example: 25 * 4 + 10",
        )

    def get_parameters(self) -> Dict[str, Any]:
        """Get parameter schema."""
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate",
                }
            },
            "required": ["expression"],
        }

    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute calculation.

        Args:
            expression: Math expression string

        Returns:
            Result dictionary
        """
        expression = kwargs.get("expression", "")

        if not expression:
            return {"success": False, "error": "Expression is required"}

        try:
            # Parse expression
            tree = ast.parse(expression, mode="eval")

            # Evaluate safely
            result = self._eval_node(tree.body)

            return {
                "success": True,
                "expression": expression,
                "result": result,
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Calculation error: {str(e)}",
            }

    def _eval_node(self, node):
        """Safely evaluate AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = self.SAFE_OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = self.SAFE_OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(operand)
        else:
            raise ValueError(f"Unsupported expression: {type(node).__name__}")
