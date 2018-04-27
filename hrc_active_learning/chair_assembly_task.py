from htm import *

def chair_task_HTM():
    myHTM = HTM(PARALLEL)
    myHTM.add_children([ARROW, ARROW])
    myHTM.child(0).add_children([PARALLEL, 'GP_seat', 'A_seat'])
    myHTM.child(0).child(0).add_children(['GP_L1', 'GP_L2', 'GP_L3', 'GP_L4'])
    myHTM.child(1).add_children([PARALLEL, 'GP_top', 'A_back'])
    myHTM.child(1).child(0).add_children(['GP_BL', 'GP_BR'])
    return myHTM

def chair_task_rand_state_seq():
    htm = chair_task_HTM()
    traj = htm.gen_task_seq()
    return traj
    

def chair_task_features():
    return set(['screwdriver_taken', 'dowel_1taken', 'dowel_2taken', 'dowel_3taken', 'dowel_4taken', 'dowel_5taken', 'dowel_6taken', 'longdowel_taken', 'frontb_1taken', 'frontb_2taken', 'backb_1taken', 'backb_2taken', 'seat_taken', 'back_taken', 'topb_1taken', 'topb_2taken', 'hold_taken'])

def chair_task_sup_actions():
    return set(['dowel', 'long_dowel', 'screwdriver', 'top_bracket', 'back_bracket', 'front_bracket', 'hold', 'seat', 'back'])
