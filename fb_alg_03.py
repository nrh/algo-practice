#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, consider-using-enumerate

def start_positions(M, s):
    s_y = None
    r = []
    for s_x in range(len(M)):
        for s_y in range(len(M[s_x])):
            if M[s_x][s_y] == s:
                r.append([s_x, s_y])
    return r

def find_next_pos(M, V, p):
    if len(V) - 1 == len(p):
        return True

    for next_pos in [0, 1], [0, -1], [1, 0], [-1, 0]:
        n_x = next_pos[0] + V[-1][0]
        n_y = next_pos[1] + V[-1][1]
        n_c = p[len(V) - 1]

        # no wrapping
        if n_x < 0 or n_y < 0:
            continue

        # can only use each tile once
        if [n_x, n_y] in V:
            continue

        try:
            if M[n_x][n_y] == n_c:
                V.append([n_x, n_y])
                if find_next_pos(M, V, p):
                    return True
                else:
                    V.pop()
                    continue

        except IndexError:
            continue

    return False



def has_path(M, p):
    V = []
    for start in start_positions(M, p[0]):
        V = [start]
        find_next_pos(M, V, p[1:])
        if len(V) == len(p):
            return V
    return False


if __name__ == '__main__':
    print(has_path([['B', 'B', 'C', 'X'],
                    ['S', 'F', 'C', 'E'],
                    ['A', 'D', 'E', 'E']], 'BCCED'))
    print(has_path([['A', 'B', 'C', 'E'],
                    ['S', 'F', 'C', 'S'],
                    ['A', 'D', 'E', 'E']], 'ABCB'))
    print(has_path([['A', 'B', 'C', 'E'],
                    ['S', 'F', 'C', 'S'],
                    ['A', 'D', 'E', 'E']], 'ABCESCFSADEE'))
