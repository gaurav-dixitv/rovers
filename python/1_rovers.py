
from librovers import *  # import bindings.


# aliasing some types to reduce typing
Dense = rovers.Lidar[rovers.Density]        # lidar with density composition
Close = rovers.Lidar[rovers.Closest]        # lidar for closest rover/poi
Discrete = thyme.spaces.Discrete            # Discrete action space
Difference = rovers.rewards.Difference      # Difference reward

# create rovers
agents = [
    # create agent with difference reward
    rovers.Rover[Dense, Discrete, Difference](1.0, Dense(90)),
    # create rover with close lidar and global reward
    rovers.Rover[Close, Discrete](2.0, Close(90)),
    rovers.Drone()  # drone with no policy specifications (all defaults)
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
