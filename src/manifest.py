
COMPANY_NAME = "PaintDryin Inc."
COMPANY_ADDRESS = "Paintburg, Paint Street 54/6"
COMPANY_NIP = "123-456-78-90"
COMPANY_BANK_ACCOUNT = "12 3456 7890 0000 0000 1234 5678"

# subscription name must be in female form
SUBSCRIPTIONS = {
    "basic": {
        "name": "Podstawowa",
        "price": 12.99
    },
    "standard": {
        "name": "Standardowa",
        "price": 39.99
    },
    "premium": {
        "name": "Premium",
        "price": 56.99
    }
}

# packet name must be in male form
PACKETS = {
    "monthly": {
        "name": "Miesięczny",
        "description": "Ten pakiet oferuje rotacyjny wybór comiesięcznych scen schnięcia farby, dzięki czemu zawartość jest świeża i ekscytująca.",
        "duration": 31,
        "price": 9.99
    },
    "family": {
        "name": "Rodzinny",
        "description": "Ten pakiet, przeznaczony dla rodzin, umożliwia wielu profilom korzystanie z treści związanych ze schnięciem farby na jednym koncie.",
        "duration": 31,
        "price": 12.99
    }
}


class USER_TYPES:
    ADMIN = "admin"
    NORMAL = "normal"
