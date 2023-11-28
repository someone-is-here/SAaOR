def solve(volumes, price, full_volume):
    """
    :param volumes: вес предметов
    :param price: стоимость предметов
    :param full_volume: объем рюкзака
    :return: максимальная стоимость, вес рюкзака, выбранные предметы
    """

    if len(volumes) != len(price):
        raise Exception("Invalid input! Volumes and price must be same dimension")

    n = len(volumes)

    x = {}
    OPT = {}

    """Прямой ход алгоритма"""
    for i in range(n):
        for k in range(full_volume):
            if i == 0:
                if k >= volumes[i]:
                    OPT[(i, k)] = price[i]
                    x[(i, k)] = 1
                else:
                    OPT[(i, k)] = 0
                    x[(i, k)] = 0
            else:
                if k >= volumes[i] and \
                        OPT[(i - 1, k)] < price[i] + OPT[(i - 1, k - volumes[i])]:
                    x[(i, k)] = 1
                    OPT[(i, k)] = price[i] + OPT[(i - 1, k - volumes[i])]
                else:
                    x[(i, k)] = 0
                    OPT[(i, k)] = OPT[(i - 1), k]

    selected_objects = []
    temp = x[(n - 1, full_volume - 1)]
    total_weight = 0
    temp_volume = full_volume - 1

    """Обратный ход алгоритма"""
    for i in range(n - 1, 0, -1):
        if temp == 1:
            selected_objects.append(i + 1)
            total_weight += volumes[i]
            temp_volume -= volumes[i]

        temp = x[(i - 1, temp_volume)]

    return OPT[(n - 1, full_volume - 1)], total_weight, sorted(selected_objects)
