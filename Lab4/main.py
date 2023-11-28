from knapsack_problem import solve

if __name__ == '__main__':
    print(solve(
        volumes=[3, 4, 5, 8, 9],
        price=[1, 6, 4, 7, 6],
        full_volume=13
    ))
