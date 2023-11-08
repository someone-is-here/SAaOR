import math
from collections import deque, defaultdict


def solve(points, arc_weight):
    """
    Решение задачи поиска в направленном графе без контура
    наидлиннейшего пути
    :param points: вершины графа G
    :param arc_weight: dict, где key: дуга графа; value: вес дуги key
    """
    graph = prepare_graph(arc_weight)
    sorted_list = topological_sorting(points, graph)
    print(f'Топологически отсортированные вершины {sorted_list}')

    if sorted_list.index('s') > sorted_list.index('t'):
        print('В графе отсутствует s-t путь!')
        return

    s_t_path = sorted_list[sorted_list.index('s'):sorted_list.index('t') + 1]

    OPT_vector = {}
    pre_last_vector = {}

    for point in s_t_path:
        OPT_vector[point] = 0
        if point == 's':
            pre_last_vector[point] = point
        else:
            in_arcs = get_in_arc(point, arc_weight)
            if len(in_arcs) == 0:
                OPT_vector[point] = -math.inf
                pre_last_vector[point] = None
                continue

            for point_in in in_arcs:
                if not OPT_vector.__contains__(point_in):
                    max_value = -math.inf
                else:
                    max_value = OPT_vector[point_in] + arc_weight[(point_in, point)]

                if max_value > OPT_vector[point]:
                    OPT_vector[point] = max_value
                    pre_last_vector[point] = point_in

    print(f'Наидлиннейший s-t путь {OPT_vector}')
    print(f'''Maксимальный вес на s-t пути: {OPT_vector['t']}''')
    print(f'Вершины наидлиннейшего s-t пути: {get_max_path(pre_last_vector)}')


def get_max_path(pre_last_vector):
    """
    Получение наидлиннейшего s-t пути
    """

    list_with_points = deque()
    list_with_points.appendleft('t')
    current_point = pre_last_vector['t']

    while not current_point == 's':
        list_with_points.appendleft(current_point)
        current_point = pre_last_vector[current_point]

    list_with_points.appendleft(pre_last_vector[current_point])

    return list_with_points


def get_in_arc(point, arc_weight):
    """
    Получение входящих дуг в вершину point
    """
    result = []
    for i in arc_weight.keys():
        if i[1] == point:
            result.append(i[0])

    return result


def prepare_graph(arc_weight):
    """
    Подготовка данных в нужный формат
    :return dict в формате
        :key - вершина
        :value - вершины, в которые можно попасть из key
    """
    graph = defaultdict(list)

    for i in arc_weight.keys():
        graph[i[0]].append(i[1])

    return graph


def topological_sort_util(v, visited, stack, graph):
    visited[v] = True

    for i in graph[v]:
        if not visited[i]:
            topological_sort_util(i, visited, stack, graph)

    stack.insert(0, v)


def topological_sorting(points, graph):
    """
    Топологическая сортировка графа G
    :param points: вершины графа G
    :param graph: dict, где key: вершина графа; value: в какие вершины можем попасть из key
    :return: list с топологически отсортированными вершинами
    """

    visited = {i: False for i in points}
    stack = []

    for i in points:
        if not visited[i]:
            topological_sort_util(i, visited, stack, graph)

    return stack
