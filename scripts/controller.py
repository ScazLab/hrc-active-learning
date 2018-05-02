#!/usr/bin/env python
import os
import argparse
import sys
import distutils.dir_util
from threading import Lock

import numpy as np
import random
from sklearn.externals import joblib
import rospy
from rospy import init_node, is_shutdown
from std_msgs.msg import String
from std_srvs.srv import Empty
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg

from human_robot_collaboration.controller import BaseController
from svox_tts.srv import Speech, SpeechRequest
from hrc_pred_supp_bhv.service_request import ServiceRequest, finished_request
from hrc_pred_supp_bhv.task_def import *
from hrc_pred_supp_bhv.srv import *
from hrc_pred_supp_bhv.bern_hmm.bernoulli_hmm import *




import rospy
from rospy import init_node, is_shutdown

from std_msgs.msg import String

from human_robot_collaboration.controller import BaseController
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
        # print('proactive_queries ', self.proactive_queries)
        # print('incorrect_action_queries ', self.incorrect_action_queries)
        print('timestep ', self.timestep)
        print('state_of_the_world ', self.state_of_the_world)
        print('current_action_plan ', self.current_action_plan)
        # print('task_len ', self.task_len)

    def _run(self):
        # while not is_shutdown():
        #     print self.query()
        #     rospy.signal_shutdown("End of task.")
        self.training()
        # print self.current_model.model[(0,())].most_common(1)[0][1]
        self.debug()
        raw_input('Proceed?')

        while not is_shutdown():
            # try:
                while self.timestep < 2:#self.task_len:

                    if self.current_model.should_query(self.timestep, self.state_of_the_world):
                        self.current_action_plan = deque(self.query())
                        self.current_model.update((self.timestep, self.state_of_the_world), tuple(self.current_action_plan))
                        self.proactive_queries += 1
                        self.debug()
                    else:
                        self.current_action_plan = deque(self.current_model.predict(self.timestep, self.state_of_the_world))
                        self.debug()
                    # self.debug()
                    # raw_input('Proceed?')

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

                    # Go through action plan queue
                    while True:
                        if self.state_of_the_world.check_action(next_action):
                            feedback = self.robot_do(next_action)
                        else:
                            raise Exception('Invalid action request')
                        if feedback.success == True:
                            self.state_of_the_world.update(next_action)
                            self.debug()
                            try:
                                next_action = self.current_action_plan.popleft()
                                self.debug()
                            except IndexError:
                                break
                        elif feedback.response == feedback.ACT_KILLED:
                            print "Would have to do an incorrect_action_query"
                            self.current_action_plan = deque(self.query())
                            self.current_model.update((self.timestep, self.state_of_the_world), tuple(self.current_action_plan))
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
                            if num_fails < 3:
                                pass
                            #If it fails 3 times, stopping the whole thing rather than going to next timestep. can change
                            else:
                                self._stop()
                                raise Exception('Robot failed 3 times to do supportive action, exiting')
                        # self.debug()

                    # break #DEBUGGING
                    self.timestep += 1

                rospy.signal_shutdown("End of task.")
                # break #remove on robot
            # except Exception as e:
            #     print e
            #     self._stop()


    def training(self):
        self.current_model = framework.sim_trained_model(3)

    def web_interface_callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s ", data.data)
        self.human_input = data.data

    def query(self):
        user_resp = ('hold',)
        self.human_input = None
        actions_requested = []
        inp = raw_input("Robot: What can I do to help? (Enter comma-seperated)")
        user_resp = tuple([item.strip() for item in inp.strip().split(',')])
        print user_resp
        # while self.human_input != 'next':
        #     rospy.Subscriber(self.WEB_INTERFACE, String, self.web_interface_callback)
        #     # print("got human_input ", self.human_input)
        #     rospy.rostime.wallsleep(0.5)

        return user_resp

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
    # framework.sim_trained_model(1).prettyprint()
    controller = UserPrefDemoController()
    controller.time_step = 0
    controller._run()

if __name__ == '__main__': main()
