from librovers import *
import random
import numpy as np
from tqdm import tqdm

"""
================================================================================
Putting it all together.
This file uses all the defined variations of \
    1. Agents
    2. Sensors
    3. Entities
    4. Rewards
to create a rich customizable and heterogeneous environment.

A PyTorch stub near the end of the file shows an example of running an episode.
================================================================================
"""




"""
================================================================================
Custom Agents
================================================================================
"""
"""
A custom rover that:
uses orientation
computes a modified difference reward
implements a new sensing mechanism
"""
class PyRover (rovers.IRover):
    def __init__(self, obs_radius=1.0, use_orientation=False, reward_type = rovers.rewards.Difference()):
        super().__init__(obs_radius)
        self.use_orientation = use_orientation      # Our custom rover uses orientation
        self.reward_type = reward_type
    # You can use a scanning method implemented \
    # in the library or roll out your own:
    def scan(self, agent_pack):
        # I see 9.0 for all agents!
        return rovers.tensor([9.0 for r in agent_pack.agents])

    # You can use a reward method implemented \
    # in the library or roll out your own.
    # Create a new reward that adds -1.0 to difference rewards
    def reward(self, agent_pack):
        return self.reward_type.compute(agent_pack) - 0.5

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





"""
================================================================================
Custom Sensors
================================================================================
"""
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





"""
================================================================================
Custom Entities / POIs
================================================================================
"""
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






"""
================================================================================
Custom Rewards
================================================================================
"""
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
            return self.state  # stay in the current state.

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





"""
================================================================================
Setting up the environment
================================================================================
"""
print ("Setting up bindings...")

# aliasing some types to reduce typing
Dense = rovers.Lidar[rovers.Density]        # lidar with density composition
Close = rovers.Lidar[rovers.Closest]        # lidar for closest rover/poi
Discrete = thyme.spaces.Discrete            # Discrete action space
Difference = rovers.rewards.Difference      # Difference reward

# Lidar with our new bonked composition policy!
BonkedLidar = rovers.Lidar[BonkedComposition]

agents = [
    # create agent with FSMReward reward and a dense lidar sensor
    rovers.Rover[Dense, Discrete, FSMReward](1.0, Dense(90), FSMReward()),
    # create rover with close lidar and global reward
    rovers.Rover[Close, Discrete](2.0, Close(90)),
    rovers.Drone(),  # drone with no policy specifications (all defaults)
    # Our new custom Rover that uses a sliced version of the FSMReward
    PyRover(1.0, True, FSMReward()),
    # Rover with a bonked lidar
    rovers.Rover[BonkedLidar, Discrete](
        3.0, BonkedLidar(90, BonkedComposition())),
    # Rover with our custom Camera sensor using difference reward
    rovers.Rover[Camera, Discrete, Difference](2.0, Camera()),
    # Rover with our custom depth camera sensor and Lidar Density and InDifference rewards
    rovers.Rover[DepthCamera, Discrete, InDifference](2.0, DepthCamera(rovers.Density), InDifference()),
    # Rover with bonked Lidar with resolution 9 degrees that uses an InDifference reward
    rovers.Rover[BonkedLidar, Discrete, InDifference](2.0, BonkedLidar(9, BonkedComposition(1.5)), InDifference()),
    # Rover with Close Lidar sensor that uses an FSMReward reward
    rovers.Rover[Close, Discrete, FSMReward](10.0, Close(90), FSMReward())
]

pois = [
    # 27% stealthy POI; needs to be observed after all other POIs.
    StealthyPOI(10, 1.0, LastPOIConstraint(), .27),
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


Env = rovers.Environment[rovers.CornersInit]
env = Env(rovers.CornersInit(10.0), agents, pois)
states, rewards = env.reset()

print ("Sample environment state (state of each rover is a row): ")
for state in states:
    print(state.transpose())





"""
================================================================================
Setting up a policy: PyTorch stub
================================================================================
"""
class GreedyPolicy:
    def __init__(self, initial_epsilon = 1.0,min_epsilon= 0.1, anneal_interval=1000, decay_rate=1.0):
        self.epsilon = initial_epsilon
        self.min_epsilon = min_epsilon
        self.delta = ((initial_epsilon - min_epsilon) * decay_rate) / anneal_interval

    def sample(self, action_values, deterministic = False):
        exploration = random.random()
        if (not deterministic and exploration < self.epsilon):
                return random.randint(0, len(action_values))
        return np.argmax(action_values)
    
    # assuming you are using a machine learning library like PyTorch
    def anneal(self):
        self.epsilon -= m_delta
        self.epsilon = max(self.min_epsilon, self.epsilon)


# state -> action values
def get_values_from_pytorch(state):
    return [70.5, 33.2, 11.98, 0.1, 100.2]

def learn(state, action, next_state, reward):
    # your machine/reinforcemnt learning \ evolution magic here
    pass




"""
================================================================================
Running n steps
================================================================================
"""
print ("\nBegining learning sequence.")
policies = [GreedyPolicy() for agent in agents]

states, _ = env.reset()
steps = 1000
for s in tqdm(range(steps)):
    actions = [
        policies[i].sample(get_values_from_pytorch(states[i])) for i in range(len(agents))
    ]
    old_states = states
    states, rewards = env.step(actions)

    for i in range(len(agents)):
        learn(old_states[i], actions[i], states[i], rewards[i])

print ("Learning complete.")
