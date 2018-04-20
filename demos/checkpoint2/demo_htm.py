import json

from task_models.task import (HierarchicalTask, AbstractAction,
                              SequentialCombination, ParallelCombination,
                              LeafCombination)


# def chair_htm_simple():
#     take_base = LeafCombination(AbstractAction('Take base'))
#     mount_leg_combinations = [
#         SequentialCombination(
#             [LeafCombination(AbstractAction('Take leg {}'.format(i))),
#              LeafCombination(AbstractAction('Attach leg {}'.format(i)))
#              ],
#             name='Mount leg {}'.format(i))
#         for i in range(4)
#         ]
#     mount_frame = SequentialCombination(
#         [LeafCombination(AbstractAction('Take frame'), highlighted=True),
#          LeafCombination(AbstractAction('Attach frame'))
#          ],
#         name='Mount frame')

#     chair_task = HierarchicalTask(
#         root=ParallelCombination(
#             [take_base,
#              ParallelCombination(mount_leg_combinations, name='Mount legs'),
#              mount_frame,
#              ],
#             name='Mount chair')
#         )

#     print(json.dumps(chair_task.as_dictionary(), indent=2))

# from hrc_pref_supp_bhv.task_def import TaskDef 

class ChairTaskDefSimple(object):
    """Class for defining an actual chair task
    Includes functionality for transfer learning task
    """
    FEATURES = {
        0:  'back',
        1:  'back_bracket_more_0',
        2:  'back_bracket_more_1',
        3:  'dowel_more_0',
        4:  'dowel_more_1',
        5:  'dowel_more_2',
        6:  'dowel_more_3',
        7:  'front_bracket_more_0',
        8:  'front_bracket_more_1',
        9:  'screwdriver',
        10: 'seat',
    }
    MAIN_OBJ = {
        0:  'back',
        1:  'back_bracket',
        2:  'dowel',
        3:  'front_bracket',
        4:  'screwdriver',
        5:  'seat',
    }
    # Indices of where the first, second, etc. obj
    # of that type are present in the features array
    OBJ_COUNT_IDX = {
        'back':           [0],
        'back_bracket':   [1, 2],
        'dowel':          [3, 4, 5, 6],
        'front_bracket':  [7, 8],
        'screwdriver':    [9],
        'seat':           [10],
    }
    OBJ_PRESENCE = {
        'gatherparts_leg_1':  [2, 3],
        'assemble_leg_1':     [4],
        'gatherparts_leg_2':  [2, 3],
        'assemble_leg_2':     [4],
        'gatherparts_leg_3':  [2, 1],
        'assemble_leg_3':     [4],
        'gatherparts_leg_4':  [2, 1],
        'assemble_leg_4':     [4],
        'gatherparts_seat':   [5],
        'assemble_seat':      [4],
        'gatherparts_back':   [0],
        'assemble_back':      [4],
    }
    OBJ_DISTINCT = {
        0:  'back',
        1:  'back_bracket_1',
        2:  'back_bracket_2',
        3:  'dowel_1',
        4:  'dowel_2',
        5:  'dowel_3',
        6:  'dowel_4',
        7:  'front_bracket_1',
        8:  'front_bracket_2',
        9:  'screwdriver',
        10: 'seat',
    }
    OBJ_PRESENCE_DISTINCT = {
        'gatherparts_leg_1':  [3, 7],
        'assemble_leg_1':     [3, 7, 9],
        'gatherparts_leg_2':  [4, 8],
        'assemble_leg_2':     [4, 8, 9],
        'gatherparts_leg_3':  [5, 1],
        'assemble_leg_3':     [5, 1, 9],
        'gatherparts_leg_4':  [6, 2],
        'assemble_leg_4':     [6, 2, 9],
        'gatherparts_seat':   [10],
        'assemble_seat':      [10, 9],
        'gatherparts_back':   [0],
        'assemble_back':      [0, 9],
    }
    OBS_PROBS = {
        'gp_l1_probs':  [0, 0, 1, 1, 0, 0],
        'ass_l1_probs': [0, 0, 1, 1, 1, 0],
        'gp_l2_probs':  [0, 0, 1, 1, 0, 0],
        'ass_l2_probs': [0, 0, 1, 1, 1, 0],
        'gp_l3_probs':  [0, 1, 1, 0, 0, 0],
        'ass_l3_probs': [0, 1, 1, 0, 1, 0],
        'gp_l4_probs':  [0, 1, 1, 0, 0, 0],
        'ass_l4_probs': [0, 1, 1, 0, 1, 0],
        'gp_s_probs':   [0, 0, 0, 0, 0, 1],
        'ass_s_probs':  [0, 0, 0, 0, 1, 1],
        'gp_b_probs':   [1, 0, 0, 0, 0, 0],
        'ass_b_probs':  [1, 0, 0, 0, 1, 0],
    }
    # SUPP_BHVS = {
    #     'cleanup':            0,
    #     'br_scrdrv':          1,
    #     'br_front_brackets':  2,
    #     'br_back_brackets':   3,
    #     'br_dowel':           4,
    #     'hold':               5,
    #     'br_seat':            6,
    #     'br_back':            7,
    # }
    #latest supp bhvs:
    # SUPP_BHVS = {
    #     'gatherparts_leg_1':  0,
    #     'assemble_leg_1':     1,
    #     'gatherparts_leg_2':  2,
    #     'assemble_leg_2':     3,
    #     'gatherparts_leg_3':  4,
    #     'assemble_leg_3':     5,
    #     'gatherparts_leg_4':  6,
    #     'assemble_leg_4':     7,
    #     'gatherparts_seat':   8,
    #     'assemble_seat':      9,
    #     'gatherparts_back':   10,
    #     'assemble_back':      11,
    # }
    SUPP_BHVS = {
        'cleanup':            0,
        'br_screwdriver':     1,
        'br_front_bracket':   2,
        'br_back_bracket':    3,
        'br_dowel':           4,
        'hold':               5,
        'br_seat':            6,
        'br_back':            7,
    }
    SUPP_BHVS_REV = {v: k for k, v in SUPP_BHVS.iteritems()}
    TRAIN_SET_SIZE = 500
    TEST_SET_SIZE = 100
    NUM_FEATS = 11  # had 12, 5, 6
    # 'obj_presence', 'obj_presence_distinct'
    # 'cumulative', 'shared', 'distinct'
    FEAT = 'obj_presence'
    NUM_USER_DEMS = 5
    NUM_USER_DEMS_TEST_GT = 100

    def __init__(self, tf):
        # main task
        self.main_task = None
        # transfer learning task
        self.tf_task = None
        # 0, 1, 2 representing transfer learning
        self.tf = tf
        self.user_prefs = dict()
        self._task_def()
        self._create_user_prefs()
        self._generate_necessary_trajectories(self.main_task)
        self._generate_necessary_trajectories(self.tf_task)

    @property
    def supp_bhvs(self):
        return self.SUPP_BHVS

    @property
    def supp_bhvs_rev(self):
        return self.SUPP_BHVS_REV

    def _task_def(self):
        gp_l1 = LeafCombination(PredAction
                                ('gatherparts_leg_1', self.NUM_FEATS, self.OBS_PROBS['gp_l1_probs']))
        ass_l1 = LeafCombination(PredAction
                                 ('assemble_leg_1', self.NUM_FEATS, self.OBS_PROBS['ass_l1_probs']))
        gp_l2 = LeafCombination(PredAction
                                ('gatherparts_leg_2', self.NUM_FEATS, self.OBS_PROBS['gp_l2_probs']))
        ass_l2 = LeafCombination(PredAction
                                 ('assemble_leg_2', self.NUM_FEATS, self.OBS_PROBS['ass_l2_probs']))
        gp_l3 = LeafCombination(PredAction
                                ('gatherparts_leg_3', self.NUM_FEATS, self.OBS_PROBS['gp_l3_probs']))
        ass_l3 = LeafCombination(PredAction
                                 ('assemble_leg_3', self.NUM_FEATS, self.OBS_PROBS['ass_l3_probs']))
        gp_l4 = LeafCombination(PredAction
                                ('gatherparts_leg_4', self.NUM_FEATS, self.OBS_PROBS['gp_l4_probs']))
        ass_l4 = LeafCombination(PredAction
                                 ('assemble_leg_4', self.NUM_FEATS, self.OBS_PROBS['ass_l4_probs']))
        gp_s = LeafCombination(PredAction
                               ('gatherparts_seat', self.NUM_FEATS, self.OBS_PROBS['gp_s_probs']))
        ass_s = LeafCombination(PredAction
                                ('assemble_seat', self.NUM_FEATS, self.OBS_PROBS['ass_s_probs']))
        gp_b = LeafCombination(PredAction
                               ('gatherparts_back', self.NUM_FEATS, self.OBS_PROBS['gp_b_probs']))
        ass_b = LeafCombination(PredAction
                                ('assemble_back', self.NUM_FEATS, self.OBS_PROBS['ass_b_probs']))
        f_l1 = SequentialCombination([gp_l1, ass_l1], name='finish_leg1')
        f_l2 = SequentialCombination([gp_l2, ass_l2], name='finish_leg2')
        f_l3 = SequentialCombination([gp_l3, ass_l3], name='finish_leg3')
        f_l4 = SequentialCombination([gp_l4, ass_l4], name='finish_leg4')
        f_s = SequentialCombination([gp_s, ass_s], name='finish_seat')
        f_b = SequentialCombination([gp_b, ass_b], name='finish_back')
        f_legs = ParallelCombination([f_l1, f_l2, f_l3, f_l4], name='finish_legs')
        f_rest = ParallelCombination([f_b, f_s], name='finish_rest')

        main_task = HierarchicalTaskHMMSuppRD(root=
                                              SequentialCombination([f_legs, f_rest], name='complete'),
                                              name='TaskA',
                                              num_feats_action=self.NUM_FEATS,
                                              feats=self.FEAT,
                                              supp_bhvs=self.SUPP_BHVS,
                                              obj_presence=self.OBJ_PRESENCE,
                                              obj_count_idx=self.OBJ_COUNT_IDX,
                                              main_obj=self.MAIN_OBJ)

        tf_task = HierarchicalTaskHMMSuppRD(root=
                                            SequentialCombination([f_rest, f_legs], name='complete'),
                                            name='TaskB',
                                            num_feats_action=self.NUM_FEATS,
                                            feats=self.FEAT,
                                            supp_bhvs=self.SUPP_BHVS,
                                            obj_presence=self.OBJ_PRESENCE,
                                            obj_count_idx=self.OBJ_COUNT_IDX,
                                            main_obj=self.MAIN_OBJ)

        self.main_task = main_task
        self.tf_task = tf_task

    def _gen_feat_probs(self):
        return np.random.uniform(low=0, high=1, size=self.NUM_FEATS)

    def _create_user_prefs(self):
        user_prefs = dict()

        user_prefs['user1'] = \
            {'cleanup': ['end'], 'br_screwdriver':['time_assemble_leg_1', 'assemble_seat', 'assemble_back'],
             'br_front_bracket': ['gatherparts_leg_1', 'gatherparts_leg_2'],
             'br_back_bracket': ['gatherparts_leg_3', 'gatherparts_leg_4'],
             'br_dowel': ['all_gatherparts_leg'],
             'hold': ['all_assemble_leg'],
             'br_seat': ['gatherparts_seat'], 'br_back': ['gatherparts_back']
             }

        user_prefs['user2'] = \
            {'cleanup': ['end'], 'br_screwdriver':['time_assemble_leg_1', 'assemble_seat', 'assemble_back'],
             'br_front_bracket': ['gatherparts_leg_1', 'gatherparts_leg_2'],
             'br_back_bracket': ['gatherparts_leg_3', 'gatherparts_leg_4'],
             'br_dowel': ['all_gatherparts_leg'],
             'hold': ['all_assemble_leg'],
             'br_seat': ['gatherparts_seat'], 'br_back': ['gatherparts_back']
             }
        # latest
        # user_prefs['user3'] = \
        #     {'gatherparts_leg_1':['gatherparts_leg_1'],
        #      'assemble_leg_1': ['assemble_leg_1'],
        #      'gatherparts_leg_2': ['gatherparts_leg_2'],
        #      'assemble_leg_2': ['assemble_leg_2'],
        #      'gatherparts_leg_3': ['gatherparts_leg_3'],
        #      'assemble_leg_3': ['assemble_leg_3'],
        #      'gatherparts_leg_4': ['gatherparts_leg_4'],
        #      'assemble_leg_4': ['assemble_leg_4'],
        #      'gatherparts_seat': ['gatherparts_seat'],
        #      'assemble_seat': ['assemble_seat'],
        #      'gatherparts_back': ['gatherparts_back'],
        #      'assemble_back': ['assemble_back'],
        #      }

        # # user_prefs['user1'] = \
        # #     {'cleanup': ['end'], 'br_scrdrv': ['time_assemble_leg_1'],
        # #      'br_front_brackets': ['gatherparts_leg_1', 'gatherparts_leg_2'],
        # #      'br_back_brackets': ['gatherparts_leg_3', 'gatherparts_leg_4'],
        # #      'br_dowel': ['all_gatherparts_leg'],
        # #      'hold': ['all_assemble_leg'],
        # #      'br_seat': ['gatherparts_seat'], 'br_back': ['gatherparts_back']}
        # user_prefs['user4'] = \
        #     {'cleanup': ['end'], 'br_scrdrv': ['time_assemble_leg_3'],
        #      'br_front_brackets': ['gatherparts_leg_1'],
        #      'br_back_brackets': ['gatherparts_leg_4'],
        #      'br_dowel': ['gatherparts_leg_1', 'gatherparts_leg_3', 'gatherparts_leg_4'],
        #      'hold': ['all_assemble_leg'],
        #      'br_seat': ['gatherparts_seat'], 'br_back': ['gatherparts_back']
        #      }
        # user_prefs['user5'] = \
        #     {'cleanup': ['end'], 'br_scrdrv': ['time_assemble_leg_3'],
        #      'br_front_brackets': ['gatherparts_leg_2'],
        #      'br_back_brackets': ['gatherparts_leg_4'],
        #      'br_dowel': ['gatherparts_leg_2', 'gatherparts_leg_4'],
        #      'hold': ['assemble_leg_2', 'assemble_leg_4'],
        #      'br_seat': ['gatherparts_seat'], 'br_back': ['gatherparts_back']
        #      }

        self.user_prefs = user_prefs

    def _generate_necessary_trajectories(self, task):
        task.gen_training_set_actions(self.TRAIN_SET_SIZE)
        task.gen_test_set_actions(self.TEST_SET_SIZE)

        task.gen_train_set_sb(self.user_prefs, self.NUM_USER_DEMS)
        task.gen_test_set_sb(self.user_prefs, self.NUM_USER_DEMS_TEST_GT)

    @staticmethod
    def __traj_gen(trajectories):
        for traj_idx, traj in enumerate(trajectories):
            yield traj, traj_idx

    def prep_X(self, trajectories):
        X = np.empty([1, self.NUM_FEATS])
        X_lens = []
        train_dataset = self.__traj_gen(trajectories)
        first_concat = True
        for episode, file_name in train_dataset:
            X_lens.append(episode.shape[0])
            if episode.shape[1] != self.NUM_FEATS:
                logging.warning("feat length not as expected in {} ".format(file_name))
            X = np.vstack((X, episode))
            if first_concat is True:
                X = X[1:]
                first_concat = False
return X, X_lens



print(json.dumps(TaskDef.main_task.as_dictionary(), indent=2))
