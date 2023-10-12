# short_code_info

Get Information for Short Code

```python
import pathlib

from codeinfo.cc import code_cc
from codeinfo.pylint import code_pylint

for i in range(1, 21):
    code_text = pathlib.Path(f'test/testfile/{i}.py').read_text()
    result = code_pylint(code_text)
    print(i, result.get_type_header_analysis(), code_cc(code_text))

```