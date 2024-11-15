from typing import List
from .outline import OutlineData
from pikepdf import Pdf


def fix_toc(input: str, output: str, js: str):
    outline_data: List[OutlineData] = OutlineData.Decoder().decode(js)
    with Pdf.open(input) as pdf:
        with pdf.open_outline() as outline:
            outline.root.clear()
            outline.root.extend([child.create(pdf) for child in outline_data])
        pdf.save(output)