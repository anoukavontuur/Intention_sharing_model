from Grid import GridGraph
import heapq
from conflict_detection import has_conflict

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
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx * dx + dy * dy)**0.5 # Euclidean distance

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
            next_xy = next_state[0]
            next_t = next_state[1]
           
            if has_conflict([current_state, next_state], reservation_table):
                continue

            dx = next_xy[0] - current_xy[0]
            dy = next_xy[1] - current_xy[1]

            if abs(dx) and abs(dy): 
                new_cost = cost_so_far[current_state] + 1.4  # Diagonal move
            else:
                new_cost = cost_so_far[current_state] + 1
            
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + heuristic(next_state[0], goal_xy)
                frontier.put(next_state, priority)
                came_from[next_state] = current_state
        
    return came_from, goal_state

def path_cost(path):
    total_cost = 0.0
    edges = [(path[i-1], path[i]) for i in range(1, len(path))]

    for edge in edges:
        dx = edge[1][0][0] - edge[0][0][0]
        dy = edge[1][0][1] - edge[0][0][1]
        if abs(dx) and abs(dy):
            total_cost += 1.4  # Diagonal move
        else:
            total_cost += 1    
    return round(total_cost, 2)

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

def Yens_algorithm(graph, start_state, goal_xy, reservation_table=None):
    A = [spacetime_A_star_path(graph, start_state, goal_xy, reservation_table)]
    B = []

    k = min(graph.width, graph.height, 10)

    for _ in range(1, k):
        previous_path = A[-1]

        for i in range(len(previous_path) - 1):
            spur_node = previous_path[i]
            root_path = previous_path[:i + 1]
            blocked_next_states = []

            for path in A:
                if len(path) > i and path[:i + 1] == root_path:
                    blocked_next_states.append(path[i + 1])
            
            spur_path = spacetime_A_star_path(graph, spur_node, goal_xy, blocked_next_states)

            total_path = root_path[:-1] + spur_path

            if total_path not in A and total_path not in B:
                B.append(total_path)

        next_path = min(B, key = lambda p: path_cost(p))
        B.remove(next_path)
        A.append(next_path)

    return A
    
class Pathspace(PriorityQueue):
    def __init__(self, graph, start_state, goal_xy):
        super().__init__()
        A = Yens_algorithm(graph, start_state, goal_xy)
        for path in A:
            self.put(path, path_cost(path))
        self.get() # Remove the first path, which is the shortest path


