import rospy
from human_robot_collaboration.controller import BaseController

class SuppBhvsHMMController(BaseController):
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
    BRING = 'get_pass' #suction
    CLEAR = 'cleanup'
    HOLD_LEG = 'hold_leg' #higher 'hold'
    HOLD_TOP = 'hold_top' #hold
    HOLD = 'hold_leg'

    def __init__(self, timer_path=None):
        super(SuppBhvsHMMController, self).__init__(
            left=True,
            right=True,
            speech=False,
            listen=True,
            recovery=True,
            timer_path=os.path.join(path, timer_path),
            **kwargs)

    def _run(self):
        while not is_shutdown():
            pass

controller = SuppBhvsHMMController(timer_path='timer.json')

if __name__ == '__main__':

    controller.time_step = 0
    controller.run()
