from librovers import *  # import bindings.
import random
import numpy as np

"""
A stealthy POI that blinks out occasionally. 
"""
class StealthyPOI(rovers.IPOI):
    def __init__(self, value, obs_radius, constraintPolicy, stealth_mastery=0.3):
        super().__init__(value, obs_radius)
        # we will use the stealth combined with a constraint defined in the lib
        self.constraintPolicy = constraintPolicy
        self.stealth_mastery = stealth_mastery  # 0.0 = rookie, 1.0 = super stealthy
        self.visible = False

    # Use a library defined or custom constraint policy with stealth
    def constraint_satisfied(self, entity_pack):
        if not self.visible:
            return False    # "you can't see me"

        return self.constraintPolicy.is_satisfied(entity_pack)

    # tick() is called at every time step (tick) by the library.
    # blink based on a coin toss and stealth mastery
    def tick(self):
        if random.random() < self.stealth_mastery:
            self.visible = False
        else:
            self.visible = True


"""
Custom constraint:
POIs with this constrait can only be observed \
after all other POIs have been observed.
"""
class LastPOIConstraint(rovers.IConstraint):
    def is_satisfied(self, entity_pack):
        for poi in entity_pack.entities:
            if not poi.observed():
                return False

        return True


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
    rovers.Drone()  # drone with no policy specifications (all defaults)
]

pois = [
    # 3 agents must observe
    rovers.POI[rovers.CountConstraint](3),
    # Our custom POI constraint. The POI has a value of 10 and obs_radius of 5.0.
    # mvp, can be observed when all other POIs are observed
    rovers.POI[LastPOIConstraint](10, 5.0, LastPOIConstraint()),
    # 5 agents of a certain type must observe
    rovers.POI[rovers.TypeConstraint](5),
    # Stealthy POI! Has a value of 100.
    # super stealthy with 97% mastery, but needs only 1 spotter!
    StealthyPOI(100, 3.0, rovers.CountConstraint(1), .97)
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
