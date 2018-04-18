from htm import *

from collections import Counter
import random
# random.seed(0)


def example_sup_actions():
	# return set(['wave', 'smile', 'hold', 'bring new part'])
	return set(['dowel', 'long_dowel', 'screwdriver', 'top_bracket', 'back_bracket', 'front_bracket', 'hold', 'seat', 'back'])
	# return set(['act1', 'act2', 'act3', 'act4', 'act5', 'act6', 'act7', 'act8'])

def example_additional_features():
	return ['seat_taken', '1dowel_taken', '2dowel_taken', '3dowel_taken', '4dowel_taken', 'screwdriver_taken', 'back_taken', '1frontb_taken', '2frontb_taken', '1backb_taken', '2backb_taken', '1topb_taken', '2topb_taken']

def generate_reasonable_train_labels(Oi_seq):
	# if Oi_seq[0] is 
	pass
	return

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

def uncertainty_score(user_pref_dict):
	uncertainty_dict = {}
	for k in user_pref_dict.keys():
		if user_pref_dict[k].most_common(1)[0][1] <= float(sum(user_pref_dict[k].values()))/2.0:
			uncertainty_dict[k] = True
		else:
			uncertainty_dict[k] = False
	return uncertainty_dict

