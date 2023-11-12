from os import remove, listdir, environ
from os.path import exists

import pytest
from docx import Document

from src.report.report_utils import convert_docx_to_pdf


@pytest.fixture(autouse=True)
def file_cleanup():
    yield
    for file in listdir('./'):
        if file.endswith('.docx'):
            remove(file)
        if file.endswith('.pdf'):
            remove(file)


def test_convert_docx_to_pdf():
    document = Document()
    document.save('test.docx')
    assert exists('test.docx')

    convert_docx_to_pdf('test.docx', '')
    assert exists('test.pdf')
