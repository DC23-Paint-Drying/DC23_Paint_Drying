"""
Module containing chart generation functions used in report.
"""


import uuid

import matplotlib.pyplot as plt


def create_donut_chart(values: list[int], labels: list[str]) -> str:
    """
    Creates donut chart image and returns path to it.
    Zero values will be not be included in the chart.

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

    # remove zero values from values list and its corresponding label in labels list
    filtered = dict(filter(lambda x: x[1] > 0, dict(zip(labels, values)).items()))

    fig, ax = plt.subplots()
    fig.set_figwidth(6.0)
    fig.set_figheight(6.0)
    _, texts = ax.pie(filtered.values(),
                      labels=filtered.keys(),
                      textprops={'weight': 'bold'},
                      labeldistance=0.75,
                      startangle=180.0)
    for t in texts:
        t.set_horizontalalignment('center')
    ax.add_artist(plt.Circle((0, 0), 0.5, color='White'))
    filename = f'{uuid.uuid4()}.png'
    plt.savefig(filename, bbox_inches='tight', pad_inches=-0.3)
    return filename
