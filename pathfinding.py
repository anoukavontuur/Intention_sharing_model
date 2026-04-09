import heapq

class GridGraph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.all_nodes = [(x, y) for x in range(width) for y in range(height)]

    def neighbors(self, node, current_time):
        directions = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)] 
        result = []
        
        for dx, dy in directions:
            neighbour = (node[0] + dx, node[1] + dy)
            if neighbour in self.all_nodes:
                result.append((neighbour, current_time + 1)) #result = [((x, y), t), ...]
        return result

class PriorityQueue:
    def __init__(self):
        self.elements = [] # Make a queue to hold elements as (priority, item) pairs

    def empty(self) -> bool:
        return not self.elements # Check if the queue is empty
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item)) # Add an element to the end of the queue
    
    def get(self):
        return heapq.heappop(self.elements)[1] # Remove and return the element with highest priority

def heuristic(a, b):
    """Spatial heuristic: Manhattan distance between two 2D positions."""
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def spacetime_A_star_search(graph, start_state, goal_xy, reservation_table=None):
    if reservation_table is None:
        reservation_table = {}
    
    frontier = PriorityQueue()
    frontier.put(start_state, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start_state] = None
    cost_so_far[start_state] = 0
    
    goal_found = None 
    
    while not frontier.empty():
        current_state = frontier.get()  # current_state = ((x, y), t)
        current_xy = current_state[0]   #(x, y)
        current_t = current_state[1]    #t
        
        # Check if goal is reached (any time is acceptable)
        if current_xy == goal_xy:
            goal_found = current_state
            break
        
        # Generate space-time successors
        for next_state in graph.neighbors(current_xy, current_t):
            # next_state = ((next_x, next_y), next_t)
           
            # Check if this state is reserved by another agent
            if next_state in reservation_table:
                continue
           
            new_cost = cost_so_far[current_state] + 1
            
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + heuristic(next_state[0], goal_xy)
                frontier.put(next_state, priority)
                came_from[next_state] = current_state
    
    if goal_found is None:
        return {}
    
    return came_from, goal_found

def reconstruct_path(came_from, start, goal_state):
    # came_from maps ((x, y), t) -> ((prev_x, prev_y), prev_t)
    # start is ((start_x, start_y), start_t)
    # goal_state is ((goal_x, goal_y), goal_t)
    # return a list of ((x, y), t) from start to goal

    current = goal_state 
    path = []
    
    if goal_state not in came_from:
        return []
    
    while current != start:
        path.append(current)
        current = came_from[current]
    
    path.append(start)
    path.reverse()
    plan = {t: (x, y) for (x, y), t in path}
    return plan





