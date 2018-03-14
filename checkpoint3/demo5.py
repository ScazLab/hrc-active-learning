from utils import *
from part_one import *
from part_two import *

from collections import defaultdict
from collections import Counter


NUMBER_INIT_USERS_PART_TWO = 3

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
		init_labels +=[((timestep,tuple(Oi)), random.choice(possible_ai) ) for timestep, Oi in enumerate(generate_valid_Oi_seq(myHTM, f)) ]
		# init_labels +=[(tuple(Oi), random.choice(possible_ai) ) for Oi in generate_valid_Oi_seq(myHTM, f)]
	# print generate_valid_Oi_seq(myHTM, f)


	user_pref_dict = defaultdict(Counter)
	for (t, Oi), ai in init_labels:
		user_pref_dict[(t,Oi)][ai] += 1
		# user_pref_dict[(t,Oi)].update(ai)

	Oi_to_query = uncertainty_score(user_pref_dict, float(NUMBER_INIT_USERS_PART_TWO)/ 2)
	# Oi_to_query = uncertainty_score_2(user_pref_dict)
	return user_pref_dict, Oi_to_query

def execute_part_three_sim(user_pref, query_vec):
	return

def main():
	myHTM = example_HTM()
	# print generate_rand_state_seq(myHTM)
	
	f, g = execute_part_one_sim(myHTM)
	
	user_pref_dict, query_vec = execute_part_two_sim(myHTM,f)
	
	mymatrix = []
	for t,Oi in sorted(user_pref_dict.keys(), key=lambda x: x[0]):
		mymatrix += [[str(t), str(g[Oi]), str(query_vec[(t,Oi)]), str(user_pref_dict[(t, Oi)])]]
	prettyprint(mymatrix)

	execute_part_three_sim(user_pref_dict, query_vec)



if __name__ == "__main__": main()