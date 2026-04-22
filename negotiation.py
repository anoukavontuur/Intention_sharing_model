
def negotiate(agent1, agent2, max_rounds=50):
    offer1 = agent1.path
    offer2 = agent2.path

    #set pathspace for both agents
    agent1.set_pathspace()
    agent2.set_pathspace()

    print("\nInitial offers:")
    print(f"Agent 1: {offer1}")
    print(f"Agent 2: {offer2}")

    for round in range(max_rounds):
        print(f"\nRound {round + 1}:")

        action1, new_offer1 = agent1.make_offer(offer2)
        print(f"Agent 1 action: {action1}, offer: {new_offer1}")
     
        if action1 == "accept":
            resolve(agent1, agent2, winner=1)
            return

        action2, new_offer2 = agent2.make_offer(offer1)
        print(f"Agent 2 action: {action2}, offer: {new_offer2}")

        if action2 == "accept":
            resolve(agent1, agent2, winner=2)
            return
        
        offer1 = new_offer1
        offer2 = new_offer2

    resolve(agent1, agent2, winner=0)
    
def resolve(agent1, agent2, winner):
    if winner == 1:
        payment = agent1.offered_tokens
        agent1.tokens -= payment
        agent2.tokens += payment
        #agent2.path = agent2.generate_alt_path(agent1.path)
        print(f"Agent 1 accepts Agent 2's offer")
        print(f"Agent 1 pays {payment} tokens to Agent 2")
        print(f"Agent 1 new token count: {agent1.tokens}")
        print(f"Agent 2 new token count: {agent2.tokens}")

    elif winner == 2:
        payment = agent2.offered_tokens
        agent2.tokens -= payment
        agent1.tokens += payment
        #agent1.path = agent1.generate_alt_path(agent2.path)
        print(f"Agent 2 accepts Agent 1's offer")
        print(f"Agent 2 pays {payment} tokens to Agent 1")
        print(f"Agent 1 new token count: {agent1.tokens}")
        print(f"Agent 2 new token count: {agent2.tokens}")
    
    else:
        print("Negotiation failed, both agents keep their paths")