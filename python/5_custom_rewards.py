from librovers import *  # import bindings.
import random
import numpy as np

"""
Difference reward but the rover ignores a random rover.
Indifferent towards just that one random rover.
"""
class InDifference (rovers.rewards.IReward):
    def compute(self, agent_pack):
        global_reward = rovers.rewards.Global().compute(agent_pack)

        without_me = list(filter(lambda r: std.addressof(r) != std.addressof(agent_pack.agent),
                                 agent_pack.agents))  # filter myself out
        without_me.remove(random.choice(without_me))  # Ignore random rover :x

        reward_without_me = rovers.rewards.Global().compute((agent_pack.agent, without_me, agent_pack.entities))
        return global_reward - reward_without_me

# Rewards can be arbitrarily complex:
"""
Reward when POIs are observed in a certain order.
Implemented with a trivial state machine.

The state machine transitions are:
start => observe poi 1.0 -> observe poi 2.0 -> wait for n ticks -> observe all pois => end
"""
class FSMReward (rovers.rewards.IReward):
    def __init__(self):
        super().__init__()
        self.state = "start"
        self.counted_ticks = 0

    # True if any poi with `value` has been observed
    def observed(self, pois, value):
        for poi in pois:
            if poi.value() == value and poi.observed():
                return True
        return False

    # True if all pois are observed
    def all_observed(self, pois):
        for poi in pois:
            if not poi.observed():
                return False
        return True

    # define transitions
    def transition(self):
        epsilon = random.random()
        if epsilon < 0.25:
            return  # stay in the current state.

        # 75% chance of transition
        # dictionary defines our transitions        
        self.state = {
            'start': 'step2',
            'step2': 'wait_for_ticks',
            'wait_for_ticks': 'all_pois',
            'all_pois': 'end'
        }.get(self.state, 'start')

    # transition when needed and give a reward of 1.0 when FSM is complete.
    def compute(self, agent_pack):
        
        if self.observed(agent_pack.entities, 1.0) or self.observed(agent_pack.entities, 2.0):
            self.transition()
        if self.all_observed(agent_pack.entities):
            self.transition()
    
        if self.state == 'end':
            return 1.0
        else:
            return 0.0

    # called by the library at every time step
    def tick(self):
        if self.state == 'wait_for_ticks':
            self.counted_ticks += 1
            if self.counted_ticks == 70:    # wait for 70 ticks, then transition
                self.transition()


# aliasing some types to reduce typing
Dense = rovers.Lidar[rovers.Density]        # lidar with density composition
Close = rovers.Lidar[rovers.Closest]        # lidar for closest rover/poi
Discrete = thyme.spaces.Discrete            # Discrete action space
Difference = rovers.rewards.Difference      # Difference reward

agents = [
    # create agent with difference reward
    rovers.Rover[Dense, Discrete, Difference](1.0, Dense(90)),
    # create rover with close lidar and global reward
    rovers.Rover[Close, Discrete](2.0, Close(90)),
    rovers.Drone(),  # drone with no policy specifications (all defaults)
    # Rover with Close Lidar sensor that uses an InDifference reward
    rovers.Rover[Close, Discrete, InDifference](2.0, Close(90), InDifference()),
    # Rover with Dense Lidar sensor that uses an InDifference reward
    rovers.Rover[Dense, Discrete, FSMReward](10.0, Dense(90), FSMReward())
]

# Three POIs with Count and Type constraints:
pois = [
    # 3 agents must observe
    rovers.POI[rovers.CountConstraint](3),
    # 2 agents of a certaiin type to get value 1.0
    rovers.POI[rovers.TypeConstraint](2, 1.0),
    # 5 agents of a certain type must observe
    rovers.POI[rovers.TypeConstraint](5)
]

# Environment with rovers and pois placed in the corners. Defaults to random initialization if unspecified.
Env = rovers.Environment[rovers.CornersInit]
# create an environment with our rovers and pois:
env = Env(rovers.CornersInit(10.0), agents, pois)
states, rewards = env.reset()

# print sample state
print("Sample environment state (each row corresponds to the state of a rover): ")
for state in states:
    print(state.transpose())
