"""
Module used to collect data for report.
"""


def get_report_data() -> dict:
    """
    Collects all required data for report and transforms it to dictionary.
    *Temporary mock, will be changed to actual data collection*

    Returns:
        Dictionary containing data for report.

    """
    return {
        'date': '10-2023',
        'users': {
            'activity': {
                'Aktywni': 15000,
                'Nieaktywni': 5000,
            },
            'gender': {
                'Mężczyźni': 8000,
                'Kobiety': 10000,
                'Inne': 2000,
            },
            'age': {
                '<18': 3000,
                '19-25': 5000,
                '26-35': 5000,
                '36-50': 4000,
                '>51': 3000,
            },
        },
        'sales': {
            'bronze': {
                'users': 8000,
                'profit': 16000,
            },
            'silver': {
                'users': 5000,
                'profit': 15000,
            },
            'gold': {
                'users': 2000,
                'profit': 8000,
            }
        },
        'recent': {
            'bronze': {
                'subscribed': 800,
                'cancelled': 250,
            },
            'silver': {
                'subscribed': 500,
                'cancelled': 150,
            },
            'gold': {
                'subscribed': 200,
                'cancelled': 100,
            }
        }
    }
