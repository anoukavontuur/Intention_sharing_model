# from conflict_detection import has_conflict

# path1 = [((6, 3), 3.0), ((6, 4), 4.0), ((5, 5), 5.0), ((6, 6), 6.0), ((6, 7), 7.0), ((6, 8), 8.0)]
# path2 = [((3, 3), 3.0), ((4, 4), 4.0), ((5, 5), 5.0), ((6, 6), 6.0), ((7, 7), 7.0), ((8, 8), 8.0)]

# if has_conflict(path1, path2):
#     print("Conflict detected!")
# else:
#     print("No conflict detected.")

class GridGraph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.all_nodes = [(x, y) for x in range(width) for y in range(height)]

    def neighbors(self, node, current_time, goal_xy, heading, velocity):
        all_directions = [
            (-1, 1), (0, 1), (1, 1), (1, 0),
            (1, -1), (0, -1), (-1, -1), (-1, 0)
        ]

        v_min, v_max = 0, 3  # example limits

        result = []

        # possible heading changes: left, straight, right
        heading_indices = [
            (heading - 1) % 8,
            heading,
            (heading + 1) % 8
        ]

        # possible velocity changes
        for dv in [-1, 0, 1]:
            if node == goal_xy:
                continue

            v_new = velocity + dv
            if v_new < v_min or v_new > v_max:
                continue

            # allow standing still
            if v_new == 0:
                result.append((node, current_time + 1, heading, 0))
                continue

            dx, dy = all_directions[heading]
            base_directions = (dx*(v_new-1), dy*(v_new-1))

            for h in heading_indices:
                x, y = node
                base_x, base_y = base_directions
                dx, dy = all_directions[h]

                new_pos = (x + base_x + dx, y + base_y + dy)
                if new_pos in self.all_nodes:
                    result.append((new_pos, current_time + 1, h, v_new))

        return result


Testgraph = GridGraph(6, 6)
start_node = (2, 2)
current_time = 2
goal_xy = (3, 3)
heading = 2
velocity = 2

print(Testgraph.neighbors(start_node, current_time, goal_xy, heading, velocity))