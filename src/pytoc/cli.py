from typing import Optional
import typer
from .main import fix_toc

app = typer.Typer()

@app.command()
def main(input: str, json: str, output: Optional[str] = None):
    if output == None:
        output = f'(fixed) {input}'
    with open(json, 'r') as f:
        fix_toc(input, output, f.read())
        print(f'Done fixing `{input}`')