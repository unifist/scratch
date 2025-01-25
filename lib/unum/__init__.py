import Levenshtein

def closest(haystack, needle):
    """ Finds the closet match ina set of value """

    return sorted(haystack, key=lambda value: Levenshtein.distance(value, needle))[0]
