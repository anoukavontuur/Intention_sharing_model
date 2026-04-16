import heapq

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
    
    goal_state = None
    
    while not frontier.empty():
        current_state = frontier.get()  # current_state = ((x, y), t)
        current_xy = current_state[0]   #(x, y)
        current_t = current_state[1]    #t
        
        # Check if goal is reached (any time is acceptable)
        if current_xy == goal_xy:
            goal_state = current_state
            break

        
        # Generate space-time successors
        for next_state in graph.neighbors(current_xy, current_t, goal_xy):
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
        
    return came_from, goal_state

def spacetime_A_star_path(graph, start_state, goal_xy, reservation_table=None):

    came_from, goal_state = spacetime_A_star_search(
        graph, 
        start_state, 
        goal_xy, 
        reservation_table)
    
    current = goal_state
    path = []
    
    if goal_state not in came_from:
        return []
    
    while current != start_state:
        path.append(current)
        current = came_from[current]
    
    path.append(start_state)
    path.reverse()

    return path

def Yens_algorithm(graph, start_state, goal_xy, reservation_table=None, k=5):
    A = [spacetime_A_star_path(graph, start_state, goal_xy, reservation_table)]
    B = []

    for k_i in range(1, k):
       last_path = A[-1]

       for i in range(len(last_path) - 1):
           spur_node = last_path[i]
           root_path = last_path[:i + 1]
           reservation_table = []

           for path in A:
               if len(path) > i and path[:i + 1] == root_path:
                   reservation_table.append(path[i + 1])

           # Calculate the spur path from the spur node to the goal
           spur_path = spacetime_A_star_path(graph, spur_node, goal_xy, reservation_table)

           # If a valid spur path is found, add it to the list of potential paths
           if spur_path:
               total_path = root_path[:-1] + spur_path
               B.append(total_path)
    
    return A, B
    

class Pathspace():
    def __init__(self, graph, start_state, goal_xy):
        A, B = Yens_algorithm(graph, start_state, goal_xy)
        self.pathspace = PriorityQueue()
        self.pathspace.put(A, 0)
        for path in B:
            self.pathspace.put(path, len(path))
            
    def add_path(self, path):
        self.pathspace.put(path, len(path))
        
    def path(self):
        if self.pathspace.empty():
            return None
        return self.pathspace.get()

