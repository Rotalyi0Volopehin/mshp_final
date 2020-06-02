def triangle_contains_point(p_1, p_2, p_3, x, y) -> bool:
    """Функция, проверяющая входит ли данная точка в данный треуголник"""
    s_1 = (p_1[0] - x) * (p_2[1] - p_1[1]) - (p_2[0] - p_1[0]) * (p_1[1] - y)
    s_2 = (p_2[0] - x) * (p_3[1] - p_2[1]) - (p_3[0] - p_2[0]) * (p_2[1] - y)
    s_3 = (p_3[0] - x) * (p_1[1] - p_3[1]) - (p_1[0] - p_3[0]) * (p_3[1] - y)
    return (sign(s_1) == sign(s_2)) and (sign(s_2) == sign(s_3))


def rect_contains_point(origin, right_top, left_bottom, x, y) -> bool:
    """Функция, проверяющая входит ли данная точка в данный прямоугольник"""
    return (origin[0] <= x) and (right_top[0] >= x) and (origin[1] <= y) and (left_bottom[1] >= y)


def sign(value) -> int:
    """Возвращает значение в зависимости от знака входного параметра"""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0
