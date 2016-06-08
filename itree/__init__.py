""" itree api """
from structs import ITreeMatrix, ITreeError


class AugmentedITreeNode(object):

    """ITreeNode extended with extra information about the tree.
    this object is usable as a node object but has access to more information
    about the actual tree through the tree variable - reference."""

    def __init__(self, level_index, sibling_index, tree):
        """

        :level_index: int - height in the tree, what level this node is on
        :sibling_index: int - the index of the node on this level
        :tree: ITreeMatrix - the tree implementation (a list of lists)

        """
        self.level_index = level_index
        self.sibling_index = sibling_index
        self.tree = tree
        # below solution to extending the node is clearly overkill
        # reasons:
        # a) unclear why a user of itree would expect such behaviour
        # b) blurs the lines between the node as a container and the data
        # c) probably expensive computationally
        # # append all non private stuff to augmented node
        # try:
        #     for key, value in self.node.data.__class__.__dict__.items():
        #         if not key.startswith('_'):
        #             if key in self.__class__.__dict__:
        #                 setattr(self.__class__, '_%s' % key, value)
        #             else:
        #                 setattr(self.__class__, key, value)
        #     # append all non private variables to augmented node
        #     for key, value in self.node.data.__dict__.items():
        #         if not key.startswith('_'):
        #             if key in self.__dict__:
        #                 setattr(self, '_%s' % key, value)
        #             else:
        #                 setattr(self, key, value)
        # except Exception:
        #     pass

    def __repr__(self):
        return '%s at (%s, %s)' % (self.node,
                                   self.level_index,
                                   self.sibling_index)

    def __str__(self):
        return '%s at (%s, %s)' % (self.node,
                                   self.level_index,
                                   self.sibling_index)

    def __call__(self, *indices):
        """get itree node at indices (level, left_index). people who use matlab
        and octave will love me

        :indices: level, left_index indices to get referenced node
        if you pass more than two indices they will be ignored.
        :returns: node_class instance - api wrapped ITreeNode

        """
        level_index, sibling_index = indices[:2]
        # check if node exists
        self.tree[level_index][sibling_index]
        # use self.__class__ to support extending this class using inheritance
        # we don't return the value of the node, we keep the information
        # needed to access it when we have to
        return self.__class__(level_index, sibling_index, self.tree)

    def __getitem__(self, indices):
        """get itree node at indices [level, left_index]. python style getter,
        people who use pandas will love me (what are the odds that someone
        reading this comment actually uses real live animal pandas?)

        :indices: level, left_index indices to get referenced node
        :returns: node_class instance - api wrapped ITreeNode

        """
        level_index, sibling_index = indices
        # check if node exists
        self.tree[level_index][sibling_index]
        # use self.__class__ to support extending this class using inheritance
        # we don't return the value of the node, we keep the information
        # needed to access it when we have to
        return self.__class__(level_index, sibling_index, self.tree)

    @property
    def index(self):
        """get the indices that refer to this node as a tuple

        :returns: tuple - (level, left_index)
        """
        return (self.level_index, self.sibling_index)

    @property
    def height(self):
        """get level index

        :returns: int - how far from the root this node is
        """
        return (self.level_index)

    @property
    def width(self):
        """get sibling index

        :returns: int - how far from the farmost left node on this level
        this node is
        """
        return (self.sibling_index)

    @property
    def node(self):
        """get the real node - the implementation

        :returns: ITreeNode - the node this proxy object references
        """
        return self.tree[self.level_index][self.sibling_index]

    @property
    def data(self):
        """get the data of this node

        :returns: YouKnowWhatTypeSinceYouPutItHere - the data you stored in
        the node
        """
        return self.node.data

    @property
    def children(self):
        """get the children of this node as a list

        :returns: list - of proxy objects of this class or subclass you made
        """
        return [self.__class__(self.level_index+1, sibling_index, self.tree)
                for sibling_index in self.node.children_indices]

    @property
    def parent(self):
        """get the parent of this node

        :returns: AugmentedITreeNode - or subclass you made wrapping the
        parent ITreeNode
        """
        parent_index = self.node.parent_index
        return self.__class__(self.level_index-1, parent_index, self.tree)

    @property
    def siblings(self):
        # TODO: guess what..
        raise NotImplemented

    def append_child(self, data):
        """create and append a child node to this node in the tree setting
        its data to :data:. returns the newly created node wrapped in this
        proxy object for ease of use.

        :data: YouKnowWhatTypeSinceYouPutItHere - your data
        :returns: AugmentedITreeNode - or subclass you made wrapping the
        newly created ITreeNode
        """
        args = (data, self.level_index, self.sibling_index)
        level_index, sibling_index = self.tree.append_child(*args)
        return self.__class__(level_index, sibling_index, self.tree)

    def add_sibling(self, data):
        # TODO: guess what..
        raise NotImplemented

    def delete(self):
        """delete this node. only allowed if this node doesn't have children"""
        self.tree.remove_node(self.level_index, self.sibling_index)


