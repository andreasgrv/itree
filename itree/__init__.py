""" itree api """


class ITreeError(Exception):
    pass


class ITree(object):

    """API for ITree structure - I tried to focus on simplicity of use.
    this object is usable as a node object but has access to more information
    about the actual tree through the tree instance variable"""

    # TODO will anyone want to create an empty ITree??
    def __init__(self, root_data):
        self.sibling_index = 0
        self.tree = ITreeMatrix(levels=1)
        self.level_index = 0
        self.tree.set_root(root_data)

    def __getattr__(self, name):
        return getattr(self.tree, name)

    def __getitem__(self, index):
        return self.tree[index]

    def __repr__(self):
        return repr(self.tree)

    def __str__(self):
        return str(self.tree)

    def __len__(self):
        return len(self.tree)


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
        return '%s : (%s, %s)' % (self.node, self.level_index, self.sibling_index)

    def __str__(self):
        return '%s : (%s, %s)' % (self.node, self.level_index, self.sibling_index)

    def __getitem__(self, index):
        return self.tree[index]

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


from structs import ITreeMatrix, ITreeNode
