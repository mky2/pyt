from typing import List
from pikepdf import Pdf, Page, OutlineItem
from .outline import OutlineData


def fix_toc(input: str, output: str, js: str):
    outline_data: List[OutlineData] = OutlineData.Decoder().decode(js)
    with Pdf.open(input) as pdf:
        with pdf.open_outline() as outline:
            outline.root.clear()
            outline.root.extend([child.create(pdf) for child in outline_data])
        pdf.save(output)


def _update_item(item: OutlineItem):
    if item.action and "/D" in item.action:
        dest = Page(item.action["/D"][0]).label
    elif item.destination:
        dest = Page(item.destination[0]).label
    if item.children:
        children = [_update_item(child) for child in item.children]
    else:
        children = None
    return OutlineData(item.title, dest, children)


def fix_width(input: str, output: str):
    with Pdf.open(input) as pdf:
        with pdf.open_outline() as outline:
            updated_items = [_update_item(i).create(pdf) for i in outline.root]
            outline.root.clear()
            outline.root.extend(updated_items)
        pdf.save(output)