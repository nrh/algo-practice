#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring, consider-using-enumerate


def sumstozero(A):
    '''determine whether an array has three elements that sum to zero'''
    A = sorted(A)

    for i in range(len(A)):
        for j in range(1, len(A)):
            s = sum([A[i], A[j]])

            # since we're sorted we can skip out early here
            if s + A[j + 1] > 0:
                return False

            lookingfor = 0 - s

            try:
                if A.index(lookingfor):
                    return True, [A[i], A[j], A[A.index(lookingfor)]]

            except ValueError:
                pass

    return False


if __name__ == '__main__':
    print(sumstozero([1, 2, 3, 4, 5, -1, -2]))
    print(sumstozero([1, 2, 3, -1, -2, 0]))
    print(sumstozero([1, 2, 3, 4, 5, 5]))
