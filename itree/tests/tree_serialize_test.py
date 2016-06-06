"""test itree structure"""
import json
import random
from itree import ITree


def generate_nested_list(num_elem, num_sublists):
    assert num_elem > 1
    assert num_sublists >= 0
    l = [0]*(num_elem + 2*num_sublists)
    r = 1
    for i in range(num_sublists):
        while(True):
            open_b, close_b = sorted([random.randrange(r, len(l)-r),
                                      random.randrange(r, len(l)-r)])
            if abs(open_b - close_b) <= r:
                continue
            # we want brackets to be at least r positions apart
            a_brac_before = any(l[open_b-r:open_b+r+1])
            a_brac_after = any(l[close_b-r:close_b+r+1])
            if (not(a_brac_before or a_brac_after)):
                l[open_b] = '['
                l[close_b] = ']'
                break
    num = 0
    for i in range(len(l)):
        if not l[i]:
            l[i] = str(num)
            num += 1
    string_list = '[%s]' % ','.join(l).replace('[,', '[').replace(',]', ']')
    return json.loads(string_list)


def test_tree_from_list():
    multi_list = [1, generate_nested_list(400000, 100)]
    tree = ITree.from_nested_list(multi_list)
    list_from_tree = tree.to_nested_list()
    assert(multi_list == list_from_tree)
