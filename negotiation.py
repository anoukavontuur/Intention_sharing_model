
def negotiate(agenta, agentb):
    offer_a = agenta.path
    offer_b = agentb.path

    #set pathspace for both agents
    agenta.set_pathspace()
    agentb.set_pathspace()

    print("\nInitial offers:")
    print(f"Vessel {agenta.unique_id}: {offer_a}")
    print(f"Vessel {agentb.unique_id}: {offer_b}")

    round = 0

    while not agenta.pathspace.empty() and not agentb.pathspace.empty():
        round += 1
        print(f"\nRound {round}:")

        # Agent A makes an offer to Agent B
        action_a, offer_a = agenta.make_offer(offer_b)
        print(f"Vessel {agenta.unique_id} action: {action_a}, offer: {offer_a}")
     
        if action_a == "accept":
            print(f"Vessel {agenta.unique_id} accepts the offer from Vessel {agentb.unique_id}, vessel {agentb.unique_id} wins")
            resolve(winner=agentb, offer=offer_b, loser=agenta)
            return
        
        if action_a == "wait":
            print(f"Vessel {agenta.unique_id} waits, no path available")
            resolve_waiting(waiter=agenta, offer=offer_a, other=agentb)
            return

        # Agent B makes an offer to Agent A
        action_b, offer_b = agentb.make_offer(offer_a)
        print(f"Vessel {agentb.unique_id} action: {action_b}, offer: {offer_b}")

        if action_b == "accept":
            print(f"Vessel {agentb.unique_id} accepts the offer from Vessel {agenta.unique_id}, vessel {agenta.unique_id} wins")
            resolve(winner=agenta, offer=offer_a, loser=agentb)
            return
        
        if action_b == "wait":
            print(f"Vessel {agentb.unique_id} waits, no path available")
            resolve_waiting(waiter=agentb, offer=offer_b, other=agenta)
            return
        
    print("\nNegotiation failed, both agents keep their paths")

def resolve(winner, offer, loser):
    #Payement
    payement = winner.offered_tokens
    winner.tokens -= payement
    loser.tokens += payement
    winner.offered_tokens = 0
    loser.offered_tokens = 0

    #Paths
    winner.path = offer
    loser.path = loser.generate_alternative_path(offer)

    #Prints
    print(f"\nVessel {winner.unique_id} pays {payement} tokens to Vessel {loser.unique_id}")
    print(f"Vessel {winner.unique_id} new token count: {winner.tokens}")
    print(f"Vessel {loser.unique_id} new token count: {loser.tokens}")

def resolve_waiting(waiter, offer, other):
    #Paths
    waiter.path = offer
    other.path = other.generate_alternative_path(offer)
    
    #Prints
    print(f"Vessel {waiter.unique_id} new path: {waiter.path}")
    print(f"Vessel {other.unique_id} new path: {other.path}")