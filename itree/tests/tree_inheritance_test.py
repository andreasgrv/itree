"""test adding itree functionality through inheritance"""
from itree import ITree, AugmentedITreeNode


class MyExtendedTree(ITree):

    """A tree with added functionality - what we want to have on our tree."""

    def __init__(self):
        super(MyExtendedTree, self).__init__(node_class=MyExtendedNode)

    def say_hi(self):
        """this method is on the node, and not on the data.
        check this works """
        print("Hi, I'm a tree wooooo hwahahwa hwoooo waaaa hwoooo nibbit!"
              " meet my nodes:")
        self.root.say_hi()

    @property
    def sum(self):
        return self.root.sum


class MyExtendedNode(AugmentedITreeNode):

    """A tree node with added functionality"""

    def say_hi(self):
        """this method is on the node, and not on the data.
        check this works """
        print(self.greeting)
        for child in self.children:
            child.say_hi()

    @property
    def greeting(self):
        return "hi, I'm node: %s" % repr(self)

    @property
    def sum(self):
        return sum(each.sum for each in self.children) + self.data


def test_say_hi(capsys):
    """test that nodes are visited as expected"""
    tree = MyExtendedTree()
    child = tree.append_child(1)
    child.append_child(2)
    last_child = child.append_child(3).append_child(4).append_child(5)
    tree.say_hi()
    out, err = capsys.readouterr()
    out = out.strip()
    lines = out.split('\n')
    assert(len(lines) == 6)
    assert(lines[-1].strip() == last_child.greeting)


def test_sum():
    """test that accessing node data works as expected"""
    tree = MyExtendedTree()
    child = tree.append_child(1)
    child.append_child(2)
    child.append_child(3).append_child(4).append_child(5)
    assert(tree.sum == sum(range(6)))
