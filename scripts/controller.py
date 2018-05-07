#!/usr/bin/env python
import os
import argparse
import sys

import rospy
from rospy import init_node, is_shutdown

from std_msgs.msg import String

from human_robot_collaboration.controller import BaseController
import hrc_active_learning.model_framework as framework
from hrc_active_learning import chair_assembly_task
from hrc_active_learning.utils import *

from collections import deque

#TODO
#- model framework class, with __str__() --done
#- obj params
#- __init__ rather than _run? for vars --done
#- improve readability --done
#- array O(1) for state_of_the_world check/update rather than list lookup, note has to be hashable type
#- change 'face' display
#- ask Corina about _stop() for last condition feedback -- left arm suction problem

class UserPrefDemoController(BaseController):
    WEB_INTERFACE = '/hrc_active_learning/web_interface/pressed'
    def __init__(self, **kwargs):
        super(UserPrefDemoController, self).__init__(
            left=True,
            right=True,
            speech=False,
            listen=True,
            recovery=True,
            timer_path='timer.json', **kwargs)
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
        print('proactive_queries ', self.proactive_queries)
        print('incorrect_action_queries ', self.incorrect_action_queries)
        print('timestep ', self.timestep)
        print('state_of_the_world ', self.state_of_the_world)
        print('current_action_plan ', self.current_action_plan)
        print('task_len ', self.task_len)

    def _run(self):
        # TO GENERATE SIMULATED USER PREFERENCES FOR REFERENCE (USERFUL FOR DEBUGGING)
        # while not is_shutdown():
        #     print self.query()
        #     rospy.signal_shutdown("End of task.")
        # framework.sim_trained_model(1).prettyprint()
        # framework.sim_trained_model(1).prettyprint()
        # framework.sim_trained_model(1).prettyprint()
        # raw_input('Proceed?')

        self.training()
        self.debug()
        raw_input('Proceed?')

        while not is_shutdown():
            interaction_count = 0
            while self.timestep < self.task_len:

                if self.current_model.should_query(self.timestep, self.state_of_the_world.to_tuple()):
                    self.current_action_plan = deque(self.query())
                    self.proactive_queries += 1
                    self.debug()
                else:
                    self.current_action_plan = deque(self.current_model.predict(self.timestep, self.state_of_the_world.to_tuple()))
                    self.debug()

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

                starting_state = self.state_of_the_world.to_tuple()
                succ_actions_done = []
                # Go through action plan queue
                while True:
                    if self.state_of_the_world.check_action(next_action):
                        feedback = self.robot_do(next_action)

                    else:
                        self.current_action_plan = deque(self.query())
                        self.incorrect_action_queries += 1
                        try:
                            next_action = self.current_action_plan.popleft()
                            continue
                        except IndexError:
                            break
                    if feedback.success == True:
                        self.state_of_the_world.update(next_action)
                        succ_actions_done += [next_action]
                        try:
                            next_action = self.current_action_plan.popleft()
                        except IndexError:
                            break
                    elif feedback.response == feedback.ACT_KILLED:
                        print "Would have to do an incorrect_action_query"
                        self.current_action_plan = deque(self.query())
                        self.incorrect_action_queries += 1
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
                        if num_fails < 10:
                            pass
                        else:
                            self._stop()
                            raise Exception('Robot failed 10 times to do supportive action, exiting')

                self.timestep += 1
                self.current_model.update((self.timestep - 1, starting_state), tuple(succ_actions_done))
            print ('interaction_count', interaction_count)
            print ('proactive_queries', self.proactive_queries, 'incorrect_action_queries', self.incorrect_action_queries)

            if raw_input('Again?')[0]== 'y':
                interaction_count += 1
                self.proactive_queries = 0
                self.incorrect_action_queries = 0
                self.timestep = 0
                self.current_action_plan = deque()
                self.state_of_the_world = chair_assembly_task.UserPrefDemoEnvState()
            else:
                rospy.signal_shutdown("End of task.")

    def training(self):
        self.current_model = framework.sim_trained_model(3)

    def web_interface_callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s ", data.data)
        self.human_input = data.data

    def query(self):
        self.human_input = None
        actions_requested = []

        print "What can I do to help? Select and press 'next.'"
        while self.human_input != 'next':
            rospy.Subscriber(self.WEB_INTERFACE, String, self.web_interface_callback)
            if(self.human_input != None and self.human_input not in actions_requested):
                actions_requested += [self.human_input]
            rospy.rostime.wallsleep(0.5)
        user_resp = tuple(actions_requested)
        print user_resp

        return user_resp

    #This code could be rewritten more elegantly
    def robot_do(self, spec): 
        index = None
        if spec == 'dowel':
            if self.state_of_the_world.dowel_count == 0:
                index = 0
            else:
                index = self.state_of_the_world.dowel_count #count is 1-indexed, index is 0-indexed
            side, obj_num = self.object_info[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        elif spec == 'long_dowel':
            index = 0
            side, obj_num = self.object_info[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        elif spec == 'screwdriver':
            index = 0
            side, obj_num = self.object_info[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        elif spec == 'top_bracket':
            if self.state_of_the_world.topb_count == 0:
                index = 0
            else:
                index = self.state_of_the_world.topb_count
            side, obj_num = self.object_info[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        elif spec == 'back_bracket':
            if self.state_of_the_world.backb_count == 0:
                index =0
            else:
                index = self.state_of_the_world.backb_count
            side, obj_num = self.object_info[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        elif spec == 'front_bracket':
            if self.state_of_the_world.frontb_count == 0:
                index =0
            else:
                index = self.state_of_the_world.frontb_count
            side, obj_num = self.object_info[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        elif spec == 'hold':
            r = self._action(BaseController.RIGHT, ('hold_top', []), {'wait': True})
        elif spec == 'seat':
            index =0
            side, obj_num = self.object_info[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        elif spec == 'back':
            index =0
            side, obj_num = self.object_info[spec][index]
            r = self._action(side, ('get_pass', [obj_num]), {'wait': True})
        else:
            raise Exception('Invalid action specified in robot_do()')
        return r



def main():
    controller = UserPrefDemoController()
    controller.time_step = 0
    controller._run()

if __name__ == '__main__': main()
