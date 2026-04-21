from Grid import GridGraph
from pathfinding import spacetime_A_star_path, Pathspace
from conflict_detection import has_conflict

class Testagent():
    def __init__(self, graph, start_state, goal_position, tokens, unique_id):
        self.graph = graph
        self.start_state = start_state
        self.goal_position = goal_position
        self.pathspace = Pathspace(self.graph, self.start_state, self.goal_position)
        self.tokens = tokens
        self.offered_tokens = 0
        self.id = unique_id
        self.path = self.pathspace.path()

    def cost(self, path):
        return len(path)
    
    def generate_alt_path(self, reservation_table):
        return spacetime_A_star_path(self.graph, self.start_state, self.goal_position, reservation_table)
    
    def make_offer(self, opponent_offer):
        alt_path = self.generate_alt_path(opponent_offer)
        if not has_conflict(self.path, opponent_offer):
            return "accept", self.path

        if self.cost(self.path) <= self.cost(alt_path):
            if self.tokens - self.offered_tokens > 0:
                self.offered_tokens += 1
                return "keep", self.path
            else:
                self.path = self.pathspace.path()
                self.offered_tokens = 0
                return "change", self.path
        else:
            self.path = alt_path
            return "accept", self.path

def negotiate(agent1, agent2, max_rounds=50):
    offer1 = agent1.path
    offer2 = agent2.path

    print("\nInitial offers:")
    print(f"Agent 1: {offer1}")
    print(f"Agent 2: {offer2}")

    for round in range(max_rounds):
        print(f"\nRound {round + 1}:")

        action1, offer1 = agent1.make_offer(offer2)
        print(f"Agent 1 action: {action1}, offer: {offer1}")
     
        if action1 == "accept":
            resolve(agent1, agent2, winner=1)
            return

        action2, offer2 = agent2.make_offer(offer1)
        print(f"Agent 2 action: {action2}, offer: {offer2}")

        if action2 == "accept":
            resolve(agent1, agent2, winner=2)
            return

    resolve(agent1, agent2, winner=0)
    
def resolve(agent1, agent2, winner):
    if winner == 1:
        payment = agent1.offered_tokens
        agent1.tokens -= payment
        agent2.tokens += payment
        #agent2.path = agent2.generate_alt_path(agent1.path)
        print(f"Agent 1 accepts Agent 2's offer")

    elif winner == 2:
        payment = agent2.offered_tokens
        agent2.tokens -= payment
        agent1.tokens += payment
        #agent1.path = agent1.generate_alt_path(agent2.path)
        print(f"Agent 2 accepts Agent 1's offer")
    
    else:
        print("Negotiation failed, both agents keep their paths")

mygraph = GridGraph(5, 5)
agent1 = Testagent(mygraph, ((0, 0), 0), (4, 4), 1, 1)
agent2 = Testagent(mygraph, ((0, 4), 0), (4, 0), 1, 2)

if has_conflict(agent1.path, agent2.path):
    print("Conflict detected, starting negotiation")
    negotiate(agent1, agent2)

print("\nFinal paths and tokens:")
print(f"Agent 1 path: {agent1.path}, tokens: {agent1.tokens}")
print(f"Agent 2 path: {agent2.path}, tokens: {agent2.tokens}")

