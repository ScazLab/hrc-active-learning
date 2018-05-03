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

class UserPrefDemoEnvState(object):
    def __init__(self):
        self.back_taken = False
        self.backb_count = 0
        self.dowel_count = 0
        self.frontb_count = 0
        self.hold_taken = False
        self.longdowel_taken = False
        self.screwdriver_taken = False
        self.seat_taken = False
        self.topb_count = 0

    def to_tuple(self):
        r = []
        if self.back_taken : r += ['back_taken']
        if self.backb_count > 0: r += ['backb_' + str(self.backb_count) + 'taken']
        if self.dowel_count > 0: r += ['dowel_' + str(self.dowel_count) + 'taken']
        if self.frontb_count > 0: r += ['frontb_' + str(self.frontb_count) + 'taken']
        if self.hold_taken: r+= ['hold_taken']
        if self.longdowel_taken: r += ['longdowel_taken']
        if self.screwdriver_taken: r += ['screwdriver_taken']
        if self.seat_taken: r += ['seat_taken']
        if self.topb_count > 0 : r += ['topb_' + str(self.topb_count) + 'taken']
        return tuple(r)

    def update(self, successful_action):
        if successful_action == 'dowel':
            self.dowel_count += 1
        elif successful_action == 'long_dowel':
            self.longdowel_taken = True
        elif successful_action == 'screwdriver':
            self.screwdriver_taken = True
        elif successful_action == 'top_bracket':
            self.topb_count += 1
        elif successful_action == 'back_bracket':
            self.backb_count += 1
        elif successful_action == 'front_bracket':
            self.frontb_count += 1
        elif successful_action == 'hold':
            self.hold_taken = True
        elif successful_action == 'seat':
            self.seat_taken = True
        elif successful_action == 'back':
            self.back_taken = True
        else:
            raise Exception('Error: invalid successful_action passed to UserPrefDemoEnvState.update')
        if self.dowel_count > 6 or self.backb_count > 2 or self.topb_count > 2 or self.frontb_count > 2:
            raise Exception('Error: Counts for environment objects too high')

    def check_action(self, action):
        check = False
        if action == 'dowel':
            check = (self.dowel_count + 1) <= 6
        elif action == 'long_dowel':
            check = not self.longdowel_taken
        elif action == 'screwdriver':
            check = not self.screwdriver_taken
        elif action == 'top_bracket':
            check = (self.topb_count + 1) <= 2
        elif action == 'back_bracket':
            check = (self.backb_count + 1) <= 2
        elif action == 'front_bracket':
            check = (self.frontb_count + 1) <= 2
        elif action == 'hold':
            check =  True #no limit
        elif action == 'seat':
            check = not self.seat_taken
        elif action == 'back':
            check = not self.back_taken
        return check

    def __repr__(self):
        return str(self.to_tuple())

    def __hash__(self):
        return hash(self.to_tuple())

    def __eq__(self, other):
        return (self.to_tuple() == other)

# def sim_user_labels(): #Clean up: change to return in form (timestep_feats_tuple, supp_acts_tuple), but in a nicer way. Can use Env class here
#     traj = rand_taskstep_seq()
#     labels = []
#     feature_seq = [()]

#     brackets_first = random.random() > .6
#     dowels = 0
#     front_brackets =0
#     back_brackets = 0
#     top_brackets = 0

#     feats = []

#     for timestep, taskstep in enumerate(traj):

#         supp_acts = []


#         if taskstep == 'GP_L1' or taskstep == 'GP_L2':
#             if brackets_first:
#                 supp_acts += ['front_bracket', 'dowel']
#             else:
#                 supp_acts += ['dowel', 'front_bracket']
#             front_brackets +=1
#             dowels +=1
#             feats += ['dowel_{}taken'.format(dowels),'frontb_{}taken'.format(front_brackets)]


#         elif taskstep == 'GP_L3' or taskstep == 'GP_L4':
#             if brackets_first:
#                 supp_acts += ['back_bracket', 'dowel']
#             else:
#                 supp_acts += ['dowel', 'back_bracket']
#             back_brackets += 1
#             dowels += 1
#             feats += ['dowel_{}taken'.format(dowels), 'backb_{}taken'.format(back_brackets)]

#         elif taskstep == 'GP_seat':
#             supp_acts += ['seat']
#             feats += ['seat_taken']

#         elif taskstep == 'A_seat' or taskstep == 'A_back':
#             supp_acts += random.choice([['hold'],[]]) #might want to skew this in favor of empty
#             if supp_acts == ['hold']: feats += ['hold_taken']

