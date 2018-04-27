#!/usr/bin/env python

import rospy
from human_robot_collaboration.controller import BaseController
# from hrc_active_learning.chair_assembly_task import *
import hrc_active_learning.model_framework as framework
from hrc_active_learning.utils import *

#TODO
#- model framework class, with __str__()
#- obj params
#- __init__ rather than _run?
#- improve readability
#- array O(1) for state_of_the_world check/update rather than list lookup, note has to be hashable type

class UserPrefDemoController(BaseController):
    # BRING = 'get_pass' #suction
    # CLEAR = 'cleanup'
    # HOLD_LEG = 'hold_leg' #higher 'hold'
    # HOLD_TOP = 'hold_top' #hold
    # HOLD = 'hold_leg'

    def __init__(self):
        super(SuppBhvsHMMController, self).__init__(
            left=True,
            right=True,
            speech=False,
            listen=True,
            recovery=True,
            timer_path='timer.json',
            **kwargs)
        self.object_info = {
            "seat":                [(BaseController.LEFT, 198)],
            "back":                [(BaseController.LEFT, 201)],
            "dowel":               [(BaseController.LEFT, 150),(BaseController.LEFT, 151),(BaseController.LEFT, 152),(BaseController.LEFT, 153), (BaseController.LEFT, 154),(BaseController.LEFT, 155)],
            "long_dowel":          [(BaseController.LEFT, 156)],
            "front_bracket":       [(BaseController.RIGHT, 14), (BaseController.RIGHT, 15)],
            "back_bracket":        [(BaseController.RIGHT, 18), (BaseController.RIGHT, 19)],
            "top_bracket":         [(BaseController.RIGHT, 16), (BaseController.RIGHT, 17)],
            "screwdriver":         [(BaseController.RIGHT, 20)]
        }

    def do_supp_action(spec, index=0):
        if spec == 'dowel':
            if index > 5:
                print "Error: the index for the next object to bring is too high"
                return -1
            side, obj_num = self.OBJECT_INFO[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        else:
            r = self._action(BaseController.RIGHT, ('hold_top', []), {'wait': True})
        return r

    def state_of_the_world(current=(), successful_action=None): #change
        new = list(current)
        for action in successful_actions:
            if action == 'dowel':
                for feat in current:
                    if feat[:5] == 'dowel':
                        new += ['dowel_' + str(feat[6] + 1) + 'taken']
            elif action == 'hold':
                new += ['hold_taken']
        return tuple(new)

    def _run(self):
        curr_model = framework.default_supp_actions(num_users=3)
        query_dict = framework.uncertainty_score(curr_model)

        sim_user_truth = framework.default_supp_actions(num_users=1)
        
        prettyprint(curr_model)
        print
        prettyprint(query_dict)
        print 
        prettyprint(sim_user_truth)

        proactive_queries = 0
        incorrect_action_queries = 0

        timestep = 0
        state_of_the_world = ()
        supp_acts = ()
        
        while not is_shutdown():
            try:
                #Possible Pro-active Query
                if query_dict[(timestep, state_of_the_world)]:
                    print "Robot: What can I do to help?"
                    print "<< (Sim user) : " + str(sim_user_truth[(timestep, state_of_the_world)])
                    curr_model[(timestep, state_of_the_world)][sim_user_truth[(timestep, state_of_the_world)]] += 1
                    proactive_queries += 1
                    feedback = do_supp_action(sim_user_truth[timestep, state_of_the_world])
                    last_actions_performed = sim_user_truth[timestep, state_of_the_world]
                #Pro-active Action
                else:
                    print "Pro-actively doing supportive action: " + str(curr_model[(timestep, state_of_the_world)].most_common(1)[0][0])
                    feedback = do_supp_action(curr_model[(timestep, state_of_the_world)].most_common(1)[0][0])
                    last_actions_performed = curr_model[(timestep, state_of_the_world)].most_common(1)[0][0]

            except KeyError:
                #When never seen this state in training, always query the user
                print "Robot:What can I do to help?"
                print "<< (Sim user) : " + str(sim_user_truth[(timestep, state_of_the_world)])
                curr_model[(timestep, state_of_the_world)][sim_user_truth[(timestep, state_of_the_world)]] += 1
                proactive_queries += 1

            if feedback.success:
                state_of_the_world = state_of_the_world(state_of_the_world, last_actions_performed)
                


            '''
            if should query given state_of_the_world:
                query
                supp_acts = user response
                proactive queries ++
            else:
                supp_acts = prediction

            while supp_acts is not empty:
                feedback = do next act ()
                if success:
                    update state of the world based on that one action
                        (sort before storing)
                    continue
                else:
                    query
                    supp_acts = supp_acts[:act_count] #keep whatever worked
                    supp_acts += user responses[act_count:] #add from this point on
                    incorrect acts ++
                

            wait for feedback
            if negative
                incorrect_action_query()
            else
                update state_of_the_world

            '''

def main():
    

    controller = UserPrefDemoController()
    controller.time_step = 0
    controller.run()

if __name__ == '__main__': main()
