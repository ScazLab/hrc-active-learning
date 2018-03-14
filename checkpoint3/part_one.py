from htm import *

def example_HTM():
	myHTM = HTM(PARALLEL)
	# myHTM.add_children([PARALLEL, "assemble seat", "assemble back", "varnish"])
	# myHTM.child(0).add_children(["assemble leg A", "assemble leg B"])
	myHTM.add_children([ARROW, ARROW])
	myHTM.child(0).add_children([PARALLEL, 'GP_seat', 'A_seat'])
	myHTM.child(0).child(0).add_children(['GP_L1', 'GP_L2', 'GP_L3', 'GP_L4'])
	myHTM.child(1).add_children([PARALLEL, 'GP_top', 'A_back'])
	myHTM.child(1).child(0).add_children(['GP_BL', 'GP_BR'])
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



