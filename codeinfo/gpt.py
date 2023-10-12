import os
import re
from functools import lru_cache
from typing import Optional

import openai


@lru_cache()
def _setup_openai():
    openai.api_key = os.environ['OPENAI_KEY']


def code_gpt(code_text) -> Optional[str]:
    _setup_openai()

    messages = []
    messages.append({
        "role": "system",
        "content": """
I will show you some parts of Python code, please evaluate its quality of naming of functions, variables, classes or something within 5 levels (A/B/C/D/E, A is the best, E is the worst) in the following format:

Naming Quality: A/B/C/D/E
        """
    })
    messages.append({
        "role": "user",
        "content": f"""
```python
{code_text}
```
    """})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_text = response["choices"][0]["message"]["content"]
    findings = re.findall(r'quality:\s*(?P<quality>[ABCDE])', response_text, re.IGNORECASE)
    if findings:
        return findings[0].upper()
    else:
        return None
