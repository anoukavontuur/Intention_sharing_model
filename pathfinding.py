import heapq

class GridGraph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.all_nodes = [(x, y) for x in range(width) for y in range(height)]

    def neighbors(self, node, current_time, goal_xy):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)] 
        result = []
        
        for dx, dy in directions:
            if node == goal_xy:
                continue

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

def spacetime_A_star_search(graph, start_state, goal_xy, max_goals=5, reservation_table=None):
    
    if reservation_table is None:
        reservation_table = {}
    
    frontier = PriorityQueue()
    frontier.put(start_state, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start_state] = None
    cost_so_far[start_state] = 0
    
    goal_states = []
    
    while not frontier.empty():
        current_state = frontier.get()  # current_state = ((x, y), t)
        current_xy = current_state[0]   #(x, y)
        current_t = current_state[1]    #t
        
        # Check if goal is reached (any time is acceptable)
        if current_xy == goal_xy:
            goal_states.append(current_state)
            if len(goal_states) >= max_goals:   
                break
        
        # Generate space-time successors
        for next_state in graph.neighbors(current_xy, current_t, goal_xy):
            # next_state = ((next_x, next_y), next_t)
           
            # Check if this state is reserved by another agent
            if next_state in reservation_table:
                continue

            weight = graph.width + graph.height - heuristic(next_state[0], goal_xy) 
            new_cost = cost_so_far[current_state] + weight
            
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + heuristic(next_state[0], goal_xy)
                frontier.put(next_state, priority)
                came_from[next_state] = current_state
    
    if not goal_states:
        return {}, [], {}
    
    return came_from, goal_states, cost_so_far


def reconstruct_k_paths(came_from, start, goal_states, cost_so_far, k=5):
    # came_from maps ((x, y), t) -> ((prev_x, prev_y), prev_t)
    # start is ((start_x, start_y), start_t)
    # goal_states is a list of ((goal_x, goal_y), goal_t)

    goal_states = sorted(goal_states, key=lambda s: cost_so_far[s])

    paths = []
    plans = []

    for goal_state in goal_states[:k]:  # Consider only the top k goal states
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

        paths.append(path)
        plans.append(plan)

    return paths, plans









