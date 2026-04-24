def _orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def _segments_cross(a, b, c, d):
    if a == c or a == d or b == c or b == d:
        return False

    o1 = _orientation(a, b, c)
    o2 = _orientation(a, b, d)
    o3 = _orientation(c, d, a)
    o4 = _orientation(c, d, b)

    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)

def time_space_path(path):
    return [(step[0], step[1]) for step in path]

def has_conflict(path1, path2):
    path1 = time_space_path(path1)
    path2 = time_space_path(path2)

    edges1 = [(path1[i-1], path1[i]) for i in range(1, len(path1))]
    edges2 = [(path2[i-1], path2[i]) for i in range(1, len(path2))]

    #Vertex conflict
    for step in path1:
        if step in path2:
            return True

    #Edge conflict
    for edge1 in edges1:
        for edge2 in edges2:
            if _segments_cross(edge1[0][0], edge1[1][0], edge2[0][0], edge2[1][0]) and edge1[0][1] == edge2[0][1]: 
                return True

    #Following conflict
    for edge1 in edges1:
        for edge2 in edges2:
            if (edge1[0][0] == edge2[1][0] or edge1[1][0] == edge2[0][0]) and edge1[0][1] == edge2[0][1]:
                return True

    return False

def has_conflict(path1, path2):
    # edges: ((pos1, t1, h1), (pos2, t2, h2))
    edges1 = [(path1[i-1], path1[i]) for i in range(1, len(path1))]
    edges2 = [(path2[i-1], path2[i]) for i in range(1, len(path2))]

    # -----------------
    # Vertex conflict
    # zelfde positie op zelfde tijd (heading negeren)
    # -----------------
    positions_times_2 = {(s[0], s[1]) for s in path2}

    for s1 in path1:
        if (s1[0], s1[1]) in positions_times_2:
            return True

    # -----------------
    # Edge conflict (kruisen)
    # -----------------
    for e1 in edges1:
        for e2 in edges2:
            pos1_a, t1_a = e1[0][0], e1[0][1]
            pos1_b, t1_b = e1[1][0], e1[1][1]

            pos2_a, t2_a = e2[0][0], e2[0][1]
            pos2_b, t2_b = e2[1][0], e2[1][1]

            if t1_a == t2_a:  # zelfde tijdstap
                if _segments_cross(pos1_a, pos1_b, pos2_a, pos2_b):
                    return True

    # -----------------
    # Swap / following conflict
    # -----------------
    for e1 in edges1:
        for e2 in edges2:
            pos1_a, t1_a = e1[0][0], e1[0][1]
            pos1_b = e1[1][0]

            pos2_a, t2_a = e2[0][0], e2[0][1]
            pos2_b = e2[1][0]

            if t1_a == t2_a:
                # swap: A→B en B→A
                if pos1_a == pos2_b and pos1_b == pos2_a:
                    return True

                # following (optioneel, afhankelijk van je definitie)
                if pos1_b == pos2_a:
                    return True

    return False