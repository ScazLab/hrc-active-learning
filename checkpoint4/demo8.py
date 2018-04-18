from utils import *
from part_one import *
from part_two import *
# import numpy as np

from collections import defaultdict
from collections import Counter
from copy import deepcopy



NUMBER_INIT_USERS_PART_TWO = 1
NUMBER_TRIALS_PART_THREE = 3

"""
Notes:
change htm to GP_TOP before GP_BL, BR before robot demo
take into account results of queries in part three more that default model?
add 'don't care out of these two options' as a way to answer a query
add 'was this order ok'  check for when labels aren't hardcoded. if 'no' update order directly or add this order tuple with vote=majority
ideally would be able to interrupt a robot if supportive action wrong

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
    S = get_leaves(myHTM) 
    O = example_obs()
    
    # assume found distinct mapping, anything out of the set Oi is an unknown human state
    disamb_obs = random.sample(list(powerset(O)), len(S))
    assumption1 = zip(S, disamb_obs) 
    
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


    # #with holds
    # train1 = zip(['GP_L2', 'GP_L3', 'GP_L4', 'GP_L1', 'GP_seat', 'A_seat', 'GP_BR', 'GP_BL', 'GP_top', 'A_back'],[('dowel', 'screwdriver', 'front_bracket'),('dowel', 'back_bracket'),('dowel', 'back_bracket'),('dowel', 'front_bracket'),('seat',),('hold',),('dowel',), ('dowel',), ('long_dowel', 'top_bracket','top_bracket', 'back'), ('hold',)])
    # #without holds
    # train2 = zip(['GP_BL', 'GP_BR', 'GP_top', 'A_back', 'GP_L2', 'GP_L3', 'GP_L4', 'GP_L1', 'GP_seat', 'A_seat'],[('dowel', 'top_bracket', 'screwdriver'), ('dowel', 'top_bracket'), ('long_dowel','back'), (), ('dowel', 'front_bracket'), ('dowel', 'back_bracket'), ('dowel', 'back_bracket'), ('dowel', 'front_bracket'), ('seat',), ()])

    # #without holds
    # train3 = zip(['GP_BR', 'GP_BL', 'GP_top', 'A_back', 'GP_L4', 'GP_L1', 'GP_L2', 'GP_L3', 'GP_seat', 'A_seat'],[('dowel','top_bracket','screwdriver'), ('dowel','top_bracket'),('long_dowel','back'),(), ('dowel','back_bracket'), ('dowel','front_bracket'),('dowel','front_bracket'),('dowel','back_bracket'),('seat',), ()])
    t1 = generate_rand_state_seq(myHTM)
    # print t1
    train1 = zip(t1, generate_reasonable_train_labels(t1))
    t2 = generate_rand_state_seq(myHTM)
    train2 = zip(t2, generate_reasonable_train_labels(t2))
    t3 = generate_rand_state_seq(myHTM)
    train3 = zip(t3, generate_reasonable_train_labels(t3))
    # prettyprint(train1)

    default_supp_actions = defaultdict(Counter)
    for (htmleaf, supp_acts) in train1 + train2 + train3:
        default_supp_actions[htmleaf][supp_acts] += 1

    # tasksteps_to_query = uncertainty_score(default_supp_actions)
    return default_supp_actions

def execute_part_three_sim(new_traj, new_labels_seq, old_supp_acts_model, verbose_flag):
    tasksteps_to_query = uncertainty_score(old_supp_acts_model)
    new_supp_acts_model = old_supp_acts_model
    total_queries = 0
    incorrect_actions = 0
    for taskstep in new_traj:
        if verbose_flag: print "[Human worker task state: " + str(taskstep) + "]"
        if tasksteps_to_query[taskstep]:
            if verbose_flag: print "Robot:What can I do to help?" + " -> Human worker's answer: " + str(new_labels_seq[taskstep]) 
            if verbose_flag: print "[Robot provides supportive action: " + str(new_labels_seq[taskstep]) + "]"
            new_supp_acts_model[taskstep][new_labels_seq[taskstep]] += 1
            total_queries += 1

        else:
            if verbose_flag: print "[Robot provides supportive action: " + str(old_supp_acts_model[taskstep].most_common(1)[0][0]) + "]"
            if old_supp_acts_model[taskstep].most_common(1)[0][0] != new_labels_seq[taskstep]:
                if verbose_flag: print "[Human wanted " + str(new_labels_seq[taskstep]) + "]"
                if verbose_flag: print "Robot:Sorry for not acting as intended. Will try to keep this in mind for next time, but it may take a few times to get right."
                new_supp_acts_model[taskstep][new_labels_seq[taskstep]] += 1
                incorrect_actions += 1
            else:
                if verbose_flag: print "[Robot acted as intended.]"
    # print str(total_queries) + " total queries made."
    # print str(incorrect_actions) + " incorrect actions."
    if total_queries ==0 and incorrect_actions == 0:
        prettyprint(new_supp_acts_model)
    return new_supp_acts_model, total_queries, incorrect_actions

def run_sim(new_traj, new_labels_seq, def_supp_acts_model, verbose_flag):
    # prettyprint(def_supp_acts_model)
    supp_acts_model_to_update = deepcopy(def_supp_acts_model)
    completed_runs = 0
    # print "Run " + str(completed_runs + 1)
    # new_supp_acts_model = 
    supp_acts_model_to_update, total_queries, incorrect_actions = execute_part_three_sim(new_traj, new_labels_seq, supp_acts_model_to_update, verbose_flag)
    completed_runs += 1
    while completed_runs < 20 and (total_queries > 0 or incorrect_actions > 0 ):
        # print "Run " + str(completed_runs + 1)
        supp_acts_model_to_update, total_queries, incorrect_actions = execute_part_three_sim(new_traj, new_labels_seq, supp_acts_model_to_update, verbose_flag)
        completed_runs += 1
    return completed_runs



def main():
    myHTM = example_HTM()
    print "=== PART ONE ==="
    f, g = execute_part_one_sim(myHTM)
    print "Assumption:there is a one-to-one matching between sets of observations of the environment and the state of the task. "
    prettyprint(f)


    print "=== PART TWO ==="
    default_supp_actions = execute_part_two_sim(myHTM, f)
    print "Default Model: Results of 3 training interactions (interactions where a query for supportive action labels is raised for every state of the task)"
    prettyprint(default_supp_actions)
    print "Given this model, whether the robot will query the user at each task state:"
    print "Will query ('True') if did not have a majority among the supportive action labels given by the initial training interactions."
    prettyprint(uncertainty_score(default_supp_actions))

    print
    print "=== PART THREE ==="
    print "------Simulation 1------"
    print "Simulate one interaction with worker Alice"
    Alice_traj = ['GP_BR', 'GP_BL', 'GP_top', 'A_back', 'GP_L2', 'GP_L3', 'GP_L1', 'GP_L4', 'GP_seat', 'A_seat']
    Alice_truth_labels = [('dowel','top_bracket', 'screwdriver'), ('dowel', 'top_bracket'), ('long_dowel', 'back'), ('hold',),('dowel','front_bracket'), ('dowel','back_bracket'),('dowel', 'front_bracket'),('dowel','back_bracket'),('seat',),('hold',)]
    Alice_sim = dict(zip(Alice_traj,Alice_truth_labels))
    alice_runs = run_sim(Alice_traj, Alice_sim, default_supp_actions, True)
    print str(alice_runs) + " runs to convergence for Alice"
    # model_of_supp_actions_for_Alice = execute_part_three_sim(Alice_traj, Alice_sim, default_supp_actions, True)
    # print "Simulate 3 more interactions with worker Alice, where she follows the same trajectory (print suppressed)"
    # model_of_supp_actions_for_Alice, _, _  = execute_part_three_sim(Alice_traj, Alice_sim, model_of_supp_actions_for_Alice, False)
    # model_of_supp_actions_for_Alice _, _ = execute_part_three_sim(Alice_traj, Alice_sim, model_of_supp_actions_for_Alice, False)
    # model_of_supp_actions_for_Alice _, _ = execute_part_three_sim(Alice_traj, Alice_sim, model_of_supp_actions_for_Alice, False)
    prettyprint(default_supp_actions)
    print
    print "------Simulation 2------"
    print "Simulate (capped) four interactions with work Bob, whose task trajectories vary slightly (varied trajectory hardcoded)"
    Bob_traj = ['GP_BR', 'GP_BL', 'GP_top', 'A_back', 'GP_L2', 'GP_L3', 'GP_L1', 'GP_L4', 'GP_seat', 'A_seat']
    Bob_truth_labels_onMondays = [('dowel','top_bracket', 'screwdriver'), ('dowel', 'top_bracket'), ('long_dowel', 'back'), ('hold',),('dowel','front_bracket'), ('dowel','back_bracket'),('dowel', 'front_bracket'),('dowel','back_bracket'),('seat',),('hold',)]
    #same thing, but without holds
    Bob_truth_labels_onTuesdays = [('dowel','top_bracket', 'screwdriver'), ('dowel', 'top_bracket'), ('long_dowel', 'back'), (),('dowel','front_bracket'), ('dowel','back_bracket'),('dowel', 'front_bracket'),('dowel','back_bracket'),('seat',),()]
    Bob_sim_Mondays = dict(zip(Bob_traj,Bob_truth_labels_onMondays))
    Bob_sim_Tuesdays = dict(zip(Bob_traj,Bob_truth_labels_onTuesdays))
    # bob_runs = run_sim (Bob_traj, Bob_truth_labels_onMondays)
    model_of_supp_actions_for_Bob = deepcopy(default_supp_actions)
    print "Run 1"
    model_of_supp_actions_for_Bob, q, w = execute_part_three_sim(Bob_traj, Bob_sim_Mondays, model_of_supp_actions_for_Bob, True)
    print str(q) + " queries"
    print str(w) + " incorrect actions"
    print "Run 2"
    model_of_supp_actions_for_Bob, q, w= execute_part_three_sim(Bob_traj, Bob_sim_Tuesdays, model_of_supp_actions_for_Bob, True)
    print str(q) + " queries"
    print str(w) + " incorrect actions"
    print "Run 3"
    model_of_supp_actions_for_Bob,q, w = execute_part_three_sim(Bob_traj, Bob_sim_Mondays, model_of_supp_actions_for_Bob, True)
    print str(q) + " queries"
    print str(w) + " incorrect actions"
    print "Run 4"
    model_of_supp_actions_for_Bob,q, w = execute_part_three_sim(Bob_traj, Bob_sim_Mondays, model_of_supp_actions_for_Bob, True)
    print str(q) + " queries"
    print str(w) + " incorrect actions"
    # print "------Simulation 3-------"
    # print "Showing convergence with both generated (but constant over 10 interactions) state seq and generated labels"
    # gen_traj = generate_rand_state_seq(myHTM)
    # gen_sim_truth = dict(zip(gen_traj, generate_reasonable_train_labels(gen_traj)))
    # print "Generated truth labels for generated trajectory:"
    # prettyprint(gen_sim_truth)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, default_supp_actions, False)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, model_of_supp_actions_for_gen, False)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, model_of_supp_actions_for_gen, False)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, model_of_supp_actions_for_gen, False)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, model_of_supp_actions_for_gen, False)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, model_of_supp_actions_for_gen, False)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, model_of_supp_actions_for_gen, False)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, model_of_supp_actions_for_gen, False)
    # model_of_supp_actions_for_gen = execute_part_three_sim(gen_traj, gen_sim_truth, model_of_supp_actions_for_gen, False)
    print
    print "------Simulation 3------"
    print "Showing convergence with both generated (but constant over all interactions) state seq and generated labels"

    print "Default model, for reference:"
    prettyprint(default_supp_actions)
    print "Calculating completed_runs before zero queries and zero incorrect_actions"
    for i in range(10):
        t = generate_rand_state_seq(myHTM)
        l = dict(zip(t, generate_reasonable_train_labels(t)))
        print "---------Worker: " + str(i)
        if i == 9:
            print "Worker 9 ground-truth, for reference:"
            prettyprint(l)
        d = deepcopy(default_supp_actions)
        # prettyprint(d)
        runs = run_sim(t, l, d, False)
        print  str(runs) + " runs before success"
    # t0 = generate_rand_state_seq(myHTM)
    # l0 = dict(zip(t0, generate_reasonable_train_labels(t0)))
    # d0 = deepcopy(default_supp_actions)
    print
    
    # prettyprint(d0)
    # runs= run_sim(t0, l0, d0, False)
    # print "Worker: " + str(10) + "\t" + str(runs) + " runs before success"
    # print
    # print "Last worker's ground truth labels, for reference:"
    # prettyprint(l0)
    # print "Last worker's dict for supportive actions, after aggregating 'votes' towards their ground-truth labels"
    # prettyprint(m0)

    # generate_reasonable_train_labels(generate_rand_state_seq(myHTM))



if __name__ == "__main__": main()