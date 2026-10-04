import Levenshtein

def find_closest_match_levenshtein(target, candidates):
    """
    Find the closest matching string from a list using Levenshtein distance.

    :param target: The string to match.
    :param candidates: List of strings to search.
    :return: Closest match or None if list is empty.
    """
    # Validate inputs
    if not isinstance(target, str) or not target.strip():
        raise ValueError("Target must be a non-empty string.")
    if not isinstance(candidates, list) or not all(isinstance(c, str) for c in candidates):
        raise ValueError("Candidates must be a list of strings.")
    if not candidates:
        return None

    # Find the candidate with the smallest edit distance
    closest = min(candidates, key=lambda c: Levenshtein.distance(target, c))
    return closest