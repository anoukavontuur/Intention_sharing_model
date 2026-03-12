import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mesa
from mesa.time import Priority, Schedule

class MoneyAgent(mesa.Agent):
    """ An agent with a fixed initial wealth and ethnicity"""

    def __init__(self, model, ethnicity):
        super().__init__(model)
        self.wealth = 10
        self.savings = 0
        self.ethnicity = ethnicity
        self.age = self.random.randint(18, 30)
  
    def exchange(self):
        """Give 1 unit to a random other agent""" 
        if self.wealth > 0: 
            other_agent = self.random.choice(self.model.agents)
            other_agent.wealth += 1
            self.wealth -= 1

    def earn_interest(self):
        """Earn interest on savings based on current rate"""
        interest = int(self.savings * self.model.interest_rate)
        self.savings += interest    
              
        
class MoneyModel(mesa.Model):
    """An economy model with some number of agents and policy events"""

    def __init__(self, n=100):
        super().__init__()
        self.interest_rate = 0.05
        self.log = []

        ethnicities = ["Green", "Blue", "Mixed"]

        MoneyAgent.create_agents(
            model = self, 
            n=n,
            ethnicity=self.random.choices(ethnicities, k=n))
        
        #Distribute initial savings
        for agent in self.agents:
            agent.savings = self.random.randint(0, 20)

        #Recurring: Central bank reviews interest rates
        self.rate_review = self.schedule_recurring(
            self.review_interest_rate,
            Schedule(interval=10.0)
        )

        #Recurring: Pay interest
        self.schedule_recurring(
            self.pay_interest,
            Schedule(interval=5.0),
        )

        #One-off: Economic stimulus at t=25
        self.schedule_event(self.economic_stimulus, at=25.0)

    def review_interest_rate(self):
        """Central bank adjusts rate based on average wealth."""
        avg_wealth = self.agents.agg("wealth", np.mean)
        if avg_wealth < 8:
            self.interest_rate = min(0.15, self.interest_rate + 0.02)
            action = "raised"        
        elif avg_wealth > 12:
            self.interest_rate = max(0.01, self.interest_rate - 0.02)
            action = "lowered"
        else:
            action = "held"
        self.log.append(
            f"t={self.time:5.1f} | Rate review: {action} to {self.interest_rate:.0%} "
            f"(avg wealth: {avg_wealth:.1f})"
        )

    def pay_interest(self):
            """Pay interest to all citizens."""
            total_paid = 0
            for agent in self.agents:
                interest = int(agent.savings * self.interest_rate)
                agent.savings += interest
                total_paid += interest
            self.log.append(f"t={self.time:5.1f} | Interest paid: {total_paid} total")

    def economic_stimulus(self):
        """One-time stimulus: every citizen gets 5 units."""
        for agent in self.agents:
            agent.wealth += 5
        self.log.append(f"t={self.time:5.1f} | *** STIMULUS: +5 to all citizens ***")

    def step(self):
        """Regular step: agents exchange money."""
        self.agents.shuffle_do("exchange")

        # Some agents save a portion of their wealth
        for agent in self.agents.select(lambda a: a.wealth > 3):
            save_amount = agent.wealth // 4
            agent.wealth -= save_amount
            agent.savings += save_amount


model = MoneyModel(50)
model.run_until(50)

print("=== Central Bank Economy: Event Log ===\n")
for entry in model.log:
    print(f"  {entry}")

print(f"\n=== Final State (t={model.time:.0f}) ===")
print(f"Interest rate: {model.interest_rate:.0%}")
print(f"Avg wealth: {model.agents.agg('wealth', np.mean):.1f}")
print(f"Avg savings: {model.agents.agg('savings', np.mean):.1f}")
total = sum(a.wealth + a.savings for a in model.agents)
print(f"Total money in economy: {total}")

# reports = model.agents.map("report_status")
# print("Agent reports:")
# for r in reports[:5]:
#     print (f"{r}")

# print(f"Max wealth before tax: {model.agents.agg('wealth', max)}")
# model.agents.do(tax_agent)
# print(f"Max wealth after tax: {model.agents.agg('wealth', max)}")

# # Give all broke agents a subsidy of 1
# broke = model.agents.select(lambda agent: agent.wealth == 0)
# print(f"Broke agents before subsidy: {len(broke)}")

# broke.set("wealth", 1)

# # Verify
# still_broke = model.agents.select(lambda a: a.wealth == 0)
# print(f"Broke agents after subsidy: {len(still_broke)}")

# def wealth_bracket(agent):
#     if agent.wealth == 0:
#         return "broke"
#     elif agent.wealth <= 2:
#         return "moderate"
#     else:
#         return "wealthy"

# print("=== Model Summary After 50 Steps ===\n")

# #overall statistics
# min_wealth, max_wealth, avg_wealth, total_wealth = model.agents.agg("wealth", [min, max, np.mean, sum])
# print(f"Agents: {len(model.agents)}")
# print(
#     f"Total wealth: {total_wealth} (conserved: {'yes' if total_wealth == len(model.agents) else 'no, subsidy applied'})"
# )
# print(f"Wealth range: {min_wealth} to {max_wealth}, mean: {avg_wealth:.2f}\n")

# print("\nBy ethnicity")
# for ethnicity, group in model.agents.groupby("ethnicity"):
#     count = len(group)
#     average = group.agg("wealth", np.mean)
#     broke = len(group.select(lambda agent: agent.wealth == 0))
#     print(
#         f"  {ethnicity:6s}: {count:3d} agents, avg wealth = {average:.2f}, broke = {broke}"
#     )

# print("\nWealth brackets:")
# for bracket, group in model.agents.groupby(wealth_bracket):
#     print(f"  {bracket:8s}: {len(group)} agents")

# #Visualizing
# data = []
# for agent in model.agents:
#     data.append({"wealth": agent.wealth, "ethnicity": agent.ethnicity})
# df = pd.DataFrame(data)
# palette = {"Green": "green", "Blue": "blue", "Mixed": "purple"}
# g = sns.histplot(data=df, x="wealth", hue="ethnicity", discrete=True, palette=palette)
# g.set(
#     title="Wealth distribution by ethnicity", xlabel="Wealth", ylabel="Number of agents"
# )
# plt.show()