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

def has_conflict(path1, path2):
    edges1 = [(path1[i-1], path1[i]) for i in range(1, len(path1))]
    edges2 = [(path2[i-1], path2[i]) for i in range(1, len(path2))]
    print("Edges:")
    print(edges1)
    print(edges2)

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
