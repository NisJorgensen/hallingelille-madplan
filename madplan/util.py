
def kommaliste (liste):
	liste = [unicode (x) for x in liste]
	l = len(liste)
	if l == 0: return ''
	if l == 1: return liste[0]
	return u' og '.join([u', '.join(liste[0:-1]),liste[-1]])

def remove_dups(seq):
    """Returns the elements of seq in the same order, with all duplicates removed"""
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

