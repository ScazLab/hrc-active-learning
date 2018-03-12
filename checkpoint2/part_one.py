from htm import *

def example_HTM():
	myHTM = HTM(ARROW)
	myHTM.add_children([PARALLEL, "assemble seat", "assemble back", "varnish"])
	myHTM.child(0).add_children(["assemble leg A", "assemble leg B"])
	return myHTM

def example_obs():
	return ['ob1', 'ob2', 'ob3', 'ob4', 'ob5', 'ob6', 'ob7', 'ob8', 'ob9']

def get_leaves(htm):
	leaves = []
	for child in htm.children:
		if len(child.children) ==0 :
			leaves.append(child.data)
		else:
			leaves += get_leaves(child)
	return leaves



