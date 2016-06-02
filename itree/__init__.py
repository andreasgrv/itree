""" itree api """


class ITreeError(Exception):
    pass


class ITree(object):

    """API for ITree structure - I tried to focus on simplicity of use.
    this object is usable as a node object but has access to more information
    about the actual tree through the tree instance variable"""

    def __init__(self):
        self.tree = ITreeMatrix()

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

    def append_child(self, data):
        child = self.tree.set_root(data)
        return child

    def to_multilevel_list(self):
        def collapse_one_level(l):
            for each in l:
                if isinstance(each, list):
                    for other in each:
                        yield other
                else:
                    yield each

        def recursively_append(node):
            if node.children:
                print('%s has children : %s' % (node, node.children))
                current = [node.data]
                c = list(collapse_one_level(map(recursively_append, node.children)))
                current.append(c)
                print(current)
                return current
            else:
                return node.data
        return recursively_append(self.root)

    @classmethod
    def from_multilevel_list(cls, multi_list):
        def recursively_append(l, node):
            child = None
            for index in range(len(l)):
                data = l[index]
                # next data point (first item never a list in a valid tree)
                next_data = l[(index+1)%len(l)]
                # if we find a list, it means the previous node
                # has the list nodes as children
                # we keep a reference to the previous node (child)
                # in the else block which should always have run first
                # at least once if this is a valid tree representation
                if isinstance(data, list):
                    if child is None:
                        raise ValueError('this multi list cannot be a tree')
                    if isinstance(next_data, list):
                        raise ValueError('this multi list cannot be a tree, '
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
            raise ValueError('this list represents a bush not a tree '
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


from structs import ITreeMatrix, ITreeNode

if __name__ == "__main__":
    l = [1,[3,[20, [4,10],5,[2, [6]],3, [3]]]]
    i = ITree.from_multilevel_list(l)
    r = i.to_multilevel_list()
    print('correct: %s' % l)
    print(r)
    print(r==l)
