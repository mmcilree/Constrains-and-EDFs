def flatten(t):
    if isinstance(t[0], list):
        return [item for sublist in t for item in sublist]
    else:
        return t
        
# Copied from: https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
# Checks if all items in in iterable are equal
def all_equal(arr):
    iterator = flatten(arr)
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)