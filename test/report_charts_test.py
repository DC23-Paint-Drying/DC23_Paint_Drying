from os import remove, listdir
import unittest

from src.report.report_charts import create_donut_chart


class ReportCharts(unittest.TestCase):
    def tearDown(self) -> None:
        for file in listdir('./'):
            if file.endswith('.png'):
                remove(file)

    def test_create_donut_chart(self) -> None:
        create_donut_chart([1, 1], ['a', 'b'])

    def test_create_donut_chart_with_no_values(self) -> None:
        with self.assertRaises(ValueError):
            create_donut_chart([], ['a', 'b'])

    def test_create_donut_chart_with_no_labels(self) -> None:
        with self.assertRaises(ValueError):
            create_donut_chart([1, 2], [])

    def test_create_donut_chart_with_not_enough_labels(self) -> None:
        with self.assertRaises(ValueError):
            create_donut_chart([1, 2], ['a'])

    def test_create_donut_chart_with_too_many_labels(self) -> None:
        with self.assertRaises(ValueError):
            create_donut_chart([1, 2], ['a', 'b', 'c'])

