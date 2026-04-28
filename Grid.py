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

