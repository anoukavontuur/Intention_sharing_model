import heapq

class GridGraph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.all_nodes = [(x, y) for x in range(width) for y in range(height)]
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)
    
    def in_bounds(self, id) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, node):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        result = []
        for dx, dy in directions:
            neighbour = (node[0] + dx, node[1] + dy)
            if neighbour in self.all_nodes:
                result.append(neighbour)
        return result
   

class PriorityQueue:
    def __init__(self):
        self.elements= []

    def empty(self) -> bool:
        return not self.elements # Check if the queue is empty
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item)) # Add an element to the end of the queue
    
    def get(self):
        return heapq.heappop(self.elements)[1] # Remove and return an element from the front of the queue

def heuristic(a, b) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def A_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
                
    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    if goal not in came_from: # no path was found
        return None
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path





