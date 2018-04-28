from htm import *
import random


def task_HTM():
    myHTM = HTM(PARALLEL)
    myHTM.add_children([ARROW, ARROW])
    myHTM.child(0).add_children([PARALLEL, 'GP_seat', 'A_seat'])
    myHTM.child(0).child(0).add_children(['GP_L1', 'GP_L2', 'GP_L3', 'GP_L4'])
    myHTM.child(1).add_children([PARALLEL, 'GP_top', 'A_back'])
    myHTM.child(1).child(0).add_children(['GP_BL', 'GP_BR'])
    return myHTM

def task_len():
    return task_HTM().get_len()

def rand_taskstep_seq():
    htm = task_HTM()
    traj = htm.gen_task_seq()
    return traj   

def features():
    return set([['back_taken', 'backb_1taken', 'backb_2taken', 'dowel_1taken', 'dowel_2taken', 'dowel_3taken', 'dowel_4taken', 'dowel_5taken', 'dowel_6taken', 'frontb_1taken', 'frontb_2taken', 'hold_taken', 'longdowel_taken', 'screwdriver_taken', 'seat_taken', 'topb_1taken', 'topb_2taken']])

def supp_actions():
    return set(['dowel', 'long_dowel', 'screwdriver', 'top_bracket', 'back_bracket', 'front_bracket', 'hold', 'seat', 'back'])

def sim_user_labels(): #Clean up: change to return in form (timestep_feats_tuple, supp_acts_tuple), but in a nicer way. Can use Env class here
    traj = rand_taskstep_seq()
    labels = []
    feature_seq = [()]
    
    brackets_first = random.random() > .6 
    dowels = 0
    front_brackets =0
    back_brackets = 0
    top_brackets = 0

    for timestep, taskstep in enumerate(traj):
        
        supp_acts = []
        feats = []

        if taskstep == 'GP_L1' or taskstep == 'GP_L2':
            if brackets_first:
                supp_acts += ['front_bracket', 'dowel']
            else:
                supp_acts += ['dowel', 'front_bracket']
            front_brackets +=1
            dowels +=1
            feats += ['dowel_{}taken'.format(dowels),'frontb_{}taken'.format(front_brackets)]


        elif taskstep == 'GP_L3' or taskstep == 'GP_L4':
            if brackets_first:
                supp_acts += ['back_bracket', 'dowel']
            else:
                supp_acts += ['dowel', 'back_bracket']
            back_brackets += 1
            dowels += 1
            feats += ['dowel_{}taken'.format(dowels), 'backb_{}taken'.format(back_brackets)]
        
        elif taskstep == 'GP_seat':
            supp_acts += ['seat']
            feats += ['seat_taken']
        
        elif taskstep == 'A_seat' or taskstep == 'A_back':
            supp_acts += random.choice([['hold'],[]]) #might want to skew this in favor of empty
            if supp_acts == ['hold']: feats += ['hold_taken']
        
        elif taskstep == 'GP_BL' or taskstep == 'GP_BR':
            supp_acts += ['dowel']
            if random.random() > .5 or top_brackets > 0 or timestep == 0:
                supp_acts += ['top_bracket']
                top_brackets += 1
            random.shuffle(supp_acts)
            dowels += 1
            feats += ['dowel_{}taken'.format(dowels), 'topb_{}taken'.format(top_brackets)]
        
        elif taskstep == 'GP_top':
            while top_brackets < 2 :
                supp_acts += ['top_bracket']
                top_brackets += 1
                feats += ['topb_{}taken'.format(top_brackets)]
            supp_acts += ['long_dowel']
            feats += ['longdowel_taken']
            random.shuffle(supp_acts)
        

        if timestep == 0:
            supp_acts += ['screwdriver']
            feats += ['screwdriver_taken']

        supp_acts = tuple(supp_acts)
        labels += [supp_acts]
        feature_seq += [tuple(sorted(feats))]

    # return zip(feature_seq, labels)
    r = []
    for timestep, (feats, supp_acts) in enumerate(zip(feature_seq, labels)):
        r += [((timestep, feats), supp_acts)]
    return r
