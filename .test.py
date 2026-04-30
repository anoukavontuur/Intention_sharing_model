path1 = [((7, 2), 2.0, 0, 1), ((7, 2), 2.0, 0, 0), ((6, 2), 3.0, 7, 1), ((4, 3), 4.0, 0, 2), ((3, 5), 5.0, 1, 2), ((2, 7), 6.0, 0, 2), ((0, 8), 7.0, 7, 2)]
path2 = [((7, 2), 2.0, 0, 1)]

def visualization_path(path):
    if len(path) <= 1:
        return path
    
 
    edges = [(path[i-1], path[i]) for i in range(1, len(path))]

    all_directions = [
    (-1, 1), (0, 1), (1, 1), (1, 0),
    (1, -1), (0, -1), (-1, -1), (-1, 0)
    ]

    full_path = []

    for edge in edges:
        full_path.append(edge[0])
        x, y = edge[0][0]
        h1 = edge[0][2]
        t2 = edge[1][1]
        v2 = edge[1][3]
       
        last_edge = edge[1]

        for _ in range(1, v2):
            dx, dy = all_directions[h1]
            in_between_step = ((x + dx, y + dy), t2, h1, v2)
            full_path.append(in_between_step)
            x += dx
            y += dy
    
    full_path.append(last_edge)
    return full_path

full_path = visualization_path(path2)
print(path2)
print(full_path)
