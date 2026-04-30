def _orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on_segment(a, b, c):
    # check of c op segment ab ligt
    return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))


def _segments_intersect(a, b, c, d):
    o1 = _orientation(a, b, c)
    o2 = _orientation(a, b, d)
    o3 = _orientation(c, d, a)
    o4 = _orientation(c, d, b)

    # algemeen geval
    if (o1 * o2 < 0) and (o3 * o4 < 0):
        return True

    # collineair gevallen
    if o1 == 0 and _on_segment(a, b, c): return True
    if o2 == 0 and _on_segment(a, b, d): return True
    if o3 == 0 and _on_segment(c, d, a): return True
    if o4 == 0 and _on_segment(c, d, b): return True

    return False


def _time_overlap(t1a, t1b, t2a, t2b):
    return t1a == t2a and t1b == t2b


def has_conflict(path1, path2):
    # edges: ((pos, t, h), (pos, t, h))
    edges1 = [(path1[i-1], path1[i]) for i in range(1, len(path1))]
    edges2 = [(path2[i-1], path2[i]) for i in range(1, len(path2))]

    # -----------------
    # Vertex conflict (exact zelfde tijd)
    # -----------------
    states2 = {(s[0], s[1]) for s in path2}
    for s1 in path1:
        if (s1[0], s1[1]) in states2:
            return True

    # -----------------
    # Continue edge conflicts
    # -----------------
    for e1 in edges1:
        for e2 in edges2:
            p1a, t1a = e1[0][0], e1[0][1]
            p1b, t1b = e1[1][0], e1[1][1]

            p2a, t2a = e2[0][0], e2[0][1]
            p2b, t2b = e2[1][0], e2[1][1]

            # alleen relevant als tijd overlapt
            if not _time_overlap(t1a, t1b, t2a, t2b):
                continue

            # 1. geometrisch kruisen / raken
            if _segments_intersect(p1a, p1b, p2a, p2b):
                return True

            # 2. swap (tegengestelde richting op zelfde lijn)
            if p1a == p2b and p1b == p2a:
                return True

            # 3. following / inhalen (zelfde lijn, zelfde richting)
            if p1b == p2a or p1a == p2b:
                return True

    return False

