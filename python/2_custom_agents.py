from librovers import *  # import bindings.
import random

"""
A custom rover that:
uses orientation
computes a modified difference reward
implements a new sensing mechanism
"""
class PyRover (rovers.IRover):
    def __init__(self, obs_radius=1.0, use_orientation=False):
        super().__init__(obs_radius)
        self.use_orientation = use_orientation      # Our custom rover uses orientation

    # You can use a scanning method implemented \
    # in the library or roll out your own:
    def scan(self, agent_pack):
        # I see 9.0 for all agents!
        return rovers.tensor([9.0 for r in agent_pack.agents])

    # You can use a reward method implemented \
    # in the library or roll out your own.
    # Create a new reward that adds -1.0 to difference rewards
    def reward(self, agent_pack):
        return rovers.rewards.Difference().compute(agent_pack) - 1.0

    def apply_action(self):
        # some physical manifestation of this action. Maybe move or something.
        pass


"""
A noisy lidar composition strategy that adds random noise to lidar observation.
"""
class BonkedComposition(rovers.ISensorComposition):
    def __init__(self, bonk_factor=7.0):
        super().__init__()
        self.bonk_factor = bonk_factor  # how noisy this sensor is

    # add noise:
    def compose(self, range, init, scale):
        return max(range) + random.random() * self.bonk_factor


# aliasing some types to reduce typing
Dense = rovers.Lidar[rovers.Density]        # lidar with density composition
Close = rovers.Lidar[rovers.Closest]        # lidar for closest rover/poi
Discrete = thyme.spaces.Discrete            # Discrete action space
Difference = rovers.rewards.Difference      # Difference reward

# Lidar with our new bonked composition policy!
BonkedLidar = rovers.Lidar[BonkedComposition]


# create rovers
agents = [
    # create agent with difference reward
    rovers.Rover[Dense, Discrete, Difference](1.0, Dense(90)),
    # create rover with close lidar and global reward
    rovers.Rover[Close, Discrete](2.0, Close(90)),
    rovers.Drone(),  # drone with no policy specifications (all defaults)
    # Our new custom Rover
    PyRover(1.0, True),
    # Rover with a bonked lidar
    rovers.Rover[BonkedLidar, Discrete](
        3.0, BonkedLidar(90, BonkedComposition()))
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
