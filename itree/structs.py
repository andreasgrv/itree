from itree import AugmentedITreeNode, ITreeError


class ITreeNode(object):

    """itree node representation. we wrap the data in the node and keep indices
    to the parent, the first child and the last child. we dont need two
    indices, since we can figure out the depth of the parent and children nodes
    by searching one level higher and one level lower than the current node
    accordingly"""

    def __init__(self, data, parent_index=-1):
        self.data = data
        self.parent_index = parent_index
        self._first_child_index = self._last_child_index = None

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)

    @property
    def children_indices(self):
        if self._first_child_index is None:
            # empty range
            return range(0)
        return range(self._first_child_index, self._last_child_index + 1)

    def removed_sibling(self):
        """call me if you removed left sibling"""
        if self._first_child_index is not None:
            self._first_child_index -= 1
            self._last_child_index -= 1

    def append_child(self, sibling_index):
        if self._first_child_index is None:
            self._first_child_index = self._last_child_index = sibling_index
        else:
            assert(sibling_index == self._last_child_index + 1)
            self._last_child_index += 1

    def remove_child(self, sibling_index):
        """remove child with value sibling_index, since we don't want to have
        gaps in our indices, after a child removal we need to decrement the
        indices of the indices of its siblings.

        :sibling_index: TODO
        :returns: TODO

        """
        if sibling_index in self.children_indices:
            if sibling_index == self._first_child_index:
                self._first_child_index = self._last_child_index = None
            else:
                self._last_child_index -= 1
        else:
            raise ITreeError('child with index: %s not found' % sibling_index)


class ITreeRow(list):

    """A row of the ITreeMatrix which represents a level of the tree,
    all nodes at same height or depth are on the same level."""

    def __init__(self, level, tree):
        """TODO: to be defined1.

        :level: TODO
        :tree: TODO

        """
        self.level = level
        self.tree = tree

    def __getitem__(self, index):
        # call to super get item throws index error
        # if this call isn't allowed
        super(ITreeRow, self).__getitem__(index)
        return AugmentedITreeNode(self.level, index, self.tree)

    def __setitem__(self, index, item):
        """ allow setting node data with setter,
        this bypasses setting the node - we can't allow that anyways
        since it could break the tree structure"""
        self[index].data = item

    def get_node(self, index):
        return super(ITreeRow, self).__getitem__(index)

    def append_child(self, data, parent_column):
        """ append data as node next to its siblings, namely next to the nodes
        which have the same parent with it. If it is the first sibling, it must
        be inserted according to the parents column id ordering"""
        # find the last child with a parent that has index target_index
        # or find a child with a parent index less than our target index
        # the rationale is that parents are siblings, and therefore
        # their ids are also ordered as an ascending sequence
        child = ITreeNode(data, parent_index=parent_column)
        sibling_index = 0
        for index, each in enumerate(reversed(self)):
            if each.parent_index <= parent_column:
                sibling_index = len(self) - index
                break
        self.insert(sibling_index, child)
        # remember to add child to the parents children list
        # if the node has parents - negative indices correspond to no parents
        parent_level = self.level - 1
        if parent_level >= 0:
            parent = self.tree.get_node(self.level - 1, parent_column)
            parent.append_child(sibling_index)
        return AugmentedITreeNode(self.level, sibling_index, self.tree)

    def remove_child(self, parent_index, child_index):
        """TODO: Docstring for remove_child.

        :index: TODO
        :returns: TODO

        """
        self[parent_index].node.remove_child(child_index)
        # since the sibling_index must be a consecutive number with no gaps
        # we need to lower the indices by one for all the succeeding nodes
        for parent_node in self[parent_index+1:]:
            parent_node.removed_sibling()


class ITreeMatrix(object):

    """ITree internal representation - we keep the tree nodes in a matrix.
    each row contains a level of the tree. each column contains sibling nodes
    with the same number - meaning nodes which have the same number of siblings
    to their left (political comment removed)"""

    def __init__(self, levels=1):
        if levels < 0:
            raise ValueError('rows must be positive')
        self.levels = [ITreeRow(i, self) for i in range(levels)]

    def __getitem__(self, slices):
        return self.levels[slices]

    def __setitem__(self, item, slices):
        raise NotImplemented('Setting levels not allowed')

    def __iter__(self):
        for level_index, level in enumerate(self.levels):
            for sibling_index, node in enumerate(level):
                yield self[level_index][sibling_index]

    def __str__(self):
        return '\n'.join(','.join(map(str, nodes)) for nodes in self.levels)

    def __len__(self):
        return sum(len(level) for level in self.levels)

    @property
    def height(self):
        return len(self.levels)

    @property
    def depth(self):
        return len(self.levels)

    @property
    def root(self):
        try:
            return self.levels[0][0]
        except IndexError:
            raise ITreeError('This ITree has no root')

    def set_root(self, data):
        # suppose root node exists and we change the value
        try:
            self.get_node(0, 0).data = data
        except IndexError:
            # node doesn't exist so we create it
            # the parent of root is outside the matrix
            # using -1 here lets us use append_child as if (-1, -1) existed
            self.append_child(data, -1, -1)

    def append_child(self, data, parent_row, parent_column):
        """append child to row that contains its siblings and cousins"""
        child_row = parent_row + 1
        try:
            child_level = self.levels[child_row]
        # the level doesn't exist so we need to create it
        # this is an only child (no cousins either)
        except IndexError:
            self.levels.append(ITreeRow(child_row, self))
            child_level = self.levels[child_row]
        child = child_level.append_child(data, parent_column)
        return child

    def remove_node(self, row, column):
        node = self.get_node(row, column)
        if len(node.children_indices) != 0:
            raise ITreeError("cannot delete a node which has children")
        parent_row = row - 1
        # if this isn't the root node, we need to delete
        # this child from parent nodes
        if parent_row >= 0:
            parent_level = self.levels[parent_row]
            parent_level.remove_child(parent_row, column)
        # remove this node from the tree
        level = self.levels[row]
        removed = level.pop(column)
        if len(level) == 0:
            self.levels.pop(row)
        return removed

    def get_node(self, row, column):
        return self.levels[row].get_node(column)

    def add_row(self):
        self.levels.append(ITreeRow(self.height, self))
