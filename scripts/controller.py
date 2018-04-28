#!/usr/bin/env python

import rospy
from rospy import init_node, is_shutdown

#from std_msgs.msg import String

from human_robot_collaboration.controller import BaseController
import hrc_active_learning.model_framework as framework
from hrc_active_learning.utils import *

#TODO
#- model framework class, with __str__()
#- obj params
#- __init__ rather than _run?
#- improve readability
#- array O(1) for state_of_the_world check/update rather than list lookup, note has to be hashable type
#- change 'face' display
#- ask Corina about _stop() for last condition feedback -- left arm suction problem


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
        self.current_model = framework.default_supp_actions(num_users=3)

    def _run(self):
        prettyprint(current_model)
        while not is_shutdown():
            rospy.signal_shutdown("End of task.")


        
def main():
    controller = UserPrefDemoController()
    controller.time_step = 0
    controller.run()

if __name__ == '__main__': main()