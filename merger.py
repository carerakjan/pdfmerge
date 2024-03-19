from typing import IO, Any, List
from pypdf import PdfMerger, PdfReader, PdfWriter
from pathlib import Path


class Merger(PdfWriter):
    def __init__(self, fileobj: str | IO[Any] = "", clone_from: None | PdfReader | str | IO[Any] | Path = None,
                 pdf_files=[], pdf_dir='') -> None:
        super().__init__(fileobj, clone_from)
        self.__merge_pdfs(pdf_files, pdf_dir)

    def __merge_pdfs(self, pdf_files, pdf_dir):
        pdfs = []

        if pdf_files:
            pdfs = list(filter(lambda src: bool(src), pdf_files))
        elif pdf_dir:
            dir_path = Path(pdf_dir)
            pdfs = [str(file.absolute()) for file in dir_path.iterdir()]

        for pdf in pdfs:
            self.append(pdf)

    def write_to_file(self, file_name: str):
        output = open(file_name, 'wb')
        self.write(output)
