""" itree api """


class ITreeError(Exception):
    pass


class ITree(object):

    """API for ITree structure - I tried to focus on simplicity of use.
    this object is usable as a node object but has access to more information
    about the actual tree through the tree instance variable"""

    def __init__(self):
        self.tree = ITreeMatrix()

    def __getitem__(self, index):
        return self.tree[index]

    def __repr__(self):
        return repr(self.tree)

    def __str__(self):
        return str(self.tree)

    def __len__(self):
        return len(self.tree)

    @property
    def height(self):
        """get distance from root to lowest leaf"""
        self.tree.height

    @property
    def root(self):
        """get this tree's root"""
        return self.tree.root

    @property
    def children(self):
        """get children nodes"""
        return self.tree.root.children

    def set_root(self, data):
        """creates and appends the root of the tree."""
        child = self.tree.set_root(data)
        return child

    def append_child(self, data):
        """creates and appends the root of the tree - alias for set_root.
        exists to follow naming convention with nodes to assist in cases
        where recursion is required"""
        child = self.tree.set_root(data)
        return child

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
    def from_nested_list(cls, multi_list):
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
        t = ITree()
        recursively_append(multi_list, t)
        return t


class AugmentedITreeNode(object):

    """API for ITree structure - I tried to focus on simplicity of use.
    this object is usable as a node object but has access to more information
    about the actual tree through the tree instance variable"""

    def __init__(self, level_index, sibling_index, tree):
        """TODO: to be defined1.

        :node: TODO
        :level_index: TODO
        :sibling_index: TODO

        """
        self.level_index = level_index
        self.sibling_index = sibling_index
        self.tree = tree

    def __repr__(self):
        return '%s at (%s, %s)' % (self.node,
                                   self.level_index,
                                   self.sibling_index)

    def __str__(self):
        return '%s at (%s, %s)' % (self.node,
                                   self.level_index,
                                   self.sibling_index)

    def __getitem__(self, index):
        return self.tree[index]

    @property
    def index(self):
        return (self.level_index, self.sibling_index)

    @property
    def height(self):
        """how far from the root this node is"""
        return (self.level_index)

    @property
    def width(self):
        """how far from the farmost left node this node is"""
        return (self.sibling_index)

    @property
    def node(self):
        return self.tree.get_node(self.level_index, self.sibling_index)

    @property
    def data(self):
        return self.node.data

    @property
    def children(self):
        return [self.tree[self.level_index + 1][sibling_index]
                for sibling_index in self.node.children_indices]

    @property
    def parent(self):
        parent_index = self.node.parent_index
        return self.tree[self.level_index - 1][parent_index]

    @property
    def siblings(self):
        return self.tree[self.level_index]

    def append_child(self, data):
        child = self.tree.append_child(data, self.level_index, self.sibling_index)
        return child

    def add_sibling(self, data):
        """TODO: Docstring for append_child.

        :data: TODO
        :returns: TODO

        """

    def delete(self):
        """TODO: Docstring for delete.
        :returns: TODO

        """
        self.tree.remove_node(self.level_index, self.sibling_index)


from itree.structs import ITreeMatrix

if __name__ == "__main__":
    l = [1, [3, [20, [4, 10], 5, [2, [6]], 3, [3]]]]
    i = ITree.from_nested_list(l)
    r = i.to_nested_list()
    print('correct:     %s' % l)
    print('constructed: %s' % r)
    print(r == l)
