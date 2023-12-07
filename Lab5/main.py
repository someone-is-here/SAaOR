from travelling_salesman_problem import solve


if __name__ == '__main__':
    print(solve(distance=[
        [0, 10, 5, 9, 16, 8],
        [6, 0, 11, 8, 18, 19],
        [7, 13, 0, 3, 4, 14],
        [5, 9, 6, 0, 12, 17],
        [5, 4, 11, 6, 0, 14],
        [17, 7, 12, 13, 16, 0]
    ]))

