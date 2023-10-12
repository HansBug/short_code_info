import os.path
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional, List, Mapping

from hbutils.system import TemporaryDirectory


@dataclass
class PyLintItem:
    file: str
    lineno: int
    charno: Optional[int]
    type: str
    message: str


@dataclass
class PyLintResult:
    items: List[PyLintItem]

    @property
    def types(self) -> Mapping[str, int]:
        retval = {}
        for item in self.items:
            retval[item.type] = retval.get(item.type, 0) + 1
        return retval

    @property
    def headers(self) -> Mapping[str, int]:
        retval = {}
        for item in self.items:
            header = item.type[0]
            retval[header] = retval.get(header, 0) + 1
        return retval


def code_pylint(code_text: str) -> PyLintResult:
    with TemporaryDirectory() as td:
        code_file = os.path.join(td, 'code.py')
        with open(code_file, 'w') as cf:
            cf.write(code_text)

        out_file = os.path.join(td, 'stdout')
        err_file = os.path.join(td, 'stderr')
        with open(out_file, 'w') as ofile, open(err_file, 'w') as efile:
            _ = subprocess.run([sys.executable, '-m', 'pylint', code_file],
                               stdout=ofile, stderr=efile)

        output_text = pathlib.Path(out_file).read_text()
        retval = []
        for line in output_text.splitlines(keepends=True):
            matching = re.fullmatch(r'^(?P<file>[\s\S]+?):(?P<lineno>\d+)(:(?P<charno>\d+))?:'
                                    r'\s+(?P<type>[A-Z]\d+):\s+(?P<message>[\s\S]+)$', line)
            if matching:
                retval.append(PyLintItem(
                    file=matching.group('file'),
                    lineno=int(matching.group('lineno')),
                    charno=int(matching.group('charno')) if matching.group('charno') else None,
                    type=matching.group('type'),
                    message=matching.group('message'),
                ))

        return PyLintResult(retval)
