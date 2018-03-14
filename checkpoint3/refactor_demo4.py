from utils import *
from part_one import *
from part_two import *

from collections import defaultdict
from collections import Counter

NUMBER_INIT_USERS_PART_TWO = 3.0

def execute_part_one_sim(myHTM):
	S = get_leaves(myHTM) + ['UNKNOWN_STATE']
	O = example_obs()
	
	# assume found distinct mapping, anything out of the set Oi is an unknown human state
	disamb_obs = random.sample(list(powerset(O)), len(S))
	assumption1 = zip(S, disamb_obs) 
	
	f_sim = {taskstep: list(obs) for (taskstep, obs) in assumption1}
	
	# because of assumption1, g_sim is just an inverse
	g_sim = {Oi:taskstep for (taskstep, Oi) in assumption1}
	for Oi in list(powerset(O)):
		if Oi not in g_sim.keys():
			g_sim[Oi] = 'UNKNOWN_STATE'
	return f_sim, g_sim

def execute_part_two_sim(myHTM, f):
	A = example_sup_actions()
	possible_ai = list(powerset(A))

	init_labels = []
	for i in range(NUMBER_INIT_USERS_PART_TWO):
		init_labels +=[(tuple(Oi), random.choice(possible_ai) ) for Oi in generate_valid_Oi_seq(myHTM, f) ]

	user_pref_dict = defaultdict(Counter)
	for Oi, ai in init_labels:
		user_pref_dict[Oi][ai] += 1

	Oi_to_query = uncertainty_score(user_pref_dict, NUMBER_USERS_PART_TWO / 2)
	return user_pref_dict, Oi_to_query

def execute_part_three_sim(user_pref, query_vec):


def main():
	myHTM = example_HTM()
	f, g = execute_part_one_sim(myHTM)
	user_pref_dict, query_vec = execute_part_two_sim(myHTM,f)
	for Oi in user_pref_dict.keys():
		print str(g[Oi]) + '\t' + user_pref_dict[Oi]
	execute_part_three_sim(user_pref_dict, query_vec)



if __name__ == "__main__": main()