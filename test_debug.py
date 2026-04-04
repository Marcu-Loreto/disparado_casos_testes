#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from app.utils.expressions import ExpressionParser

def test_node_field():
    print("Testing node field expression...")
    parser = ExpressionParser()
    data = {
        "Node1": {"json": {"value": "test1"}},
        "Node2": {"json": {"value": "test2"}},
    }
    
    # Test the exact string from the test
    test_expr = '{{$node["Node1"].json.value}}'
    print(f"Test expression: {repr(test_expr)}")
    
    # Check if it matches our pattern
    match = parser.exact_node_pattern.match(test_expr.strip())
    print(f"Pattern match: {match}")
    if match:
        print(f"Groups: {match.groups()}")
    
    # Test evaluation
    result = parser.evaluate(test_expr, data)
    print(f"Evaluation result: {repr(result)}")
    print(f"Expected: 'test1'")
    print(f"Match: {result == 'test1'}")

if __name__ == "__main__":
    test_node_field()
