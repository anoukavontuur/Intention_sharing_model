from os import path

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
    """Spatial heuristic: Euclidean distance between two 2D positions."""
    (x1, y1) = a
    (x2, y2) = b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx * dx + dy * dy)**0.5 # Euclidean distance

def path_cost(path):
    total_cost = 0

    v_optimal = 2          # preferred velocity
    w_distance = 1.0       # weight for distance
    w_velocity = 0.5       # penalty for wrong speed
    w_acceleration = 1.0   # penalty for acceleration

    edges = [(path[i-1], path[i]) for i in range(1, len(path))]

    for step in path:
        v = step[3]  # velocity

        if v == 0:
            total_cost += 1  

        total_cost += (v - v_optimal) ** 2 * w_velocity  

    for edge in edges:

        a = edge[0][0]  # (x, y) of the first state
        b = edge[1][0]  # (x, y) of the second

        dv = edge[1][3] - edge[0][3]  # velocity change
        
        total_cost += heuristic(a, b) * w_distance
        total_cost += dv ** 2 * w_acceleration

    return round(total_cost, 2)

def spacetime_A_star_search(graph, start_state, goal_xy, reservation_table=None, horizon=50):
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
        current_state = frontier.get()  # current_state = ((x, y), t, heading, velocity)
        current_xy = current_state[0]   #(x, y)
        current_t = current_state[1]    #t
        current_heading = current_state[2]  # heading
        current_velocity = current_state[3]  # velocity

        if current_t > horizon:
            break
        
        # Check if goal is reached (any time is acceptable)
        if current_xy == goal_xy:
            goal_state = current_state
            break
        
        # Generate space-time successors
        for next_state in graph.neighbors(current_xy, current_t, goal_xy, current_heading, current_velocity):
           
            if has_conflict([current_state, next_state], reservation_table):
                continue

            new_cost = cost_so_far[current_state] + path_cost([current_state, next_state])
            
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
            if spur_path == []:
                continue

            total_path = root_path[:-1] + spur_path

            # print("\nIteration", _, i)
            # print("Root path:", root_path)
            # print("Spur node:", spur_node)
            # print("Blocked next states:", blocked_next_states)
            # print("Spur path:", spur_path)
            # print("Total path:", total_path)
            # print("Cost of total path:", path_cost(total_path))

            if total_path not in A and total_path not in B:
                B.append(total_path)

        if B == []:
            break

        next_path = min(B, key = lambda p: path_cost(p))

        # print("\nNext path added to A:", next_path)   
        
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

# TESTING
testgraph = GridGraph(9, 9)
start_state = ((0, 0), 0, 1, 2) # (x, y), t, heading, velocity
goal_xy = (0, 8)
path = spacetime_A_star_path(testgraph, start_state, goal_xy)
print("\nA* Path")
print("Shortest path:", path)
print("Cost of shortest path:", path_cost(path))

print("\nYen's K-Shortest Paths")
pathspace = Pathspace(testgraph, start_state, goal_xy)
while not pathspace.empty():
    next_path = pathspace.get()
    print("Next path:", next_path)
    print("Cost of next path:", path_cost(next_path))



