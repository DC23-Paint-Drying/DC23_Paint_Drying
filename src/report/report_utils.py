"""
Module containing utility functions used during report generation.
"""


import uuid

from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table, _Cell
from docx.enum import table, text
from docx.shared import Emu, Pt, RGBColor
from docx.oxml.shared import qn, OxmlElement
from matplotlib.pyplot import subplots, Circle, savefig


def create_stylised_document() -> Document:
    """
    Creates document and sets all styles for headings and tables.

    Returns:
        Reference to created document.

    """
    document = Document()

    # color definitions
    black = RGBColor(0x23, 0x23, 0x23)
    gray = RGBColor(0x6a, 0x6a, 0x6a)

    # non heading text
    normal = document.styles['Normal']
    normal.font.size = Pt(13)
    normal.font.bold = False
    normal.font.italic = True
    normal.font.name = 'Calibri'
    normal.font.color.rgb = black

    # title
    heading1 = document.styles['Heading 1']
    heading1.paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.CENTER
    heading1.paragraph_format.space_before = False
    heading1.font.size = Pt(26)
    heading1.font.bold = False
    heading1.font.italic = False
    heading1.font.name = 'Arial'
    heading1.font.color.rgb = black

    # subtitle
    heading2 = document.styles['Heading 2']
    heading2.paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.CENTER
    heading2.paragraph_format.space_before = False
    heading2.paragraph_format.space_after = Pt(10)
    heading2.font.size = Pt(15)
    heading2.font.bold = False
    heading2.font.italic = False
    heading2.font.name = 'Arial'
    heading2.font.color.rgb = gray

    # section heading
    heading3 = document.styles['Heading 3']
    heading3.paragraph_format.space_before = Pt(16)
    heading3.paragraph_format.space_after = Pt(6)
    heading3.font.size = Pt(20)
    heading3.font.bold = True
    heading3.font.italic = False
    heading3.font.name = 'Calibri'
    heading3.font.color.rgb = black

    # table of contents
    heading4 = document.styles['Heading 4']
    heading4.paragraph_format.space_before = False
    heading4.paragraph_format.space_after = False
    heading4.paragraph_format.line_spacing_rule = text.WD_LINE_SPACING.SINGLE
    heading4.font.size = Pt(14)
    heading4.font.bold = True
    heading4.font.italic = False
    heading4.font.name = 'Calibri'
    heading4.font.color.rgb = black

    # page number
    heading5 = document.styles['Heading 5']
    heading5.paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.RIGHT
    heading5.paragraph_format.space_before = False
    heading5.paragraph_format.space_after = False
    heading5.font.size = Pt(12)
    heading5.font.bold = False
    heading5.font.italic = False
    heading5.font.name = 'Calibri'
    heading5.font.color.rgb = black

    return document


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
    document.sections[-1].footer.paragraphs[0].style = 'Heading 5'


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
        row.height_rule = table.WD_ROW_HEIGHT_RULE.AT_LEAST
        row.height = Pt(30)
        for cell in row.cells:
            cell.paragraphs[0].paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.CENTER
            cell.vertical_alignment = table.WD_CELL_VERTICAL_ALIGNMENT.CENTER
    return t


def delete_paragraph(paragraph: Paragraph) -> None:
    """
    Deletes passed paragraph from parent element.

    Args:
        paragraph:
            Paragraph to delete.

    Returns:

    """
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None


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


def change_cells_text_bold(cells: [_Cell], value: bool) -> None:
    """
    Changes text bold setting for each cell in list.

    Args:
        cells:
            List of cells to change text of.
        value:
            Bold value to set text to.

    Returns:

    """
    for cell in cells:
        t = cell.paragraphs[0].text
        cell.paragraphs[0].text = f''
        cell.paragraphs[0].add_run(t).bold = value


def change_cells_text_color(cells: [_Cell], color: RGBColor) -> None:
    """
    Changes text color setting for each cell in list.

    Args:
        cells:
            List of cells to change text of.
        color:
            RGB color to set text to.

    Returns:

    """
    for cell in cells:
        t = cell.paragraphs[0].text
        cell.paragraphs[0].text = f''
        cell.paragraphs[0].add_run(t).font.color.rgb = color


def change_cells_background_color(cells: [_Cell], color: str) -> None:
    """
    Changes background color setting for each cell in list.

    Args:
        cells:
            List of cells to change background of.
        color:
            RGB color to set background to.

    Returns:

    """
    for cell in cells:
        properties = cell._element.tcPr
        try:
            shading = properties.xpath('w:shd')[0]
        except IndexError:
            shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), color)
        properties.append(shading)


def create_donut_chart(values: [int], labels: [str]) -> str:
    """
    Creates donut chart image and returns path to it.

    Args:
        values:
            Array containing values for each wedge.
        labels:
            Array containing labels for each value.

    Returns:
        Path to image file with donut chart.

    """

    if not values or not labels:
        raise ValueError('Values and labels must not be empty')

    if len(values) != len(labels):
        raise ValueError('Each value must have exactly one label')

    fig, ax = subplots()
    fig.set_figwidth(6.0)
    fig.set_figheight(6.0)
    _, texts = ax.pie(values, labels=labels, textprops={'weight': 'bold'}, labeldistance=0.75, startangle=180.0)
    for t in texts:
        t.set_horizontalalignment('center')
    ax.add_artist(Circle((0, 0), 0.5, color='White'))
    filename = f'{uuid.uuid4()}.png'
    savefig(filename, bbox_inches='tight', pad_inches=-0.3)
    return filename
