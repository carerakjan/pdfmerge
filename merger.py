from typing import IO, Any, List
from pypdf import PdfMerger, PdfReader, PdfWriter
from pathlib import Path

class Merger(PdfWriter):
    def __init__(self, fileobj: str | IO[Any] = "", clone_from: None | PdfReader | str | IO[Any] | Path = None) -> None:
        super().__init__(fileobj, clone_from)

    def merge_pdfs(self, sources: List[str]):
        pdfs = list(filter(lambda src: bool(src), sources))
        for pdf in pdfs:
            self.append(pdf)
           
    def merge_from_dir(self, dir_name: str):
        dir_path = Path(dir_name)
        sources = [str(file.absolute()) for file in dir_path.iterdir()]
        self.merge_pdfs(sources)

    def write_to_file(self, file_name: str):
        output = open(file_name, 'wb')
        self.write(output)
