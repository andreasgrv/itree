"""basic itree unittests"""
import pytest
from itree import ITree, ITreeError, utils

def test_len():
    tree = ITree()
    tree.append_child('dog')
    tree.root.append_child('cat')
    tree.root.append_child('mouse')
    assert(len(tree) == 3)

def test_root():
    tree = ITree()
    tree.append_child('dog')
    assert(tree.root.data == 'dog')

def test_children():
    tree = ITree()
    tree.append_child('dog')
    tree.root.append_child('cat')
    tree.root.append_child('mouse')
    assert([each.data for each in tree.root.children] == ['cat', 'mouse'])

def test_append_child():
    tree = ITree()
    tree.append_child('dog')
    cat = tree.root.append_child('cat')
    mouse = tree.root.append_child('mouse')
    cat.append_child('kitten')
    mouse.append_child('mouseling')
    kitten2 = cat.append_child('kitten2')
    assert(kitten2.sibling_index == 1)

def test_indexing_children():
    tree = ITree()
    tree.append_child('dog')
    tree.root.append_child('cat')
    tree.root.append_child('mouse')
    should_be_cat_node = tree[1, 0]
    assert should_be_cat_node.data == 'cat'
    should_be_cat_node.append_child('kitten')
    should_be_kitten_node = tree[2, 0]
    assert should_be_kitten_node.data == 'kitten'

def test_indexing_imaginary_children():
    tree = ITree()
    tree.append_child('dog')
    tree.root.append_child('cat')
    mouse = tree.root.append_child('mouse')
    with pytest.raises(ITreeError) as ex:
        shouldnt_be_cat_node = mouse[66, 0]
    with pytest.raises(ITreeError) as ex:
        shouldnt_be_cat_node = mouse(66, 0)
    with pytest.raises(ITreeError) as ex:
        shouldnt_be_cat_node = mouse(0)
    with pytest.raises(ITreeError) as ex:
        shouldnt_be_cat_node = mouse[0]
    assert(mouse(1, 0, 3, 4).data == 'cat')

def test_indexing_root_imaginary_children():
    tree = ITree()
    tree.append_child('dog')
    tree.root.append_child('cat')
    tree.root.append_child('mouse')
    with pytest.raises(ITreeError) as ex:
        shouldnt_be_cat_node = tree[66, 0]
    with pytest.raises(ITreeError) as ex:
        shouldnt_be_cat_node = tree(66, 0)
    with pytest.raises(ITreeError) as ex:
        shouldnt_be_cat_node = tree(0)
    with pytest.raises(ITreeError) as ex:
        shouldnt_be_cat_node = tree[0]
    assert(tree(1, 0, 3, 4).data == 'cat')

def test_deleting_non_leaf():
    tree = ITree()
    tree.append_child('dog')
    with pytest.raises(ITreeError) as e:
        tree.set_root('dog')
        tree.root.append_child('cat')
        tree.root.delete()
        assert(len(tree) == 1)

def test_deleting_leaf():
    tree = ITree()
    tree.append_child('dog')
    tree.root.append_child('cat')
    should_be_cat_node = tree[1, 0]
    should_be_cat_node.delete()
    assert(len(tree) == 1)
    with pytest.raises(ITreeError) as e:
        cat = tree[1, 0]

def test_deleting_root():
    tree = ITree()
    tree.append_child('dog')
    tree[0, 0].delete()
    assert(len(tree) == 0)
    assert(tree.height == 0)
    tree.set_root('b')
    assert(len(tree) == 1)

def test_tree_builtin_traversal():
    tree = ITree()
    tree.append_child('dog')
    tree.root.append_child('cat')
    tree.root.append_child('mouse')
    data = ['dog', 'cat', 'mouse']
    traversal_data = [node.data for node in tree]
    assert(data == traversal_data)

def test_to_nested_list():
    tree = ITree()
    tree.append_child('dog')
    tree.root.append_child('cat')
    tree.root.append_child('mouse')
    nested_list = tree.to_nested_list()
    assert(nested_list == ['dog', ['cat', 'mouse']])

def test_large_random_nested_list():
    multi_list = [1, utils.generate_nested_list(400000, 100)]
    tree = ITree.from_nested_list(multi_list)
    list_from_tree = tree.to_nested_list()
    assert(multi_list == list_from_tree)
