
def negotiate(agenta, agentb, max_rounds=50):
    offer1 = agenta.path
    offer2 = agentb.path

    #set pathspace for both agents
    agenta.set_pathspace()
    agentb.set_pathspace()

    print("\nInitial offers:")
    print(f"Vessel {agenta.unique_id}: {offer1}")
    print(f"Vessel {agentb.unique_id}: {offer2}")

    for round in range(max_rounds):
        print(f"\nRound {round + 1}:")

        action1, offer1 = agenta.make_offer(offer2)
        print(f"Vessel {agenta.unique_id} action: {action1}, offer: {offer1}")
     
        if action1 == "accept":
            resolve(agenta, agentb, winner=1)
            return

        action2, offer2 = agentb.make_offer(offer1)
        print(f"Vessel {agentb.unique_id} action: {action2}, offer: {offer2}")

        if action2 == "accept":
            resolve(agenta, agentb, winner=2)
            return
        
    resolve(agenta, agentb, winner=0)
    
def resolve(agenta, agentb, winner):
    if winner == 1:
        payment = agenta.offered_tokens
        agenta.tokens -= payment
        agentb.tokens += payment
        agentb.reservation_table = agenta.path
        #agentb.path = agentb.generate_alt_path(agenta.path)
        print(f"Vessel {agenta.unique_id} pays {payment} tokens to Vessel {agentb.unique_id}")
        print(f"Vessel {agenta.unique_id} new token count: {agenta.tokens}")
        print(f"Vessel {agentb.unique_id} new token count: {agentb.tokens}")

    elif winner == 2:
        payment = agentb.offered_tokens
        agentb.tokens -= payment
        agenta.tokens += payment
        agenta.reservation_table = agentb.path
        #agenta.path = agenta.generate_alt_path(agentb.path)
        print(f"Vessel {agentb.unique_id} pays {payment} tokens to Vessel {agenta.unique_id}")
        print(f"Vessel {agenta.unique_id} new token count: {agenta.tokens}")
        print(f"Vessel {agentb.unique_id} new token count: {agentb.tokens}")

    else:
        print("Negotiation failed, both agents keep their paths")