from htm import *
import random

def chair_task_HTM():
	myHTM = HTM(PARALLEL)
	# myHTM.add_children([PARALLEL, "assemble seat", "assemble back", "varnish"])
	# myHTM.child(0).add_children(["assemble leg A", "assemble leg B"])
	myHTM.add_children([ARROW, ARROW])
	myHTM.child(0).add_children([PARALLEL, 'GP_seat', 'A_seat'])
	myHTM.child(0).child(0).add_children(['GP_L1', 'GP_L2', 'GP_L3', 'GP_L4'])
	myHTM.child(1).add_children([PARALLEL, 'GP_top', 'A_back'])
	myHTM.child(1).child(0).add_children(['GP_BL', 'GP_BR'])
	return myHTM


def chair_task_features():
	possible_feats = ['screwdriver_taken', 'dowel_1taken', 'dowel_2taken', 'dowel_3taken', 'dowel_4taken', 'dowel_5taken', 'dowel_6taken', 'longdowel_taken', 'frontb_1taken', 'frontb_2taken', 'backb_1taken', 'backb_2taken', 'seat_taken', 'back_taken', 'topb_1taken', 'topb_2taken', 'hold_taken']
	return sorted(possible_feats)

def generate_rand_state_seq(htm):
	traj = []
	if htm.data == ARROW:
		for child in htm.children:
			traj.extend(generate_rand_state_seq(child))
	elif htm.data == PARALLEL:
		for child in random.sample(htm.children, len(htm.children)):
			traj.extend(generate_rand_state_seq(child))
	else:
		traj += [htm.data]
	return traj



