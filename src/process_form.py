
def process_form(**kwargs: str) -> dict:
    """
    Processes data from a form to a dictionary.

    :param kwargs: keyworded, variable-length argument list with data from the form
    """
    record = {}
    for (key, value) in kwargs.items():
        record[key] = value
    return record

