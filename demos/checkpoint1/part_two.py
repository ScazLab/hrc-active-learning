from htm import *

from collections import Counter
import random
# random.seed(0)


def example_sup_actions():
	return set(['wave', 'smile', 'hold', 'bring new part'])

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


def generate_valid_Oi_seq(htm, f):
	traj = generate_rand_state_seq(htm)
	Oi_seq = [f[si] for si in traj]
	return Oi_seq

def uncertainty_score(user_pref_dict, thres):
	uncertainty_dict = {}
	for taskstep in user_pref_dict.keys():
		# print user_pref_dict[taskstep].most_common(1)[0][1]
		if user_pref_dict[taskstep].most_common(1)[0][1] < thres:
			uncertainty_dict[taskstep] = True
		else:
			uncertainty_dict[taskstep] = False
	# print uncertainty_dict
	return uncertainty_dict
		