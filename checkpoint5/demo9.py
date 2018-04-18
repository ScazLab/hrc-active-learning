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

def part_one():
	myHTM = chair_task_HTM()
	# print chair_task_features()
	t = generate_rand_state_seq(myHTM)
	print t
	prettyprint(generate_user(t))
	pass


def main():
	part_one()
	pass

if __name__ == "__main__": main()
