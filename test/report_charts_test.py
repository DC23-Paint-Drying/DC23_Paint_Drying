from os import remove, listdir

import pytest

from src.report.report_charts import create_donut_chart


@pytest.fixture(autouse=True)
def cleanup_files():
    yield
    for file in listdir('./'):
        if file.endswith('.png'):
            remove(file)


def test_create_donut_chart():
    create_donut_chart([1, 1], ['a', 'b'])


def test_create_donut_chart_with_no_values():
    with pytest.raises(ValueError):
        create_donut_chart([], ['a', 'b'])


def test_create_donut_chart_with_no_labels():
    with pytest.raises(ValueError):
        create_donut_chart([1, 2], [])


def test_create_donut_chart_with_not_enough_labels():
    with pytest.raises(ValueError):
        create_donut_chart([1, 2], ['a'])


def test_create_donut_chart_with_too_many_labels():
    with pytest.raises(ValueError):
        create_donut_chart([1, 2], ['a', 'b', 'c'])
