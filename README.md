# short_code_info

Get Information for Short Code

```python
import pathlib

from codeinfo import code_cc, code_pylint, code_pep8, code_sugar

for i in range(1, 21):
    code_file = f'test/testfile/{i}.py'
    code_text = pathlib.Path(code_file).read_text()
    pylint_result = code_pylint(code_text)
    pep8_result = code_pep8(code_text)
    cc_value = code_cc(code_text)
    print(code_file, pylint_result.headers, pep8_result.headers, cc_value, code_sugar(code_text))

```