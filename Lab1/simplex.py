import numpy as np


def multiply_matrix_on_vector(inverse_matrix, vector):
    result_matrix = []

    for j in range(len(inverse_matrix)):
        sum_of_row = 0
        for i in range(len(inverse_matrix)):
            sum_of_row += inverse_matrix[j][i] * vector[i]

        result_matrix.append(sum_of_row)

    return result_matrix


def multiply_vector_on_matrix(vector, matrix):
    result_vector = []
    for i in range(len(matrix[0])):
        sum_of_col = 0

        for j in range(len(vector)):
            sum_of_col += matrix[j][i]*vector[j]

        result_vector.append(sum_of_col)

    return result_vector


def multiply_vector_on_digit(vector, digit):
    for i in range(len(vector)):
        vector[i] *= (-1 / digit)


def create_q_matrix(vector, index):
    identity_matrix = []

    for i in range(len(vector)):
        row = []

        for j in range(len(vector)):
            if j == index:
                row.append(vector[i])
            elif i == j:
                row.append(1)
            else:
                row.append(0)

        identity_matrix.append(row)

    return identity_matrix


def multiply_matrix_on_q_matrix(inverse_matrix, q_matrix, index):
    result_matrix = []

    for i in range(len(inverse_matrix)):
        row = []
        for j in range(len(inverse_matrix)):
            if i != index:
                row.append(inverse_matrix[i][j] * q_matrix[i][i] + inverse_matrix[index][j] * q_matrix[i][index])
            else:
                row.append(inverse_matrix[index][j] * q_matrix[i][index])

        result_matrix.append(row)

    return result_matrix


def calculate_inverse_matrix(matrix, inverse_matrix, x_vector, i):
    result_vector = multiply_matrix_on_vector(inverse_matrix, x_vector)

    # print(inverse_matrix, x_vector)

    if result_vector[i - 1] == 0:
        raise Exception("Matrix is irreversible")

    vector = result_vector.copy()
    vector[i - 1] = -1

    multiply_vector_on_digit(vector, result_vector[i - 1])

    q_matrix = create_q_matrix(vector, i - 1)

    return multiply_matrix_on_q_matrix(inverse_matrix, q_matrix, i - 1)


def get_base_matrix(a_matrix, b_basis_plan):
    a_base_matrix = []

    for j in range(len(a_matrix)):
        arr = []
        for i in b_basis_plan:
            arr.append(a_matrix[j][i - 1])
        a_base_matrix.append(arr)

    return a_base_matrix


def get_inverse_matrix(a_matrix, b_basis_plan):
    a_base_matrix = get_base_matrix(a_matrix, b_basis_plan)

    return a_base_matrix, np.linalg.inv(a_base_matrix)


def main_phase_of_simplex_method(c_vector, a_matrix, a_base_matrix, inverse_matrix, x_basis_plan, b_basis_plan, b_basis_result):
    # print(a_matrix, inverse_matrix)
    c_vector_base = []
    for i in b_basis_plan:
        c_vector_base.append(c_vector[i-1])

    # print("Vector_base ", c_vector_base)
    potential_vector = multiply_vector_on_matrix(c_vector_base, inverse_matrix)
    # print("Potential vector ", potential_vector)

    mark_vector = []
    help_vector = multiply_vector_on_matrix(potential_vector, a_matrix)
    # print("Help vector ", help_vector)
    for i in range(len(help_vector)):
        mark_vector.append(help_vector[i] - c_vector[i])
    # print("Mark vector ", mark_vector)
    j = check_is_optimal(mark_vector)
    # print("J", j)
    if j == len(mark_vector):
        # print("Plan is optimal", x_basis_plan)
        return x_basis_plan, b_basis_result

    a_j = []
    for i in range(len(a_matrix)):
        a_j.append(a_matrix[i][j-1])

    z_vector = multiply_matrix_on_vector(inverse_matrix, a_j)
    # print(z_vector)

    q_vector = []

    for i in range(len(z_vector)):
        if z_vector[i] <= 0:
            q_vector.append(np.Infinity)
        else:
            # print(b_basis_result[i], x_basis_plan)
            q_vector.append(x_basis_plan[b_basis_result[i]-1] / z_vector[i])

    # print("Q_vector: ", q_vector)
    q_0 = min(q_vector)

    if q_0 == np.Infinity:
        raise Exception("The objective functional of the problem is not bounded from above on the set of admissible plans")

    k = q_vector.index(q_0)
    j_k = b_basis_plan[k]
    # print("K: ", k)
    # print("J_k: ", j_k)

    b_basis_result[k] = j
    # print(b_basis_plan)

    # print("X_basis_plan ", x_basis_plan)

    for i in range(len(b_basis_plan)):
        if i != k:
            x_basis_plan[b_basis_result[i]-1] = (x_basis_plan[b_basis_result[i]-1] - q_0*z_vector[i])

    x_basis_plan[j_k - 1] = 0
    x_basis_plan[j - 1] = q_0

    # print(x_basis_plan)

    a_new_base_matrix = get_base_matrix(a_matrix, b_basis_result)
    inverse_new_matrix = calculate_inverse_matrix(a_base_matrix, inverse_matrix, np.array(a_matrix)[:, j-1], k+1)

    return main_phase_of_simplex_method(c_vector, a_matrix, a_new_base_matrix, inverse_new_matrix, x_basis_plan, b_basis_plan, b_basis_result)


