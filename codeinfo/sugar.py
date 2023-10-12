import ast


def _has_decorator(node: ast.AST):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return len(node.decorator_list) > 0
    else:
        return False


def _is_chain_compare(node: ast.AST):
    if isinstance(node, ast.Compare):
        return len(node.comparators) > 1
    else:
        return False


_SIMPLE_DICT = {
    'with': (ast.With, ast.AsyncWith),
    'comp': (ast.ListComp, ast.DictComp, ast.SetComp),
    'ifexp': (ast.IfExp,),
    'decorator': _has_decorator,
    'chaincmp': _is_chain_compare,
    'lambda': (ast.Lambda,),
    'async': (ast.AsyncWith, ast.AsyncFor, ast.AsyncFunctionDef),
}


def _count_for_nodes(parsed_code: ast.AST, check_dict):
    records = {}

    class SugarCounter(ast.NodeVisitor):
        def visit(self, node):
            for key, value in check_dict.items():
                if isinstance(value, tuple) or (isinstance(value, type) and issubclass(value, ast.AST)):
                    check = isinstance(node, value)
                else:
                    check = value(node)

                if check:
                    records[key] = records.get(key, 0) + 1

            self.generic_visit(node)

    # 实例化访问者并访问AST
    counter = SugarCounter()
    counter.visit(parsed_code)

    return records


def code_sugar(code_text: str, mode: str = 'simple'):
    if mode == 'simple':
        check_dict = _SIMPLE_DICT
    else:
        raise ValueError(f'Unknown mode - {mode!r}.')

    try:
        parsed_code = ast.parse(code_text)
    except (IndentationError, SyntaxError):
        return None

    return _count_for_nodes(parsed_code, check_dict)
