"""
Module containing utility functions used during report generation
"""


import uuid

from docx import Document
from docx.table import Table, _Cell
from docx.enum import table, text
from docx.shared import Emu
import matplotlib.pyplot as plt


def set_footer(document: Document, page_number: str) -> None:
    """
    Sets page number for current section.

    Args:
        document:
            Document to add footer to.
        page_number:
            Page number to add in the right corner of footer.

    Returns:

    """
    document.sections[-1].footer.is_linked_to_previous = False
    document.sections[-1].footer.paragraphs[0].text = f'\t\t{page_number}'


def create_table(document: Document, rows: int, cols: int) -> Table:
    """
    Creates and adds new table of size rows x cols.
    The table is centered on page.
    All cells are vertically and horizontally aligned.

    Args:
        document:
            Document to add table to.
        rows:
            Amount of rows in table.
        cols:
            Amount of columns in table.

    Returns:
        Reference to created table.

    """

    if rows < 1 or cols < 1:
        raise ValueError('Row and column size must be atleast 1')

    t = document.add_table(rows=rows, cols=cols)
    t.alignment = table.WD_TABLE_ALIGNMENT.CENTER
    for row in t.rows:
        for cell in row.cells:
            cell.paragraphs[0].paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.CENTER
            cell.vertical_alignment = table.WD_CELL_VERTICAL_ALIGNMENT.CENTER
    return t


def add_image_to_cell(cell: _Cell, image: str) -> None:
    """
    Adds image to provided table cell.

    Args:
        cell:
            Reference to cell.
        image:
            File path to image.

    Returns:

    """
    cell.paragraphs[0].add_run().add_picture(image, Emu(cell.width))


def create_donut_chart(values: [int], labels: [str]) -> str:
    """
    Creates donut chart image and returns path to it

    Args:
        values:
            Array containing values for each wedge
        labels:
            Array containing labels for each value

    Returns:
        Path to image file with donut chart

    """

    if not values or not labels:
        raise ValueError('Values and labels must not be empty')

    if len(values) != len(labels):
        raise ValueError('Each value must have exactly one label')

    fig, ax = plt.subplots()
    fig.set_figwidth(6.0)
    fig.set_figheight(6.0)
    _, texts = ax.pie(values, labels=labels, textprops={'weight': 'bold'}, labeldistance=0.75, startangle=180.0)
    for t in texts:
        t.set_horizontalalignment('center')
    ax.add_artist(plt.Circle((0, 0), 0.5, color='White'))
    filename = f'{uuid.uuid4()}.png'
    plt.savefig(filename, bbox_inches='tight')
    return filename
