import random
ARROW = "->"
PARALLEL = "||"

class HTM(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_children(self, lst):
        self.children += [HTM(data) for data in lst]
    
    def child(self, index):
        return self.children[index]
    
    def __str__(self, level=0):
        s = "\t"*level+str(self.data)+"\n"
        for child in self.children:
            s += child.__str__(level+1)
        return s

    def get_leaves(self):
        leaves = []
        for child in self.children:
            if len(child.children) ==0 :
                leaves.append(child.data)
            else:
                leaves += child.get_leaves()
        return leaves
    
    def gen_task_seq(self):
        traj = []
        if self.data == ARROW:
            for child in self.children:
                traj.extend(child.gen_task_seq())
        elif self.data == PARALLEL:
            for child in random.sample(self.children, len(self.children)):
                traj.extend(child.gen_task_seq())
        else:
            traj += [self.data]
        return traj

    def get_len(self):
        leaves = self.get_leaves()
        return len(leaves)