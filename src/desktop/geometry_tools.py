def triangle_contains_point(p1, p2, p3, x, y) -> bool:
    s1 = (p1[0] - x) * (p2[1] - p1[1]) - (p2[0] - p1[0]) * (p1[1] - y)
    s2 = (p2[0] - x) * (p3[1] - p2[1]) - (p3[0] - p2[0]) * (p2[1] - y)
    s3 = (p3[0] - x) * (p1[1] - p3[1]) - (p1[0] - p3[0]) * (p3[1] - y)
    return (sign(s1) == sign(s2)) and (sign(s2) == sign(s3))


def rect_contains_point(origin, right_top, left_bottom, x, y) -> bool:
    return (origin[0] <= x) and (right_top[0] >= x) and (origin[1] <= y) and (left_bottom[1] >= y)


def sign(value) -> int:
    if value > 0:
        return 1
    elif value < 0:
        return -1
    return 0
