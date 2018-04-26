import rospy
# from human_robot_collaboration.controller import BaseController
# from hrc_active_learning.chair_assembly_task import *
# from hrc_active_learning.user_pref import *
import hrc_active_learning

"""
Simulation for Initial Training Period
output: default_supp_actions dict, of form {(timestep, (?-tuple of feats)): Counter {(?-tuple of supportive actions): vote count, 
                                                                                    (?-tuple of different supportive acts): vote count, ...} ,
                                            ... }
"""
NUM_INIT_TRAINERS = 3
def default_supp_actions(myHTM):
    default_supp_actions = defaultdict(Counter)
    for trainer in range(NUM_INIT_TRAINERS):
        t = generate_rand_state_seq(myHTM)
        trainer_pref = generate_user(t)
        for timestep, (feats, supp_acts) in enumerate(trainer_pref):
            default_supp_actions[(timestep,feats)][supp_acts] += 1
    return default_supp_actions


class UserPrefDemoController(BaseController):
    OBJECT_IDX = {
        "seat_1":                [(BaseController.LEFT, 198),0],
        "back_1":                [(BaseController.LEFT, 201),0],
        "dowel_1":               [(BaseController.LEFT, 150),0],
        "dowel_2":               [(BaseController.LEFT, 151),0],
        "dowel_3":               [(BaseController.LEFT, 152),0],
        "dowel_4":               [(BaseController.LEFT, 153),0],
        "dowel_5":               [(BaseController.LEFT, 154),0],
        "dowel_6":               [(BaseController.LEFT, 155),0],
        "long_dowel_1":          [(BaseController.LEFT, 156),0],
        "front_bracket_1":       [(BaseController.RIGHT, 14),0],
        "front_bracket_2":       [(BaseController.RIGHT, 15),0],
        "back_bracket_1":        [(BaseController.RIGHT, 18),0],
        "back_bracket_2":        [(BaseController.RIGHT, 19),0],
        "top_bracket_1":         [(BaseController.RIGHT, 16),0],
        "top_bracket_2":         [(BaseController.RIGHT, 17),0],
        "screwdriver_1":         [(BaseController.RIGHT, 20),0],
    }
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

    def _run(self):
        while not is_shutdown():
            pass

def main():
    def_model = default_supp_actions(chair_task_HTM())

    # controller = UserPrefDemoController()
    # controller.time_step = 0
    # controller.run()

if __name__ == '__main__': main()
