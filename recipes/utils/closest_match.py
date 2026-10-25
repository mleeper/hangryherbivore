import Levenshtein
from fuzzywuzzy import fuzz, process

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

def match_ingredient(query, choices, threshold=70):
    """
    Match an ingredient name against a list using fuzzy matching.

    :param query: Ingredient name to search for (string)
    :param choices: List of known ingredient names
    :param threshold: Minimum similarity score to consider a match
    :return: Best match and score, or None if below threshold
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string.")

    # Get the best match from the list
    best_match, score = process.extractOne(query, choices, scorer=fuzz.partial_ratio)

    if score >= threshold:
        return best_match, score
    else:
        return None