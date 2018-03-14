
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

	num_users = 3.0
	pref_user1 = [(tuple(Oi), random.choice(possible_ai) ) for Oi in generate_valid_Oi_seq(myHTM, f_sim) ]
	pref_user2 = [(tuple(Oi), random.choice(possible_ai)) for Oi in generate_valid_Oi_seq(myHTM, f_sim) ]
	pref_user3 = [(tuple(Oi), random.choice(possible_ai)) for Oi in generate_valid_Oi_seq(myHTM, f_sim) ]
	# print pref_user1
	user_pref_dict = defaultdict(Counter)
	for Oi, ai in pref_user1 + pref_user2 + pref_user3:
		user_pref_dict[Oi][ai] += 1
	# print user_pref_dict
	# print num_users / 2
	Oi_to_query = uncertainty_score(user_pref_dict, num_users / 2)
	# print Oi_to_query

	"""------Command-line sim---------------------------"""
	print "Assumption 1:"
	print assumption1
	print "Preferences of Users 1, 2, and 3 -> whether to query:"
	user1_dict = dict(pref_user1)
	user2_dict = dict(pref_user2)
	user3_dict = dict(pref_user3)
	for Oi in user_pref_dict.keys():
		print str(Oi) + '\t' + str(user1_dict.get(Oi)) + '\t'+ str(user2_dict.get(Oi)) + '\t'+ str(user3_dict.get(Oi)) + '\t' + '->' + str(Oi_to_query.get(Oi))



	"""--------PART THREE--------------------------------"""
	# if time permits, adding complexity.


if __name__ == "__main__": main()