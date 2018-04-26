from utils import *
from htm import *
from part_one import *
from part_two import *

from collections import defaultdict
from collections import Counter
from copy import deepcopy


"""
Notes:
change htm to GP_TOP before GP_BL, BR before robot demo
take into account results of queries in part three more that default model?
add 'don't care out of these two options' as a way to answer a query
add 'was this order ok'  check for when labels aren't hardcoded. if 'no' update order directly or add this order tuple with vote=majority
ideally would be able to interrupt a robot if supportive action wrong
add more to htm data to develop heuristics for simulated feature-vector generation more readily
"""

NUM_INIT_TRAINERS = 3

"""
Part 1 (new)
Show how generate user ground truth labels to set of observations (things that have been done at end of previous time step)
"""
def part_one(myHTM):
    t = generate_rand_state_seq(myHTM)
    user_pref = generate_user(t) #list of tuples(size2) of tuples(?)
    return t, user_pref

"""
Part 2 
Initial Training Period
"""
def part_two(myHTM):
    default_supp_actions = defaultdict(Counter)
    for trainer in range(NUM_INIT_TRAINERS):
        t = generate_rand_state_seq(myHTM)
        trainer_pref = generate_user(t)
        for timestep, (feats, supp_acts) in enumerate(trainer_pref):
            default_supp_actions[(timestep,feats)][supp_acts] += 1
    return default_supp_actions

"""
Part Three
Query = 
Incorrect Action =

-don't add for successful supportive actions delivered - if there is a dramatic change to user prefs in the future, the system will be for ready to change
"""

def part_three(new_user_groundtruth, old_supp_acts_model, verbose=True):
    tasksteps_to_query = uncertainty_score(old_supp_acts_model)
    new_supp_acts_model = old_supp_acts_model
    total_queries = 0
    incorrect_actions = 0
    for timestep, feats in sorted(new_user_groundtruth.keys()):
        if verbose : print "[Observed Environment: " + str(feats) + "]"
        try:
            if tasksteps_to_query[(timestep,feats)]:
                if verbose: print "Robot:What can I do to help?" + " -> Human worker's answer: " + str(new_user_groundtruth[(timestep, feats)]) 
                if verbose: print "[Robot provides supportive action: " + str(new_user_groundtruth[(timestep, feats)]) + "]"
                new_supp_acts_model[(timestep, feats)][new_user_groundtruth[(timestep,feats)]] += 1
                total_queries += 1
            else:
                if verbose: print "[Robot provides supportive action: " + str(old_supp_acts_model[(timestep,feats)].most_common(1)[0][0]) + "]"
                if old_supp_acts_model[(timestep,feats)].most_common(1)[0][0] != new_user_groundtruth[(timestep,feats)]:
                    if verbose: print "[Human wanted " + str(new_user_groundtruth[(timestep,feats)]) + "]"
                    if verbose: print "Robot:Sorry for not acting as intended. Will try to keep this in mind for next time, but it may take a few times to get right. Providing actions specified."
                    new_supp_acts_model[(timestep, feats)][new_user_groundtruth[(timestep,feats)]] += 1
                    incorrect_actions += 1
                else:
                    if verbose: print "[Robot acted as intended.]"
        except KeyError:
            if verbose: print "Robot:What can I do to help?" + " -> Human worker's answer: " + str(new_user_groundtruth[(timestep, feats)]) 
            if verbose: print "[Robot provides supportive action: " + str(new_user_groundtruth[(timestep, feats)]) + "]"
            new_supp_acts_model[(timestep, feats)][new_user_groundtruth[(timestep,feats)]] += 1
            total_queries += 1

    print str(total_queries) + " total queries made."
    print str(incorrect_actions) + " incorrect actions."
    return new_supp_acts_model, total_queries, incorrect_actions


def run_sim(new_user_groundtruth, def_supp_acts_model, verbose = True):
    supp_acts_model_to_update = deepcopy(def_supp_acts_model)
    new_user_groundtruth = {(timestep, feats) : supp_acts for timestep, (feats, supp_acts) in enumerate(new_user_groundtruth)}
    completed_runs = 0
    print "Run " +  str(completed_runs + 1)
    supp_acts_model_to_update, total_queries, incorrect_actions = part_three(new_user_groundtruth, supp_acts_model_to_update, verbose)
    completed_runs += 1
    while completed_runs < 20 and (total_queries > 0 or incorrect_actions > 0 ):
        print "Run " + str(completed_runs + 1)
        supp_acts_model_to_update, total_queries, incorrect_actions = part_three(new_user_groundtruth, supp_acts_model_to_update, verbose)
        completed_runs += 1
    return completed_runs


def main():
    myHTM = chair_task_HTM()


    print "---Possible features:---"
    print chair_task_features()


    print "=== PART ONE ==="

    print "Demonstration of how user ground truth labels to feature vectors are generated:"
    t, sample_user_pref = part_one(myHTM)
    print "Sequence of task states, for reference:" + str(t)
    prettyprint(sample_user_pref)

    
    print "=== PART TWO ==="

    print "Result of training iterations"
    default_supp_actions = part_two(myHTM)
    prettyprint(default_supp_actions, labels = ['Features of env', 'Supportive actions to deliver'])
    print "Which will be queryed for the first run of ever new user?"
    prettyprint(uncertainty_score(default_supp_actions))


    print "=== PART THREE ==="

    print "------Simulation 1------"
    u0_traj, u0_pref = part_one(myHTM)
    print "User 1's task trajectory, for reference:"
    print u0_traj
    print "User 1's preferences, for reference:"
    prettyprint(u0_pref,labels = ['Features of env', 'Supportive actions to deliver'] )
    runs = run_sim(u0_pref, default_supp_actions, verbose=True)
    print str(runs) + " runs before success"

    print "------Simulation 2------"
    for i in range(10):
        ui_traj, ui_pref = part_one(myHTM)
        print "---------Worker: " + str(i)
        if i == 9:
            print "Worker 9 ground-truth, for reference:"
            prettyprint(ui_pref,labels = ['Features of env', 'Supportive actions to deliver'] )
            print "Default model, for reference:"
            prettyprint(default_supp_actions,labels = ['Features of env', 'Supportive actions to deliver'] )
        runs = run_sim(ui_pref, default_supp_actions, verbose=False)
        print str(runs) + " runs before success"





if __name__ == "__main__": main()
