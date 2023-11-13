"""
Module containing report generation.
"""

from sys import argv
from os import remove
from os.path import join, normpath
from docx.enum import section, text
from docx.shared import RGBColor

import report_utils as utils
import report_charts as charts
from report_data import get_report_data
import src.manifest as company


def generate(directory: str = '') -> str:
    """
    Generates .docx report using data from report_data.py get_report_data.

    Args:
        directory:
            Directory to create report file to.
            If empty, creates file in working directory.

    Returns:
        Filepath to generated .docx report or empty string if it fails.
    """
    data = get_report_data()
    directory = normpath(join(directory, ''))
    filepath = normpath(join(directory, f'report-{data["date"]}.docx'))

    # generate all chart images
    users_chart = charts.create_donut_chart(list(data["users"]["subscriptions"].values()),
                                            list(data["users"]["subscriptions"].keys()))
    users_age_chart = charts.create_donut_chart(list(data["users"]["age"].values()),
                                                list(data["users"]["age"].keys()))
    users_gender_chart = charts.create_donut_chart(list(data["users"]["gender"].values()),
                                                   list(data["users"]["gender"].keys()))

    try:
        # creates blank document with styles
        document = utils.create_stylised_document()

        utils.set_footer(document, '1')

        # set first page header
        company_header_left = [f'{company.COMPANY_NAME}', f'{company.COMPANY_ADDRESS}', f'NIP {company.COMPANY_NIP}']
        company_header_right = [f'{data["timestamp"]}']
        utils.create_company_header(document, company_header_left, company_header_right)

        # set title and toc
        document.add_heading(f'Raport miesięczny', 1)
        document.add_heading(f'Okres {data["date"]}', 2)
        utils.create_table_of_contents(document, ['Użytkownicy', 'Sprzedaż', 'Ostatni miesiąc'], ['2', '3', '3'])

        document.add_section(section.WD_SECTION.NEW_PAGE)
        utils.set_footer(document, '2')

        # add table containing users data and graphs
        document.add_heading(f'Użytkownicy', 3)
        users_table = utils.create_table(document, 1, 3)
        users_table.autofit = False
        users_table.cell(0, 0).paragraphs[0].add_run(f'Liczba klientów: ')
        users_table.cell(0, 0).paragraphs[0].add_run(f'{sum(data["users"]["subscriptions"].values())}\n').bold = True
        users_table.cell(0, 0).paragraphs[0].add_run(f'Dostępne abonamenty: ')
        users_table.cell(0, 0).paragraphs[0].add_run(f'{len(company.SUBSCRIPTIONS)}\n').bold = True
        users_table.cell(0, 0).paragraphs[0].add_run(f'Dostępne pakiety: ')
        users_table.cell(0, 0).paragraphs[0].add_run(f'{len(company.PACKETS)}\n').bold = True
        users_table.cell(0, 0).paragraphs[0].paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.LEFT
        users_table.cell(0, 1).merge(users_table.cell(0, 2))
        utils.add_image_to_cell(users_table.cell(0, 1), users_chart)
        document.add_heading(f'', 2)

        users_specs_table = utils.create_table(document, 2, 2)
        utils.add_image_to_cell(users_specs_table.cell(0, 0), users_age_chart)
        utils.add_image_to_cell(users_specs_table.cell(0, 1), users_gender_chart)
        users_specs_table.cell(1, 0).paragraphs[0].text = f'Klienci wg kategorii wiekowych'
        users_specs_table.cell(1, 1).paragraphs[0].text = f'Klienci wg płci'

        document.add_section(section.WD_SECTION.NEW_PAGE)
        utils.set_footer(document, '3')

        # add sales table
        document.add_heading(f'Sprzedaż', 3)
        sales_table = utils.create_table(document, 4, 4)
        sales_table.style = 'Table Grid'
        sales_table.cell(1, 0).paragraphs[0].text = f'Liczba abonentów'
        sales_table.cell(2, 0).paragraphs[0].text = f'Przychód'
        sales_table.cell(3, 0).paragraphs[0].text = f'Łączny przychód'
        for index, key in enumerate(data["sales"]):
            sales_table.cell(0, index + 1).paragraphs[0].text = f'{key.capitalize()}'
            sales_table.cell(1, index + 1).paragraphs[0].text = f'{data["sales"][key]["users"]}'
            sales_table.cell(2, index + 1).paragraphs[0].text = f'{data["sales"][key]["profit"]:.2f} zł'
        sales_table.cell(3, 2).merge(sales_table.cell(3, 3))
        sales_table.cell(3, 1).merge(sales_table.cell(3, 2))
        sales_table.cell(3, 1).paragraphs[0].text = f'{sum(map(lambda x: data["sales"][x]["profit"], data["sales"])):.2f} zł'
        utils.change_cells_text_bold(sales_table.rows[0].cells[1:], True)
        utils.change_cells_text_bold(sales_table.rows[3].cells, True)
        utils.change_cells_background_color(sales_table.rows[0].cells, 'B7B7B7')
        utils.change_cells_background_color(sales_table.rows[1].cells, 'EFEFEF')
        utils.change_cells_background_color(sales_table.rows[2].cells, 'B7B7B7')
        utils.change_cells_background_color(sales_table.rows[3].cells, 'EFEFEF')
        document.add_heading(f'', 4)

        document.add_heading(f'Ostatni miesiąc', 3)
        summary = utils.create_table(document, 2, 3)

        # add recent statistics table
        summary_left = summary.cell(0, 0).paragraphs[0]
        summary_left.text = f'Nowi użytkownicy: '
        sl = summary_left.add_run(f'{data["recent"]["users"]}')
        sl.bold = True
        sl.font.color.rgb = RGBColor(0x38, 0x76, 0x1D)
        summary_left.paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.RIGHT

        summary_center = summary.cell(0, 1).paragraphs[0]
        summary_center.text = f'Nowe abonamenty: '
        sc = summary_center.add_run(f'{sum(map(lambda x: data["recent"]["subscribed"][x], data["recent"]["subscribed"]))}')
        sc.bold = True
        sc.font.color.rgb = RGBColor(0x38, 0x76, 0x1D)
        summary_center.paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.CENTER

        summary_right = summary.cell(0, 2).paragraphs[0]
        summary_right.text = f'Nowe pakiety: '
        sr = summary_right.add_run(f'{sum(map(lambda x: data["recent"]["packets"][x], data["recent"]["packets"]))}')
        sr.bold = True
        sr.font.color.rgb = RGBColor(0x38, 0x76, 0x1D)
        summary_right.paragraph_format.alignment = text.WD_ALIGN_PARAGRAPH.LEFT

        # add recent subscriptions table
        summary.cell(1, 1).merge(summary.cell(1, 2))
        summary.cell(1, 0).merge(summary.cell(1, 1))
        utils.delete_paragraph(summary.cell(1, 0).paragraphs[0])
        summary_subscriptions = utils.create_table(summary.cell(1, 0), 2, 1 + len(data["recent"]["subscribed"]))
        summary_subscriptions.style = 'Table Grid'
        summary_subscriptions.cell(1, 0).paragraphs[0].text = f'Zakupione abonamenty'
        for index, key in enumerate(data["recent"]["subscribed"]):
            summary_subscriptions.cell(0, index + 1).paragraphs[0].text = f'{key.capitalize()}'
            summary_subscriptions.cell(1, index + 1).paragraphs[0].text = f'{data["recent"]["subscribed"][key]}'
        utils.change_cells_text_bold(summary_subscriptions.rows[0].cells[1:], True)
        utils.change_cells_background_color(summary_subscriptions.rows[0].cells, 'B7B7B7')
        utils.change_cells_background_color(summary_subscriptions.rows[1].cells, 'EFEFEF')

        # add recent packets table
        summary_packets = utils.create_table(summary.cell(1, 0), 2, 1 + len(data["recent"]["packets"]))
        summary_packets.style = 'Table Grid'
        summary_packets.cell(1, 0).paragraphs[0].text = f'Zakupione pakiety'
        for index, key in enumerate(data["recent"]["packets"]):
            summary_packets.cell(0, index + 1).paragraphs[0].text = f'{key.capitalize()}'
            summary_packets.cell(1, index + 1).paragraphs[0].text = f'{data["recent"]["packets"][key]}'
        utils.change_cells_text_bold(summary_packets.rows[0].cells[1:], True)
        utils.change_cells_background_color(summary_packets.rows[0].cells, 'B7B7B7')
        utils.change_cells_background_color(summary_packets.rows[1].cells, 'EFEFEF')

        document.save(filepath)

    except Exception:
        filepath = f''

    finally:
        # image cleanup
        remove(users_chart)
        remove(users_age_chart)
        remove(users_gender_chart)

    return filepath


# for development and command line generation
if __name__ == '__main__':
    globals()[argv[1]](argv[2] if 2 < len(argv) else './')
