path1 = [(0, 0), (1, 1)]
edge_reservations1 = [(path1[i-1], path1[i]) for i in range(1, len(path1))]
print(edge_reservations1)

start = (1, 1)
destination = (0, 0)
edge = (start, destination)

for reserved_edge in edge_reservations1:
    x = reserved_edge[0]
    y = reserved_edge[1]
    u = edge[0]
    v = edge[1]
    if (u[0] + v[0] == x[0] + y[0] and u[1] + v[1] == x[1] + y[1]):
        print("crossing")



