#!/usr/bin/env python

import rospy
from rospy import init_node, is_shutdown

#from std_msgs.msg import String

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
# class UserPrefDemoEnvState(object):
#     def __init__(self):
#         self.back_taken = False
#         self.backb_count = 0
#         self.dowel_count = 0
#         self.frontb_count = 0
#         self.hold_taken = False
#         self.longdowel_taken = False
#         self.screwdriver_taken = False
#         self.seat_taken = False
#         self.topb_count = 0

#     def to_tuple(self):
#         r = []
#         if self.back_taken : r += ['back_taken']
#         if self.backb_count > 0: r += ['backb_' + str(self.backb_count) + 'taken']
#         if self.dowel_count > 0: r += ['dowel_' + str(self.dowel_count) + 'taken']
#         if self.frontb_count > 0: r += ['frontb_' + str(self.frontb_count) + 'taken']
#         if self.hold_taken: r+= ['hold_taken']
#         if self.longdowel_taken: r += ['longdowel_taken']
#         if self.screwdriver_taken: r += ['screwdriver_taken']
#         if self.seat_taken: r += ['seat_taken']
#         if self.topb_count > 0 : r += ['topb_' + str(self.topb_count) + 'taken']
#         return tuple(r)

#     def update(self, successful_action):
#         if successful_action == 'dowel':
#             self.dowel_count += 1
#         elif successful_action == 'long_dowel':
#             self.longdowel_taken = True
#         elif successful_action == 'screwdriver':
#             self.screwdriver_taken = True
#         elif successful_action == 'top_bracket':
#             self.topb_count += 1
#         elif successful_action == 'back_bracket':
#             self.backb_count += 1
#         elif successful_action == 'front_bracket':
#             self.frontb_count += 1
#         elif successful_action == 'hold':
#             self.hold_taken = True
#         elif successful_action == 'seat':
#             self.seat_taken = True
#         elif successful_action == 'back':
#             self.back_taken = True
#         else:
#             raise Exception('Error: invalid successful_action passed to UserPrefDemoEnvState.update')
#         if self.dowel_count > 6 or self.backb_count > 2 or self.topb_count > 2 or self.frontb_count > 2:
#             raise Exception('Error: Counts for environment objects too high')

#     def check_action(self, action):
#         check = False
#         if action == 'dowel':
#             check = (self.dowel_count + 1) <= 6
#         elif action == 'long_dowel':
#             check = not self.longdowel_taken
#         elif action == 'screwdriver':
#             check = not self.screwdriver_taken
#         elif action == 'top_bracket':
#             check = (self.topb_count + 1) <= 2
#         elif action == 'back_bracket':
#             check = (self.backb_count + 1) <= 2
#         elif action == 'front_bracket':
#             check = (self.frontb_count + 1) <= 2
#         elif action == 'hold':
#             check =  True #no limit
#         elif action == 'seat':
#             check = not self.seat_taken
#         elif action == 'back':
#             check = not self.back_taken
#         return check

#     def __repr__(self):
#         return str(self.to_tuple())

#     def __hash__(self):
#         return hash(self.to_tuple())

#     def __eq__(self, other):
#         return (self.to_tuple() == other)

class UserPrefDemoController(BaseController):
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

    def debug(self):
        self.current_model.prettyprint()
        # print('proactive_queries ', self.proactive_queries)
        # print('incorrect_action_queries ', self.incorrect_action_queries)
        print('timestep ', self.timestep)
        print('state_of_the_world ', self.state_of_the_world)
        print('current_action_plan ', self.current_action_plan)
        # print('task_len ', self.task_len)

    def _run(self):
        self.training()
        # print self.current_model.model[(0,())].most_common(1)[0][1]
        self.debug()
        raw_input('Proceed?')

        while not is_shutdown():
            # try:
                while self.timestep < 3: #self.task_len: #DEBUGGING

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
                            # self.current_model.update()
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

    def query(self):
        user_resp = ()
        inp = raw_input("Robot: What can I do to help? (Enter comma-seperated)")
        user_resp = tuple(inp.strip().split(','))
        print user_resp,
        #TODO: take user input and change to tuple form
        # user_resp = ('hold',) #dummy
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
