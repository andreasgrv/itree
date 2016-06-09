import json
import random


def generate_nested_list(num_elem, num_sublists):
    """ Generates a nested list from which a new tree may be initialized.
    """
    assert num_elem > 1
    assert num_sublists >= 0
    l = [0] * (num_elem + 2 * num_sublists)
    r = 1
    for i in range(num_sublists):
        while(True):
            open_b, close_b = sorted([random.randrange(r, len(l) - r),
                                      random.randrange(r, len(l) - r)])
            if abs(open_b - close_b) <= r:
                continue
            # we want brackets to be at least r positions apart
            a_brac_before = any(l[open_b - r:open_b + r + 1])
            a_brac_after = any(l[close_b - r:close_b + r + 1])
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
