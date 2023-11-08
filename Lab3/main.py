import longest_path_problem


if __name__ == '__main__':
    longest_path_problem.solve(
        ['s', 'c', 'a', 'b', 'd', 't'],
        {
            ('s', 'a'): 1,
            ('s', 'c'): 2,
            ('c', 'a'): 1,
            ('a', 'b'): 3,
            ('c', 'd'): 2,
            ('b', 'd'): 3,
            ('d', 't'): 1,
            ('b', 't'): 1
        }
    )
