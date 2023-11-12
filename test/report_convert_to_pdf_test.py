from os import remove, listdir
from os.path import exists
import unittest

from docx import Document

from src.report.report_utils import convert_docx_to_pdf


class ReportPDFConvertTests(unittest.TestCase):
    def tearDown(self) -> None:
        for file in listdir('./'):
            if file.endswith('.docx'):
                remove(file)
            if file.endswith('.pdf'):
                remove(file)

    def test_convert_docx_to_pdf(self) -> None:
        document = Document()
        document.save('test.docx')
        assert exists('test.docx')

        convert_docx_to_pdf('test.docx', '')
        assert exists('test.pdf')
