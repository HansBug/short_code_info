from typing import Optional

from radon.complexity import cc_visit


def code_cc(code) -> Optional[int]:
    try:
        results = cc_visit(code)
        return sum((block.complexity for block in results), 0)
    except (IndentationError, SyntaxError):
        return None
