from librovers import *  # import bindings.
import random
import numpy as np


"""
Simple camera sensor that reads mxn numpy arrays
For use with convolutional networks
"""
class Camera(rovers.ISensor):
    def scan(self, agent_pack):
        # I read 8x8 images!
        return rovers.tensor(np.zeros((8, 8)))


"""
DepthCamera: Camera sensor that uses a lidar composition policy
"""
class DepthCamera (rovers.ISensor):
    def __init__(self, compositionPolicy):
        super().__init__()
        self.compositionPolicy = compositionPolicy()

    def scan(self, agent_pack):
        # I read 8x8 images!
        image = np.zeros((8, 8), dtype=np.int)
        # And apply lidar like composition to my image!
        composed_image = self.compositionPolicy.compose(
            image.flatten().tolist(), 1.0, 1.0)
        # composed image with alpha=1.0
        return rovers.tensor([composed_image, 1.0])


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
    # drone with no policy specifications (all defaults)
    rovers.Drone(),  
    # Rover with our custom Camera sensor
    rovers.Rover[Camera, Discrete](2.0, Camera()),
    # Rover with our custom depth camera sensor and Lidar Density composition
    rovers.Rover[DepthCamera, Discrete](2.0, DepthCamera(rovers.Density)),
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