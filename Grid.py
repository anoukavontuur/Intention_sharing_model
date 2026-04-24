class GridGraph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.all_nodes = [(x, y) for x in range(width) for y in range(height)]

    def neighbors(self, node, current_time, goal_xy, heading):
        stay = (0, 0)

        all_directions = [
            (-1, 1), (0, 1), (1, 1), (1, 0),
            (1, -1), (0, -1), (-1, -1), (-1, 0)
        ]

        result = []

        # bepaal indices voor links, rechtdoor, rechts
        indices = [
            (heading - 1) % 8,  # links
            heading,            # rechtdoor
            (heading + 1) % 8   # rechts
        ]

        possible_directions = [stay] + [all_directions[i] for i in indices]

        for dx, dy in possible_directions:
            if node == goal_xy:
                continue

            new_x = node[0] + dx
            new_y = node[1] + dy
            neighbour = (new_x, new_y)

            if neighbour in self.all_nodes:
                # nieuwe heading bepalen
                if (dx, dy) == stay:
                    new_heading = heading
                else:
                    new_heading = all_directions.index((dx, dy))

                result.append(((new_x, new_y), current_time + 1, new_heading))

        return result

