from utils import *
from htm import *
from part_one import *
from part_two import *

from collections import defaultdict
from collections import Counter
from copy import deepcopy
# import pprint


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
	# print default_supp_actions
	prettyprint(default_supp_actions, sort=True)





def main():
	myHTM = chair_task_HTM()
	print "---Possible features:---"
	print chair_task_features()
	print "=== PART ONE ==="
	print "Demonstration of how user ground truth labels to feature vectors are generated:"
	t, sample_user_pref = part_one(myHTM)
	print "Sequence of task states, for reference:" + str(t)
	# prettyprint(sample_user_pref)
	prettyprint(sample_user_pref, sort=True)
	print "=== PART TWO ==="
	print "Result of training iterations"
	part_two(myHTM)
	



if __name__ == "__main__": main()
