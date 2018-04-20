"""
Bhavani Ananthabhotla
"""


ARROW = "->"
PARALLEL = "||"

class HTM(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    # @classmethod
    # def fromlist(cls, lst):
    #   # [root, [ [child1, []] , [child2, []] ]]
    #   cls.data = lst[0]
    #   for item in lst[1]:
    #       cls.children += HTM.fromlist(item)


    def add_children(self, lst):
        self.children += [HTM(data) for data in lst]
    
    def child(self, index):
        return self.children[index]

    # def append(self, ref, lst):
    #   self.children[ref].children += [HTM(child) for child in lst]
    
    def __str__(self, level=0):
        s = "\t"*level+str(self.data)+"\n"
        for child in self.children:
            s += child.__str__(level+1)
        return s