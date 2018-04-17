from utils import *
from part_one import *
from part_two import *
# import numpy as np

from collections import defaultdict
from collections import Counter



NUMBER_INIT_USERS_PART_TWO = 3
NUMBER_TRIALS_PART_THREE = 3

"""
Notes:
change htm to GP_TOP before GP_BL, BR before robot demo
take into account results of queries in part three more that default model?
add 'don't care out of these two options' as a way to answer a query

part 1 - Oi:htmleaf dict
part 2 - htmleaf:supportiveaction dict, htmleaf:query?TorF dict
main - part1 dict, part2 dict
        print default query dict
        worker bob: 3 runs, print query dict now
        worker carol: 3 runs, print query dict now
part 3 - takes a starting htmleaf:supportiveaction dict and a starting htmleaf:query?TorF dict and update and return both
"""

def user_name(num):
    return 'User ' + str(num)

def execute_part_one_sim(myHTM):
    S = get_leaves(myHTM) + ['UNKNOWN_STATE']
    O = example_obs()
    
    # assume found distinct mapping, anything out of the set Oi is an unknown human state
    disamb_obs = random.sample(list(powerset(O)), len(S))
    assumption1 = zip(S, disamb_obs) 

    ##REPLACE OBS WITH REAL OBS
    
    f_sim = {taskstep: list(obs) for (taskstep, obs) in assumption1}
    
    # because of assumption1, g_sim is just an inverse
    # TO BE CHANGED IN demo8
    g_sim = {Oi:taskstep for (taskstep, Oi) in assumption1}
    for Oi in list(powerset(O)):
        if Oi not in g_sim.keys():
            g_sim[Oi] = 'UNKNOWN_STATE'
    return f_sim, g_sim

def execute_part_two_sim(myHTM, f):
    A = example_sup_actions()
    possible_ai = list(powerset(A)) #list of lists


    init_labels = []
    # for i in range(NUMBER_INIT_USERS_PART_TWO):
    #   #list of tasksteps
    #   traj = 
    #   init_labels +=[((timestep, user_name(i)), random.choice(possible_ai) ) for timestep, Oi in enumerate(generate_valid_Oi_seq(myHTM, f)) ]
    #   # init_labels +=[(tuple(Oi), random.choice(possible_ai) ) for Oi in generate_valid_Oi_seq(myHTM, f)]
    # # print generate_valid_Oi_seq(myHTM, f)

    #hard-code supportive action labels to three previously randomly-generated trajectories, for demonstration purposes. 
    #assuming l1 and l2 are front legs, l3 and l4 are back legs
    #assume instead of supportive actions being a set, that it is a list - order matters and repeats of a certain supportive aciton can occue
    #might just want to make this part 1 training! might make sense

    #with holds
    train1 = zip(['GP_L2', 'GP_L3', 'GP_L4', 'GP_L1', 'GP_seat', 'A_seat', 'GP_BR', 'GP_BL', 'GP_top', 'A_back'],[('dowel', 'screwdriver', 'front_bracket'),('dowel', 'back_bracket'),('dowel', 'back_bracket'),('dowel', 'front_bracket'),('seat',),('hold',),('dowel',), ('dowel',), ('long_dowel', 'top_bracket','top_bracket', 'back'), ('hold',)])
    #without holds
    train2 = zip(['GP_BL', 'GP_BR', 'GP_top', 'A_back', 'GP_L2', 'GP_L3', 'GP_L4', 'GP_L1', 'GP_seat', 'A_seat'],[Counter(['dowel', 'screwdriver', 'top_bracket']), Counter(['dowel', 'top_bracket']), Counter(['long_dowel','back']), Counter([]), Counter(['dowel', 'front_bracket']), Counter(['dowel', 'back_bracket']), Counter(['dowel', 'back_bracket']), Counter(['dowel', 'front_bracket']), Counter(['seat']), Counter([])])

    #without holds
    train3 = zip(['GP_BR', 'GP_BL', 'GP_top', 'A_back', 'GP_L4', 'GP_L1', 'GP_L2', 'GP_L3', 'GP_seat', 'A_seat'],[Counter(['dowel','top_bracket','screwdriver']), Counter(['dowel','top_bracket']),Counter(['long_dowel','back']),Counter([]), Counter(['dowel','back_bracket']), Counter(['dowel','front_bracket']),Counter(['dowel','front_bracket']),Counter(['dowel','back_bracket']),Counter(['seat']), Counter([])])

    # prettyprint(train1)

    default_supp_actions = defaultdict(Counter)
    for (htmleaf, supp_acts) in train1:
        default_supp_actions[htmleaf][supp_acts] += 1
    prettyprint(default_supp_actions)

    # user_pref_dict = defaultdict(Counter)
    # for tup, ai in init_labels:
    #     user_pref_dict[tup][ai] += 1
    #     # user_pref_dict[(t,Oi)].update(ai)

    # Oi_to_query = uncertainty_score(user_pref_dict, float(NUMBER_INIT_USERS_PART_TWO)/ 2)
    # # Oi_to_query = uncertainty_score_2(user_pref_dict)
    # return possible_ai, user_pref_dict, Oi_to_query

def execute_part_three_sim(user_pref, query_vec, possible_ai):
    print user_pref
    for user in range(NUMBER_INIT_USERS_PART_TWO):
        for trial in range(NUMBER_TRIALS_PART_THREE):
            num_queries = 0
            for t in sorted(user_pref.keys()):
                print t
                if query_vec[t] == True:
                    num_queries += 1
                    #CALL PART FOUR SIM HERE instead
                    # #user_pref[t][random.choice(possible_ai)] += 1
            print 'Number of queries for ' + user_name(user) + ' - Trial ' + str(trial) + ': ' + str(num_queries)
            # print user_pref


def main():
    myHTM = example_HTM()
    # print generate_rand_state_seq(myHTM)
    # print generate_rand_state_seq(myHTM)
    # print generate_rand_state_seq(myHTM)
    # print generate_rand_state_seq(myHTM)
    f, g = execute_part_one_sim(myHTM)
    # print f
    execute_part_two_sim(myHTM, f)
    
    # possible_ai, user_pref_dict, query_vec = execute_part_two_sim(myHTM,f)
    # # print user_pref_dict
    
    # mymatrix = []
    # for t in sorted(user_pref_dict.keys()):
    #   mymatrix += [[str(t), str(query_vec[t]), str(user_pref_dict[t])]]
    # prettyprint(mymatrix)

    # execute_part_three_sim(user_pref_dict, query_vec, possible_ai)



if __name__ == "__main__": main()