
from utils import *
from part_one import *
from part_two import *



# import random
from collections import defaultdict
from collections import Counter


def main():
	myHTM = example_HTM()

	"""--------PART ONE - assumed to be completed--------"""
	
	S = get_leaves(myHTM) + ['UNKNOWN_STATE']
	O = example_obs()
	
	# assume found distinct mapping, anything out of the set Oi is an unknown human state
	disamb_obs = random.sample(list(powerset(O)), len(S))
	assumption1 = zip(S, disamb_obs) 
	# print assumption1
	
	f_sim = {taskstep: list(obs) for (taskstep, obs) in assumption1}
	
	# because of assumption1, g_sim is just an inverse
	g_sim = {Oi:taskstep for (taskstep, Oi) in assumption1}
	for Oi in list(powerset(O)):
		if Oi not in g_sim.keys():
			g_sim[Oi] = 'UNKNOWN_STATE'

	# print g_sim


	"""--------PART TWO----------------------------------"""
	# what was discussed with Corina
	A = example_sup_actions()
	possible_ai = list(powerset(A))

	pref_user1 = [(tuple(Oi), random.choice(possible_ai) ) for Oi in generate_valid_Oi_seq(myHTM, f_sim) ]
	pref_user2 = [(tuple(Oi), random.choice(possible_ai)) for Oi in generate_valid_Oi_seq(myHTM, f_sim) ]
	pref_user3 = [(tuple(Oi), random.choice(possible_ai)) for Oi in generate_valid_Oi_seq(myHTM, f_sim) ]
	print pref_user1
	user_pref_dict = defaultdict(Counter)
	for Oi, ai in pref_user1 + pref_user2 + pref_user3:
		user_pref_dict[Oi].update((ai))
	print user_pref_dict
	# Oi_to_query = [flag for flag in uncertainty_scores([pref_user1, pref_user2, pref_user3])]



	"""--------PART THREE--------------------------------"""
	# if time permits, adding complexity.


if __name__ == "__main__": main()