def check_is_optimal(mark_vector):
    for i in range(len(mark_vector)):
        if mark_vector[i] < 0:
            return i + 1

    return len(mark_vector)


def simplex_method(c_vector, a_matrix, b_vector):
    for i in range(len(b_vector)):
        if b_vector[i] < 0:
            a_matrix[i] = [(-a_matrix[i][j]) for j in range(len(a_matrix[i]))]
            b_vector[i] = -(b_vector[i])

    c_additional = [0] * len(a_matrix[0]) + [-1] * len(a_matrix)
    # print("c_additional: ", c_additional)

    eye = np.eye(len(c_additional) - len(a_matrix[0]), len(a_matrix))
    a_additional_matrix = np.c_[a_matrix, eye]
    # print("a_additional: ", a_additional_matrix)

    x_initial_plan = [0] * len(a_matrix[0]) + b_vector
    # print("x_initial_basis_plan: ", x_initial_plan)
    b_initial_plan = [len(a_matrix[0]) + i + 1 for i in range(len(a_matrix))]
    # print("b_initial_basis_plan: ", b_initial_plan)

    b_indexes_base_result = b_initial_plan
    a_base_matrix, inverse_matrix = get_inverse_matrix(a_additional_matrix, b_initial_plan)

    x_basis_plan, b_basis_result = \
        main_phase_of_simplex_method(c_additional, a_additional_matrix,
                                     a_base_matrix, inverse_matrix,
                                     x_initial_plan, b_initial_plan,
                                     b_indexes_base_result)

    # print("Result of additional task: ", x_basis_plan, b_basis_result)

    for i in range(len(a_matrix[0]), len(a_additional_matrix[0])):
        if x_basis_plan[i] != 0:
            raise Exception("Problem is infeasible")

    while max(b_basis_result) > len(a_matrix[0]) + 1:
        j_k = max(b_basis_result)
        k = b_basis_result.index(j_k) + 1
        i = j_k - len(a_matrix[0])

        j_vector = [_ for _ in range(1, len(a_matrix[0]) + 1) if _ <= len(a_matrix[0])+1 and _ not in b_basis_result]
        print(j_k, k, i, j_vector)

        a_base_matrix, inverse_matrix = get_inverse_matrix(a_additional_matrix, b_basis_result)

        for i in j_vector:
            l_k = multiply_matrix_on_vector(inverse_matrix,  a_additional_matrix[:, i-1])

            if l_k[k-1] != 0:
                b_basis_result[k-1] = i-1
            else:
                a_additional_matrix = a_additional_matrix[:i-1]
                a_matrix = a_matrix[:i-1]

                b_basis_result.remove(j_k)
                b_vector.remove(b_vector[i-1])

                break

    return x_basis_plan[:len(a_matrix[0])], b_basis_result, a_matrix, b_vector
