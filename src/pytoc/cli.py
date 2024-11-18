from typing import Optional
import typer
from .main import fix_toc, fix_width

app = typer.Typer()


@app.command()
def add(input: str, json: str, output: Optional[str] = None):
    if output == None:
        output = _output_name(input)
    with open(json, 'r') as f:
        fix_toc(input, output, f.read())
        print(f'Done fixing `{input}`')

@app.command()
def fixw(input: str, output: Optional[str] = None):
    if output == None:
        output = _output_name(input)
    fix_width(input, output)
    print(f'Done')


def _output_name(input: str):
    return f'(fixed) {input}'