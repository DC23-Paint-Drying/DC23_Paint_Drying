from os import remove, listdir

import pytest
from docx import Document

import src.report.report_utils as utils


@pytest.fixture(autouse=True)
def cleanup_files():
    yield
    for file in listdir('./'):
        if file.endswith('.png'):
            remove(file)


def test_set_footer():
    document = Document()
    text = '1'
    utils.set_footer(document, text)
    assert text in document.sections[-1].footer.paragraphs[0].text


def test_create_table_with_valid_size():
    document = Document()
    table = utils.create_table(document, 2, 3)
    assert len(table.rows) == 2
    assert len(table.columns) == 3


def test_create_table_with_invalid_size():
    document = Document()
    with pytest.raises(ValueError):
        utils.create_table(document, -1, -1)


def test_create_donut_chart():
    utils.create_donut_chart([1, 1], ['a', 'b'])


def test_create_donut_chart_with_no_values():
    with pytest.raises(ValueError):
        utils.create_donut_chart([], ['a', 'b'])


def test_create_donut_chart_with_no_labels():
    with pytest.raises(ValueError):
        utils.create_donut_chart([1, 2], [])


def test_create_donut_chart_with_not_enough_labels():
    with pytest.raises(ValueError):
        utils.create_donut_chart([1, 2], ['a'])


def test_create_donut_chart_with_too_many_labels():
    with pytest.raises(ValueError):
        utils.create_donut_chart([1, 2], ['a', 'b', 'c'])


def test_add_nonexistent_image_to_cell():
    document = Document()
    table = utils.create_table(document, 1, 1)
    cell = table.cell(0, 0)
    with pytest.raises(FileNotFoundError):
        utils.add_image_to_cell(cell, 'doesnt_exist.png')
