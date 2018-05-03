#!/usr/bin/env python

import hrc_active_learning.model_framework as framework
from hrc_active_learning import chair_assembly_task
from hrc_active_learning.utils import *

from collections import deque

#TODO
#- model framework class, with __str__()
#- obj params
#- __init__ rather than _run?
#- improve readability
#- array O(1) for state_of_the_world check/update rather than list lookup, note has to be hashable type
#- change 'face' display
#- ask Corina about _stop() for last condition feedback -- left arm suction problem

class UserPrefDemoController(object):
    def __init__(self, **kwargs):
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
        self.current_model = None
        self.proactive_queries = 0
        self.incorrect_action_queries = 0
        self.timestep = 0
        self.state_of_the_world = chair_assembly_task.UserPrefDemoEnvState()
        self.current_action_plan = deque()
        self.task_len = chair_assembly_task.task_len()
        self.human_input = None

    def debug(self):
        self.current_model.prettyprint()
        # print('proactive_queries ', self.proactive_queries)
        # print('incorrect_action_queries ', self.incorrect_action_queries)
        print('timestep ', self.timestep)
        print('state_of_the_world ', self.state_of_the_world)
        print('current_action_plan ', self.current_action_plan)
        # print('task_len ', self.task_len)

    def _run(self):
        #initialize model with default by simulating training
        self.training()
        self.debug()
        raw_input("Proceed?")

        while ():
            # try:
            while self.timestep < self.task_len:

                if self.current_model.should_query(self.timestep, self.state_of_the_world):
                    self.current_action_plan = deque(self.query())
                    self.current_model.update((self.timestep, self.state_of_the_world), tuple(self.current_action_plan))
                    self.proactive_queries += 1
                    self.debug()
                else:
                    self.current_action_plan = deque(self.current_model.predict(self.timestep, self.state_of_the_world))
                    self.debug()
                # self.debug()
                raw_input('Proceed?')

                num_fails = 0
                next_action = None

                # To catch f no supportive actions required:
                try:
                    next_action = self.current_action_plan.popleft()
                    self.debug()
                except IndexError:
                    self.timestep += 1
                    self.debug()
                    continue

                starting_state = self.state_of_the_world
                actions_done = 0
                # Go through action plan queue
                while True:
                    if self.state_of_the_world.check_action(next_action):
                        feedback = self.robot_do(next_action)
                        actions_done +=1
                    else:
                        raise Exception('Invalid action request')
                    if feedback.success == True:
                        self.state_of_the_world.update(next_action)
                        # self.debug()
                        try:
                            next_action = self.current_action_plan.popleft()
                            # self.debug()
                        except IndexError:
                            break
                    elif feedback.response == feedback.ACT_KILLED:
                        print "Would have to do an incorrect_action_query"
                        new_action_plan = deque(self.query())
                        #This is wrong...should update the current entry
                        self.current_model.update((self.timestep, starting_state), tuple(self.current_action_plan[:actions_done] + new_action_plan))
                        self.debug()
                        self.current_action_plan += deque(list(self.current_action_plan)[:actions_done] + new_action_plan)
                        self.incorrect_action_queries += 1
                        self.debug()
                        try:
                            next_action = self.current_action_plan.popleft()
                        except IndexError:
                            break
                    elif feedback.response in (feedback.NO_IR_SENSOR, feedback.ACT_NOT_IMPL):
                        self._stop()
                        raise Exception('Robot Failure')
                    else:
                        print "Would have to retry"
                        num_fails += 1
                        if num_fails < 3:
                            pass
                        #If it fails 3 times, stopping the whole thing rather than going to next timestep. can change
                        else:
                            self._stop()
                            raise Exception('Robot failed 3 times to do supportive action, exiting')
                    # self.debug()

                # break #DEBUGGING
                self.timestep += 1
            print ('proactive_queries', proactive_queries, 'incorrect_action_queries', incorrect_action_queries)

            if raw_input('Again?') == 'y':
                self.proactive_queries = 0
                self.incorrect_action_queries = 0
                self.timestep = 0
                self.current_action_plan = deque()


    def training(self):
        self.current_model = framework.sim_trained_model(3)

    def query(self):
        # user_resp = ('hold',)
        self.human_input = None
        inp = raw_input("Robot: What can I do to help? (Enter comma-seperated)")
        user_resp = tuple([item.strip() for item in inp.strip().split(',')])
        # print user_resp
        # print "What can I do to help? Select and press 'next.'"
        # while self.human_input != 'next':
        #     rospy.Subscriber(self.WEB_INTERFACE, String, self.web_interface_callback)
        #     # print("got human_input ", self.human_input)
        #     if(self.human_input != None and self.human_input not in actions_requested):
        #         actions_requested += [self.human_input]
        #     rospy.rostime.wallsleep(0.5)
        # user_resp = tuple(actions_requested)
        print user_resp

        return user_resp

    def robot_do(self, spec):
        if raw_input(spec + "?") == 'y':
            return 'success'
        else:
            print "incorrect"
            return 'wrong'




def main():
    controller = UserPrefDemoController()
    controller._run()

if __name__ == '__main__': main()
