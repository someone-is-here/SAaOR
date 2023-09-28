from Gomery_constraint import method_Gomery_constraint


def lab1_test():
    matrix_a = [[3, 2, 1, 0],
                [-3, 2, 0, 1]]

    vector_c = [0, 1, 0, 0]
    vector_b = [6, 0]

    x_result, b_basis = method_Gomery_constraint(matrix_a, vector_b, vector_c)
    print(x_result, b_basis)


def lab1_test2():
    matrix_a = [[-1, 3, 1, 0],
                [7, 1, 0, 1]]

    vector_c = [7, 9, 0, 0]
    vector_b = [6, 35]

    x_result, b_basis = method_Gomery_constraint(matrix_a, vector_b, vector_c)
    print(x_result, b_basis)