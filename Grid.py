class GridGraph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.all_nodes = [(x, y) for x in range(width) for y in range(height)]

    def neighbors(self, node, current_time, goal_xy):
        directions = [(0, 0),(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)] 
        result = []
        
        for dx, dy in directions:
            if node == goal_xy:
                continue

            neighbour = (node[0] + dx, node[1] + dy)
            if neighbour in self.all_nodes:
                result.append((neighbour, current_time + 1)) #result = [((x, y), t), ...]
                
        return result

