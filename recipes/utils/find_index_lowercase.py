def find_index_lowercase(lst, item):
    """
    Returns the index of the first occurrence of 'item' in 'lst',
    ignoring case. Returns -1 if not found.
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(item, str):
        raise TypeError("item must be a string")

    # Convert all list elements to lowercase strings for comparison
    for idx, val in enumerate(lst):
        if isinstance(val, str) and val.lower() == item.lower():
            return idx
    return -1  # Not found
