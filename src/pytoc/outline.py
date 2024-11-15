from typing import List, Self
from pikepdf import Pdf, OutlineItem, PageLocation
from json import JSONDecoder, JSONEncoder
from dataclasses import dataclass


@dataclass
class OutlineData:
    title: str
    page: str | int
    children: List[Self] | None = None


    class Encoder(JSONEncoder):
        def default(self, obj):
            def _encode(obj):
                if obj.children != None:
                    children = [_encode(child) for child in obj.children]
                else:
                    children = None
                return {
                    'title': obj.title,
                    'page': obj.page,
                    'children': children
                }
        
            if isinstance(obj, OutlineData):
                return _encode(obj)
            elif isinstance(obj, list):
                return [_encode(child) for child in obj]
            return super().default(obj)
        
    
    class Decoder(JSONDecoder):
        def __init__(self, *args, **kwargs):
            super().__init__(object_hook=self.as_outline, *args, **kwargs)

        def as_outline(self, obj):
            if isinstance(obj, OutlineData):
                return obj

            if obj['children'] == None:
                children = None
            else:
                children = [self.as_outline(child) for child in obj['children']]
            return OutlineData(obj['title'], obj['page'], children)


    def create(self, pdf: Pdf) -> OutlineItem:
        idx = None
        # Is there a more efficient way to find the page index based on page label?
        for i, page in enumerate(pdf.pages):
            if page.label == str(self.page):
                idx = i
                break
        left = pdf.pages[1].mediabox[2]
        top = pdf.pages[1].mediabox[3]
        outline = OutlineItem(self.title, idx, PageLocation.XYZ, left=left, top=top, zoom=0)
        if self.children:
            outline.children = [child.create(pdf) for child in self.children]
        return outline