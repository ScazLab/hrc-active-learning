from htm import *

from collections import Counter
import random
# random.seed(0)


def example_sup_actions():
	# return set(['wave', 'smile', 'hold', 'bring new part'])
	return set(['dowel', 'long_dowel', 'screwdriver', 'top_bracket', 'back_bracket', 'front_bracket', 'hold', 'seat', 'back'])
	# return set(['act1', 'act2', 'act3', 'act4', 'act5', 'act6', 'act7', 'act8'])

def chair_task_features():
	return ['seat_taken', '1dowel_taken', '2dowel_taken', '3dowel_taken', '4dowel_taken', 'screwdriver_taken', 'back_taken', '1frontb_taken', '2frontb_taken', '1backb_taken', '2backb_taken', '1topb_taken', '2topb_taken']

def generate_reasonable_features():
	pass
	

def generate_reasonable_train_labels(traj):
	#not perfect, but always reasonable. WIll improve with feature-based
	# print traj
	labels = []
	brackets_first = random.random() > .6 
	# print brackets_first

	top_brackets = 0

	for timestep, taskstep in enumerate(traj):
		supp_acts = []
		if taskstep == 'GP_L1' or taskstep == 'GP_L2':
			if brackets_first:
				supp_acts += ['front_bracket', 'dowel']
			else:
				supp_acts += ['dowel', 'front_bracket']

		elif taskstep == 'GP_L3' or taskstep == 'GP_L4':
			if brackets_first:
				supp_acts += ['back_bracket', 'dowel']
			else:
				supp_acts += ['dowel', 'back_bracket']
		elif taskstep == 'GP_seat':
			supp_acts += ['seat']
		elif taskstep == 'A_seat' or taskstep == 'A_back':
			supp_acts += random.choice([['hold'],[]]) #might want to skew this in favor of empty
		elif taskstep == 'GP_BL' or taskstep == 'GP_BR':
			supp_acts += ['dowel']
			if random.random() > .5 or top_brackets > 0 or timestep == 0:
				supp_acts += ['top_bracket']
				top_brackets += 1
			random.shuffle(supp_acts)
		elif taskstep == 'GP_top':
			while top_brackets < 2 :
				supp_acts += ['top_bracket']
				top_brackets += 1
			supp_acts += ['long_dowel']
			random.shuffle(supp_acts)
		if timestep == 0:
			supp_acts += ['screwdriver']

		# random.shuffle(supp_acts)
		# print supp_acts
		supp_acts = tuple(supp_acts)
		# print timestep 
		# print supp_acts
		labels += [supp_acts]

	return labels

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

