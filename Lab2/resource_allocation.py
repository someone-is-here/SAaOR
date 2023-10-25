def resource_allocation_problem(matrix_a):
    # people
    p = len(matrix_a)
    # resources
    q = len(matrix_a[0]) - 1

    resources_amount = [i for i in range(q + 1)]

    print(f"People: {p}")
    print(f"Resources: {q}, variants: {resources_amount}")

    matrix_b = []
    matrix_c = []

    # calculation of matrix_b and matrix_c
    for i_p in range(1, p+1):
        matrix_b.append([0] * (p+1))
        matrix_c.append([0] * (p+1))
        for i_q in range(q+1):
            if i_p == 1:
                matrix_b[i_p - 1][i_q] = matrix_a[i_p - 1][i_q]
                matrix_c[i_p - 1][i_q] = i_q
            else:
                matrix_b[i_p - 1][i_q] = 0
                index = 0
                for i in range(i_q + 1):
                    num = matrix_a[i_p - 1][i] + matrix_b[i_p - 2][i_q - i]
                    if num > matrix_b[i_p - 1][i_q]:
                        matrix_b[i_p - 1][i_q] = num
                        index = i

                matrix_c[i_p - 1][i_q] = index

    print("Matrix b result: ", matrix_b)
    print("Matrix c result: ", matrix_c)

    print()
    print(f"Maximum profit: {matrix_b[p-1][q]}")

    # reverse stroke to get agent-resource distribution
    while p > 0:
        print(f"Agent {p} get {matrix_c[p - 1][q]} resource!")
        q = q - matrix_c[p - 1][q]
        p = p-1
