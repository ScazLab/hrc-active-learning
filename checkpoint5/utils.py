from itertools import chain, combinations


def powerset(iterable):
	s = list(iterable)
	return chain.from_iterable(combinations(s,r) for r in range(1, len(s) + 1))

def prettyprint(matrix, sort=True, labels=None):
	if isinstance(matrix, dict):
		max_len = max([len(str(k)) for k in matrix.keys()]) + 1
		if labels is not None:
			print '__' + str(labels[0]) + '__' + str(' ' * (max_len - len(str(labels[0])))) + '__' + str(labels[1]) + '__'
		
		if sort:
			for key in sorted(matrix.keys()):
				print str(key) + str(' ' * (max_len - len(str(key))))  + str(matrix[key])
		else:
			for key in matrix.keys():
				print str(key) + str(' ' * (max_len - len(str(key))))  + str(matrix[key])
		print
	else:

		#from online:
		s = [[str(e) for e in row] for row in matrix]
		lens = [max(map(len, col)) for col in zip(*s)]
		fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
		table = [fmt.format(*row) for row in s]
		print '\n'.join(table)
		print