class ITree(object):

    """indexable tree api class. use this class to construct an itree, you will
    probably never need to use it again. if you wish to add extra functionality
    don't forget to set node_class"""

    def __init__(self, tree=None, node_class=AugmentedITreeNode):
        """

        :tree: ITreeMatrix - internal tree structure incase we want to
        construct an ITree from an existing one (useful for cloning probably)
        :node_class: type - subclass of AugmentedITreeNode, used for wrapping
        ITreeNode and encompassing custom functionality. set this if you want
        to add custom functionality to your tree.

        """
        self.tree = tree or ITreeMatrix()
        self.node_class = node_class

    def __call__(self, *indices):
        """get itree node at indices (level, left_index). people who use matlab
        and octave will love me

        :indices: level, left_index indices to get referenced node
        if you pass more than two indices they will be ignored.
        :returns: node_class instance - api wrapped ITreeNode

        """
        level_index, sibling_index = indices[:2]
        # check if node exists
        self.tree[level_index][sibling_index]
        # use self.__class__ to support extending this class using inheritance
        # we don't return the value of the node, we keep the information
        # needed to access it when we have to
        return self.node_class(level_index, sibling_index, self.tree)

    def __getitem__(self, indices):
        """get itree node at indices [level, left_index]. python style getter,
        people who use pandas will love me (what are the odds that someone
        reading this comment actually uses real live animal pandas?)

        :indices: level, left_index indices to get referenced node
        :returns: node_class instance - api wrapped ITreeNode

        """
        level_index, sibling_index = indices
        # check if node exists
        self.tree[level_index][sibling_index]
        # use self.__class__ to support extending this class using inheritance
        # we don't return the value of the node, we keep the information
        # needed to access it when we have to
        return self.node_class(level_index, sibling_index, self.tree)

    def __repr__(self):
        return repr(self.tree)

    def __str__(self):
        return str(self.tree)

    def __len__(self):
        """get number of nodes in this tree"""
        return len(self.tree)

    @property
    def height(self):
        """get distance from root to lowest leaf"""
        return self.tree.height

    @property
    def depth(self):
        """get distance from root to lowest leaf"""
        return self.tree.depth

    @property
    def root(self):
        """get this tree's root"""
        # check it exists
        self.tree.root
        return self.node_class(0, 0, self.tree)

    @property
    def children(self):
        """get the children of root node as a list

        :returns: list - of proxy objects of this class or subclass you made
        """
        return self.root.children

    def set_root(self, data):
        """creates and appends the root of the tree."""
        level_index, sibling_index = self.tree.set_root(data)
        return self.node_class(level_index, sibling_index, self.tree)

    def append_child(self, data):
        """creates and appends the root of the tree - alias for set_root.
        exists to follow naming convention with nodes to assist in cases
        where recursion is required"""
        level_index, sibling_index = self.tree.set_root(data)
        return self.node_class(level_index, sibling_index, self.tree)

    def to_nested_list(self):
        """convert this itree to a nested list"""

        def collapse_one_level(l):
            """collapses contained lists of a list once (not recursive)"""
            for each in l:
                if isinstance(each, list):
                    for other in each:
                        yield other
                else:
                    yield each

        def recursively_nest(node):
            """recurse into tree and nest children on the right of
            the parent in a list"""
            if node.children:
                current = [node.data]
                nested_children = map(recursively_nest, node.children)
                children = list(collapse_one_level(nested_children))
                current.append(children)
                return current
            else:
                return node.data

        return recursively_nest(self.root)

    @classmethod
    def from_nested_list(cls, multi_list, *args, **kwargs):
        """create an itree from a nested list"""
        def recursively_append(l, node):
            child = None
            for index in range(len(l)):
                data = l[index]
                # next data point (first item never a list in a valid tree)
                next_data = l[(index+1) % len(l)]
                # if we find a list, it means the previous node
                # has the list nodes as children
                # we keep a reference to the previous node (child)
                # in the else block which should always have run first
                # at least once if this is a valid tree representation
                if isinstance(data, list):
                    if child is None:
                        raise ITreeError('this multi list cannot be a tree')
                    if isinstance(next_data, list):
                        raise ITreeError('this multi list cannot be a tree, '
                                         'it contains two consecutive lists')
                    recursively_append(data, child)
                else:
                    # if next element is a list, this node has children
                    # we need to keep a reference to it to pass to recursion
                    if isinstance(next_data, list):
                        child = node.append_child(data)
                    # no children - don't need to keep reference
                    else:
                        node.append_child(data)

        if len(multi_list) > 2:
            raise ITreeError('this list represents a bush not a tree '
                             ' - it has many roots')
        t = cls(*args, **kwargs)
        recursively_append(multi_list, t)
        return t


if __name__ == "__main__":
    l = [1, [3, [20, [4, 10], 5, [2, [6]], 3, [3]]]]
    i = ITree.from_nested_list(l)
    i[0, 0]
    r = i.to_nested_list()
    print('correct:     %s' % l)
    print('constructed: %s' % r)
    print(r == l)
    print(i(2, 2).append_child('blue'))
    print(i)
