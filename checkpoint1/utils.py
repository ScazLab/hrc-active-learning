from itertools import chain, combinations

def powerset(iterable):
	s = list(iterable)
	return chain.from_iterable(combinations(s,r) for r in range(1, len(s) + 1))