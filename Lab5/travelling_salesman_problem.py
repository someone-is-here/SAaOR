import itertools
import math


def solve(distance):
    n = len(distance)

    if n != len(distance[0]):
        raise Exception("Matrix must be square")

    OPT = {}

    for i in range(n):
        variants = list(itertools.permutations(range(n), i+1))

        for s in variants:
            for k in range(n):
                if i == 0:
                    OPT[(s, k)] = distance[s[0]][k]
                else:
                    s_without_k = list(s)
                    k = s_without_k.pop()
                    t = s_without_k[-1]
                    s_without_k = tuple(s_without_k)

                    temp = OPT[(s_without_k, t)] + distance[t][k]

                    if OPT.__contains__((s, k)) and OPT[(s, k)] > temp:
                        OPT[(s, k)] = temp
                    else:
                        OPT[(s, k)] = temp

    values = [i for i in range(n)]
    values.remove(0)

    variants = list(itertools.permutations(values, len(values)))
    min_distance = math.inf

    for i in range(n):
        for s in variants:
            if i != 0:
                p = s[-1]
                temp = distance[0][s[0]] + OPT[(s, p)] + distance[p][0]

                if temp < min_distance:
                    min_distance = temp
                    s_res = (0,) + s

    return min_distance, s_res
