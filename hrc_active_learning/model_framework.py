import chair_assembly_task
from utils import *

from collections import defaultdict, Counter


"""
Heuristics used to generate labels:
1. Always give the screwdriver first (what I remember made most sense for folks during Corina's user tests) - change
2. Humans want (bracket, dowel) for each of the four legs because according to the HTM GP_seat comes afterwards
(eliminates the possibility of wanting (seat and all four brackets for GP_seat and only dowels for each GP_L#))
3. introduced: you want them in the order bracket, dowel or dowel, brack for all for legs. I think given the above contraints this makes sense for a real worker.
4. GP_BR, GP_BL, GP_top: appropriate dowels for each, flip a coin to give the bracket along with it, and just make sure that all brackets are given by the end.
Randomize the ordering of these being delivered.
5. A_seat, A_top: decide between hold or ()
6. No other options for () as a label (gathering parts is assumed to be out of scope of the human's tasks)
"""


# def chair_task_sim_user_labels(traj): #change to return in form (timestep_feats_tuple, supp_acts_tuple)
# 	labels = []
# 	feature_seq = [()]

# 	brackets_first = random.random() > .6
# 	dowels = 0
# 	front_brackets =0
# 	back_brackets = 0
# 	top_brackets = 0

# 	for timestep, taskstep in enumerate(traj):

# 		supp_acts = []
# 		feats = []

# 		if taskstep == 'GP_L1' or taskstep == 'GP_L2':
# 			if brackets_first:
# 				supp_acts += ['front_bracket', 'dowel']
# 			else:
# 				supp_acts += ['dowel', 'front_bracket']
# 			front_brackets +=1
# 			dowels +=1
# 			feats += ['dowel_{}taken'.format(dowels),'frontb_{}taken'.format(front_brackets)]

		# elif taskstep == 'GP_L3' or taskstep == 'GP_L4':
		# 	if brackets_first:
		# 		supp_acts += ['back_bracket', 'dowel']
		# 	else:
		# 		supp_acts += ['dowel', 'back_bracket']
		# 	back_brackets += 1
		# 	dowels += 1
		# 	feats += ['dowel_{}taken'.format(dowels), 'backb_{}taken'.format(back_brackets)]

		# elif taskstep == 'GP_seat':
		# 	supp_acts += ['seat']
		# 	feats += ['seat_taken']

		# elif taskstep == 'A_seat' or taskstep == 'A_back':
		# 	supp_acts += random.choice([['hold'],[]]) #might want to skew this in favor of empty
		# 	if supp_acts == ['hold']: feats += ['hold_taken']

		# elif taskstep == 'GP_BL' or taskstep == 'GP_BR':
		# 	supp_acts += ['dowel']
		# 	if random.random() > .5 or top_brackets > 0 or timestep == 0:
		# 		supp_acts += ['top_bracket']
		# 		top_brackets += 1
		# 	random.shuffle(supp_acts)
		# 	dowels += 1
		# 	feats += ['dowel_{}taken'.format(dowels), 'topb_{}taken'.format(top_brackets)]

		# elif taskstep == 'GP_top':
		# 	while top_brackets < 2 :
		# 		supp_acts += ['top_bracket']
		# 		top_brackets += 1
		# 		feats += ['topb_{}taken'.format(top_brackets)]
		# 	supp_acts += ['long_dowel']
		# 	feats += ['longdowel_taken']
		# 	random.shuffle(supp_acts)


		# if timestep == 0:
		# 	supp_acts += ['screwdriver']
		# 	feats += ['screwdriver_taken']

	# 	supp_acts = tuple(supp_acts)
	# 	labels += [supp_acts]
	# 	feature_seq += [tuple(sorted(feats))]

	# return zip(feature_seq, labels)

# def default_supp_actions(num_users):
#     default_supp_actions = defaultdict(Counter)
#     for trainer in range(num_users):
#         t = chair_task_rand_state_seq()
#         trainer_pref = chair_task_sim_user_labels(t)
#         for timestep, (feats, supp_acts) in enumerate(trainer_pref):
#             default_supp_actions[(timestep,feats)][supp_acts] += 1
#     return default_supp_actions

# def uncertainty_score(user_pref_dict):
# 	uncertainty_dict = {}
# 	for k in user_pref_dict.keys():
# 		if user_pref_dict[k].most_common(1)[0][1] <= float(sum(user_pref_dict[k].values()))/2.0:
# 			uncertainty_dict[k] = True
# 		else:
# 			uncertainty_dict[k] = False
# 	return uncertainty_dict


class UserPrefModel(object):
	def __init__(self):
		self.model = defaultdict(Counter)

	def update(self, timestep_state_tup, supp_acts_tup):
		self.model[timestep_state_tup][supp_acts_tup] += 1

	def predict(self, timestep, state):
		try:
			return self.model[(timestep, state)].most_common(1)[0][0]
		except IndexError: #ONLY FOR DEBUGGING
			print('timestep', timestep, 'state', state)
			raw_input('Proceed (UserPrefModel.predict())')

	def should_query(self, timestep, state):
		check = None
		try:
			check = self.model[(timestep, state)].most_common(1)[0][1] <= float( sum(self.model[(timestep, state)].values()) ) / 2.0 #no majority vote
			# print('checking about query', check)
		except IndexError:
			check = True
		# except IndexError:
		# 	prettyprint(self.model)
		return check

	def prettyprint(self):
		prettyprint(self.model)

	def __repr__(self):
		return str(self.model)


def sim_trained_model(num_init_users):
	default_mod = UserPrefModel()
	for trainer in range(num_init_users):
		trainer_pref = chair_assembly_task.sim_user_labels()
		for timestep_state_tup, supp_acts_tup in trainer_pref:
			default_mod.update(timestep_state_tup, supp_acts_tup)
	return default_mod
