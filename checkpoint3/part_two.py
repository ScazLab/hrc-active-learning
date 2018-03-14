from htm import *

from collections import Counter
import random
# random.seed(0)


def example_sup_actions():
	# return set(['wave', 'smile', 'hold', 'bring new part'])
	return set(['bring dowel', 'bring long dowel', 'bring screwdriver', 'bring top bracket', 'bring back bracket', 'bring front bracket', 'hold'])

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
	for t,Oi in user_pref_dict.keys():
		# print user_pref_dict[taskstep].most_common(1)[0][1]
		if user_pref_dict[(t,Oi)].most_common(1)[0][1] < thres:
			uncertainty_dict[(t,Oi)] = True
		else:
			uncertainty_dict[(t,Oi)] = False
	# print uncertainty_dict
	return uncertainty_dict

# def uncertainty_score_2(user_pref_dict): #inaccurate
# 	uncertainty_dict = {}
# 	for t, Oi in  user_pref_dict.keys():
# 		# if user_pref_dict[(t,Oi)].most_common(1)[0][1] < float(len(user_pref_dict[(t,Oi)])) / 2:

# 			uncertainty_dict[(t,Oi)] = True
# 		else:
# 			uncertainty_dict[(t,Oi)] = False
# 	return uncertainty_dict