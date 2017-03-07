#!/usr/bin/env python3
# pylint: disable=invalid-name, missing-docstring


def max_slice(A, w=3):
    sums = []
    for i in range(len(A)):
        end = min(i+w, len(A))
        sums.append(sum(A[i:end]))

    mi = sums.index(max(sums))
    end = min(mi+w, len(A))
    return A[mi:end]

if __name__ == '__main__':
    print(max_slice([2, 3, 4, 2, 6, 2, 5, 1]))
