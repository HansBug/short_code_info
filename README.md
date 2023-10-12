# short_code_info

Get Information for Short Code

If you need to use function `code_gpt`, you need to set environment variable `OPENAI_KEY`, like this

```shell
export OPENAI_KEY=your-openai-key-for-chatgpt
```

Here is the full example:

```python
import pathlib

from codeinfo import code_cc, code_pylint, code_pep8, code_sugar, code_gpt

for i in range(1, 21):
    code_file = f'test/testfile/{i}.py'
    code_text = pathlib.Path(code_file).read_text()
    pylint_result = code_pylint(code_text)
    pep8_result = code_pep8(code_text)
    cc_value = code_cc(code_text)
    print(
        code_file,
        pylint_result.headers,
        pep8_result.headers,
        cc_value,
        code_sugar(code_text),
        code_gpt(code_text)
    )

```

Attention that:

* Result of `code_cc` and `code_sugar` function will return `None` when the syntax of given Python code is wrong.
* Result of `code_gpt` will be `None` when the ChatGPT not return as the required format.
* Keys of headers of pylint and pep8 result means the severity of the code style problem.

That is all, have fun with it :)
