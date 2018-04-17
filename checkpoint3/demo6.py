from utils import *
from part_one import *
from part_two import *

from collections import defaultdict
from collections import Counter


NUMBER_INIT_USERS_PART_TWO = 3
NUMBER_TRIALS_PART_THREE = 3

def user_name(num):
	return 'User ' + str(num)

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
		init_labels +=[((timestep, user_name(i)), random.choice(possible_ai) ) for timestep, Oi in enumerate(generate_valid_Oi_seq(myHTM, f)) ]
		# init_labels +=[(tuple(Oi), random.choice(possible_ai) ) for Oi in generate_valid_Oi_seq(myHTM, f)]
	# print generate_valid_Oi_seq(myHTM, f)


	user_pref_dict = defaultdict(Counter)
	for tup, ai in init_labels:
		user_pref_dict[tup][ai] += 1
		# user_pref_dict[(t,Oi)].update(ai)

	Oi_to_query = uncertainty_score(user_pref_dict, float(NUMBER_INIT_USERS_PART_TWO)/ 2)
	# Oi_to_query = uncertainty_score_2(user_pref_dict)
	return possible_ai, user_pref_dict, Oi_to_query

def execute_part_three_sim(user_pref, query_vec, possible_ai):
	print user_pref
	for user in range(NUMBER_INIT_USERS_PART_TWO):
		for trial in range(NUMBER_TRIALS_PART_THREE):
			num_queries = 0
			for t in sorted(user_pref.keys()):
				print t
				if query_vec[t] == True:
					num_queries += 1
					user_pref[t][random.choice(possible_ai)] += 1
			print 'Number of queries for ' + user_name(user) + ' - Trial ' + str(trial) + ': ' + str(num_queries)
			# print user_pref



def main():
	myHTM = example_HTM()
	# print generate_rand_state_seq(myHTM)
	
	f, g = execute_part_one_sim(myHTM)
	
	possible_ai, user_pref_dict, query_vec = execute_part_two_sim(myHTM,f)
	# print user_pref_dict
	
	mymatrix = []
	for t in sorted(user_pref_dict.keys()):
		mymatrix += [[str(t), str(query_vec[t]), str(user_pref_dict[t])]]
	prettyprint(mymatrix)

	execute_part_three_sim(user_pref_dict, query_vec, possible_ai)



if __name__ == "__main__": main()