#         elif taskstep == 'GP_BL' or taskstep == 'GP_BR':
#             supp_acts += ['dowel']
#             if random.random() > .5 or top_brackets > 0 or timestep == 0:
#                 supp_acts += ['top_bracket']
#                 top_brackets += 1
#             random.shuffle(supp_acts)
#             dowels += 1
#             feats += ['dowel_{}taken'.format(dowels), 'topb_{}taken'.format(top_brackets)]

#         elif taskstep == 'GP_top':
#             while top_brackets < 2 :
#                 supp_acts += ['top_bracket']
#                 top_brackets += 1
#                 feats += ['topb_{}taken'.format(top_brackets)]
#             supp_acts += ['long_dowel']
#             feats += ['longdowel_taken']
#             random.shuffle(supp_acts)


#         if timestep == 0:
#             supp_acts += ['screwdriver']
#             feats += ['screwdriver_taken']

#         supp_acts = tuple(supp_acts)
#         labels += [supp_acts]
#         feature_seq += [tuple(sorted(feats))]

#     # return zip(feature_seq, labels)
#     r = []
#     for timestep, (feats, supp_acts) in enumerate(zip(feature_seq, labels)):
#         r += [((timestep, feats), supp_acts)]
#     return r

#could add checks for actions
def sim_user_labels(): #Clean up: change to return in form (timestep_feats_tuple, supp_acts_tuple), but in a nicer way. Can use Env class here
    traj = rand_taskstep_seq()
    labels = []
    timestep_feats_tuples = [(0,())]

    brackets_first = random.random() > .6
    sim_world_state = UserPrefDemoEnvState()

    for timestep, taskstep in enumerate(traj):

        supp_acts = []
        feats = []

        if taskstep == 'GP_L1' or taskstep == 'GP_L2':
            if brackets_first:
                supp_acts += ['front_bracket', 'dowel']
            else:
                supp_acts += ['dowel', 'front_bracket']
            sim_world_state.update('front_bracket')
            sim_world_state.update('dowel')
            # feats += ['dowel_{}taken'.format(dowels),'frontb_{}taken'.format(front_brackets)]

        elif taskstep == 'GP_L3' or taskstep == 'GP_L4':
            if brackets_first:
                supp_acts += ['back_bracket', 'dowel']
            else:
                supp_acts += ['dowel', 'back_bracket']
            sim_world_state.update('back_bracket')
            sim_world_state.update('dowel')
            # feats += ['dowel_{}taken'.format(dowels), 'backb_{}taken'.format(back_brackets)]

        elif taskstep == 'GP_seat':
            supp_acts += ['seat']
            sim_world_state.update('seat')
            # feats += ['seat_taken']

        elif taskstep == 'A_seat' or taskstep == 'A_back':
            supp_acts += random.choice([['hold'],[]]) #might want to skew this in favor of empty
            if supp_acts == ['hold']:
                sim_world_state.update('hold')
                # feats += ['hold_taken']

        elif taskstep == 'GP_BL' or taskstep == 'GP_BR':
            supp_acts += ['dowel']
            if random.random() > .5 or sim_world_state.topb_count > 0 or timestep == 0:
                supp_acts += ['top_bracket']
                sim_world_state.update('top_bracket')
                # top_brackets += 1
            random.shuffle(supp_acts)
            sim_world_state.update('dowel')
            # dowels += 1
            # feats += ['dowel_{}taken'.format(dowels), 'topb_{}taken'.format(top_brackets)]

        elif taskstep == 'GP_top':
            while sim_world_state.topb_count < 2 :
                supp_acts += ['top_bracket']
                sim_world_state.update('top_bracket')
                # top_brackets += 1
                # feats += ['topb_{}taken'.format(top_brackets)]
            supp_acts += ['long_dowel']
            supp_acts += ['back']
            sim_world_state.update('long_dowel')
            sim_world_state.update('back')
            # feats += ['longdowel_taken']
            random.shuffle(supp_acts)


        if timestep == 0:
            supp_acts += ['screwdriver']
            sim_world_state.update('screwdriver')
            # feats += ['screwdriver_taken']

        supp_acts = tuple(supp_acts)
        labels += [supp_acts]
        timestep_feats_tuples += [(timestep + 1, sim_world_state.to_tuple())]

    return zip(timestep_feats_tuples, labels)
    # r = []
    # for timestep, (feats, supp_acts) in enumerate(zip(feature_seq, labels)):
    #     r += [((timestep, feats), supp_acts)]
    # return r

