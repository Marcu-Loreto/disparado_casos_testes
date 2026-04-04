import re

# Test the exact string from the file
test_string = '{{$node["Node1"].json.value}}'
print('Test string:', repr(test_string))

# Our pattern
pattern_str = r'^\{\{\s*\$node\["([^"]+)"\]\.json\.([^}]+)\s*\}\}$'
print('Pattern string:', repr(pattern_str))

pattern = re.compile(pattern_str)
match = pattern.match(test_string)
print('Match:', match)
if match:
    print('Groups:', match.groups())
else:
    print('No match')
    
# Let's debug step by step
print('\\nDebugging:')
print('Starts with {{:', test_string.startswith('{{'))
if test_string.startswith('{{'):
    after_double_brace = test_string[2:]
    print('After {{:', repr(after_double_brace))
    print('Starts with $:', after_double_brace.startswith('$'))
    if after_double_brace.startswith('$'):
        after_dollar = after_double_brace[1:]
        print('After $:', repr(after_dollar))
        print('Starts with node:', after_dollar.startswith('node'))
        if after_dollar.startswith('node'):
            after_node = after_dollar[4:]
            print('After node:', repr(after_node))
            print('Starts with [: ', after_node.startswith('['))
            if after_node.startswith('['):
                after_open_bracket = after_node[1:]
                print('After [: ', repr(after_open_bracket))
                print('Starts with ": ', after_open_bracket.startswith('"'))
                if after_open_bracket.startswith('"'):
                    # Find the closing quote
                    quote_end = after_open_bracket.find('"', 1)
                    print('Quote end position:', quote_end)
                    if quote_end != -1:
                        node_name = after_open_bracket[1:quote_end]
                        print('Node name:', repr(node_name))
                        after_quote = after_open_bracket[quote_end+1:]
                        print('After quote:', repr(after_quote))
                        print('Starts with ]: ', after_quote.startswith(']'))
                        if after_quote.startswith(']'):
                            after_close_bracket = after_quote[1:]
                            print('After ]:', repr(after_close_bracket))
                            print('Starts with .json.: ', after_close_bracket.startswith('.json.'))
                            if after_close_bracket.startswith('.json.'):
                                after_dot_json = after_close_bracket[6:]
                                print('After .json.: ', repr(after_dot_json))
                                print('Starts with value: ', after_dot_json.startswith('value'))
                                if after_dot_json.startswith('value'):
                                    after_value = after_dot_json[5:]
                                    print('After value:', repr(after_value))
                                    print('Starts with }}: ', after_value.startswith('}}'))
                                    if after_value.startswith('}}'):
                                        after_double_brace2 = after_value[2:]
                                        print('After }}: ', repr(after_double_brace2))
                                        print('Is empty: ', len(after_double_brace2) == 0)
