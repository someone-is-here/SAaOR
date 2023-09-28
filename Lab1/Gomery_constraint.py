import math
import numpy
from simplex import simplex_method, get_inverse_matrix, get_base_matrix


def get_frac(value):
    return value - math.floor(value)


"""
Алгоритм решения задачи целочисленного линейного программирования
методом отсекающего ограничения Гомери
"""
def method_Gomery_constraint(matrix_a, vector_b, vector_c):
    x_optional, b_basis, _, _ = simplex_method(vector_c, matrix_a, vector_b)

    for i in range(len(x_optional)):
        if abs(x_optional[i] - round(x_optional[i])) < 0.00001:
            x_optional[i] = round(x_optional[i])

    b_basis = sorted(b_basis)

    x_fractional = math.inf
    i_frac = 1
    print("X optimal: ", x_optional)
    print("Basis vector: ", b_basis)

    for i in b_basis:
        if int(x_optional[i - 1]) != x_optional[i - 1]:
            x_fractional = x_optional[i - 1]
            break
        i_frac += 1

    if x_fractional == math.inf:
        return x_optional, b_basis

    print("continue", x_fractional, i_frac)

    a_basis_matrix = get_base_matrix(a_matrix=matrix_a, b_basis_plan=b_basis)
    b_not_basis = [i+1 for i in range(len(x_optional)) if i + 1 not in b_basis]
    a_not_basis_matrix = get_base_matrix(a_matrix=matrix_a, b_basis_plan=b_not_basis)
    print(a_basis_matrix, a_not_basis_matrix)

    _, a_basis_inverse = get_inverse_matrix(matrix_a, b_basis)
    print("Base inverse matrix: ", a_basis_inverse)
    l_matrix = numpy.dot(a_basis_inverse, a_not_basis_matrix)
    print("L matrix: ", l_matrix)
    l_matrix = l_matrix[i_frac-1]
    print("Selected row: ", l_matrix)

    new_restriction = [0]*len(x_optional)

    i_l = 0
    for i in b_not_basis:
        new_restriction[i-1] = get_frac(l_matrix[i_l])
        i_l += 1

    new_restriction.append(-1)
    print("Matrix_A: ", matrix_a)
    for i in range(len(matrix_a)):
        matrix_a[i].append(0)

    print("Matrix_A: ", matrix_a)
    print(new_restriction)
    matrix_a.append(new_restriction)

    vector_b.append(get_frac(x_fractional))
    print(matrix_a, vector_b)
    print('---------------------------------')
    return method_Gomery_constraint(matrix_a, vector_b, vector_c)




