<br />
<p align="center">
  <h3 align="center">Rovers</h3>
  <p align="center">
    A prototype of the Rovers environment.
    <br />
    <br />
    <a href=https://github.com/gaurav-dixitv/rovers#usage>View Python Bindings</a>
    ·
    <a href="https://github.com/gaurav-dixitv/rovers/issues">Report Bug</a>
    ·
    <a href="https://github.com/gaurav-dixitv/rovers/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [Rovers](#rovers)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Python](#python)
  - [C++](#c)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)



<!-- ABOUT THE PROJECT -->
## Rovers

A prototype of the Rovers environment. A C++ template header-only library. Directly use the headers in your project -- does not need compilation, packaging and installation. Python bindings are provided for prototyping.

The library is designed for
* Ease of use: Manages all the hairy bits (think memory, threading, generics). 
* Flexibility: Algorithms are agent/environment/learning agnostic and can be mixed in a variety of ways. Language bindings provide an interface for rapid prototyping. 
* Performance: The rover environment was part of the thyme library for rl, evolution and planning with cpu/gpu/threading optimizations: pay only for what you use.

### Built With
The library uses parts of thyme -- you will notice references to the `thyme` namespace in the utility classes. Eigen is used for linear algebra on the [CG]PU. The python bindings were generated using cppyy. 
* [Eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page)
* [cppyy](https://cppyy.readthedocs.io/en/latest/)
* [thyme]([https://github.com/gaurav-dixitv/rovers.git])

<!-- GETTING STARTED -->
## Getting Started

You will need GCC 8 or higher for c++17 support and python3.

### Prerequisites

* Install pip3
```sh
sudo apt install python3-pip #debian
```
or
```sh
pacman -S python-pip    #arch
```
* Install virtualenv
```sh
sudo pip3 install virtualenv
```

## Installation

### Python

1. Clone the repo
```sh
git clone https://github.com/gaurav-dixitv/rovers.git
```
2. Create a virtual environment
```sh
cd rovers && mkdir env && python3 -m venv env/
```
3. Activate the environment
```sh
. env/bin/activate
```
4. Install requirements
```sh
pip3 install -r requirements.txt
```
5. Running a python api test
```sh
python3 python/1_rovers.py
```


### C++

If you want to test the the C++ api, the makefile provides convenient build targets. 
Since this is a header only library, the C++ source should go in the the `test/` folder.

1. clean objects and binaries
```sh
make clean
```
2. make target. Specify the `entry` of your source from the test folder. Assuming you want to run `test/rovers.cpp`,
```sh
make release entry=rovers
```
3. run
```sh
./build/bin/rovers
```

Or putting it all together,

4. clean, make and run
```sh
make clean && make release entry=rovers && ./build/bin/rovers
```



<!-- USAGE EXAMPLES -->
## Usage

1. Using the library: snippet from `python/1_rovers.py`
```py
from librovers import *

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
    # 2 agents of a certaiin type to get value 1.0
    rovers.POI[rovers.TypeConstraint](2, 1.0),
    # 5 agents of a certain type must observe
    rovers.POI[rovers.TypeConstraint](5)
]

env = rovers.Environment(CornersInit(10.0), agents, pois)
states, rewards = env.reset()
```

2.  `python/2_custom_agents.py` shows you how to create new agents. A partial snippet:
```py
class PyRover (rovers.IRover): #inherit from the library rover interface
    def __init__(self, do_a_flip = True):
        self.do_a_flip = do_a_flip

    # compute state
    def scan(self, agent_pack):
        # I see 9.0 for all agents!
        return rovers.tensor([9.0 for r in agent_pack.agents])

    # modified difference reward from the library
    def reward(self, agent_pack):
        return rovers.rewards.Difference().compute(agent_pack) * 0.5

    def apply_action(self, action):
        if (action and self.do_a_flip): 
            self.back_flip()
        
```

3.  `python/3_custom_sensors.py` shows you how to create new sensors for existing and new agents.
```py
class Camera(rovers.ISensor):
    def scan(self, agent_pack):
        # I read 8x8 images!
        return rovers.tensor(np.zeros((8, 8)))
```

4.  `python/4_custom_entities.py` shows you how to create new entities.
```py
"""
A stealthy POI that blinks out occasionally. 
"""
class StealthyPOI(rovers.IPOI):
    def __init__(self, stealth_mastery=0.3):
        self.stealth_mastery = stealth_mastery
        self.visible = False

    # Use a library defined or custom constraint policy with stealth
    def constraint_satisfied(self, entity_pack):
        if not self.visible:
            return False
        return self.constraintPolicy.is_satisfied(entity_pack)

    # tick() is called at every time step (tick) by the library.
    def tick(self):
        if random.random() < self.stealth_mastery:
            self.visible = False
        else:
            self.visible = True
```

5.  `python/5_custom_rewards.py` shows you how to create new rewards.
```py
"""
Indifferent towards just that one random rover.
"""
class InDifference (rovers.rewards.IReward):
    def compute(self, agent_pack):
        global_reward = rewards.Global().compute(agent_pack)

        # filter myself out
        without_me = list(filter(lambda r: r != agent_pack.agent, agent_pack.agents))
         # Ignore random rover :x
        without_me.remove(random.choice(without_me)) 

        reward_without_me = rewards.Global().compute(without_me)
        return global_reward - reward_without_me
```

6. `python/6_complete.py` uses an eclectic mix of agents, entitys and rewards with a training regime:
```py
agents = [
    rovers.Rover[Dense, Discrete, FSMReward](1.0, Dense(90), FSMReward()),
    rovers.Drone(),  # drone with no policy specifications (all defaults)
    PyRover(1.0, True, FSMReward()),
    rovers.Rover[Camera, Discrete, Difference](2.0, Camera()),
    rovers.Rover[DepthCamera, Discrete, InDifference](2.0, DepthCamera(rovers.Density), InDifference()),
]

pois = [
    StealthyPOI(10, 1.0, LastPOIConstraint(), .27),
    rovers.POI[rovers.CountConstraint](3),
    rovers.POI[rovers.TypeConstraint](5),
    StealthyPOI(100, 3.0, rovers.CountConstraint(1), .97)
]

env = rovers.Environment(CornersInit(10.0), agents, pois)
states, _ = env.reset()

steps = 1000
for s in range(steps):
    actions = [policies[i].sample(get_values_from_pytorch(states[i])) for i in range(len(agents))]
    old_states = states
    states, rewards = env.step(actions)
    for i in range(len(agents)):
        learn(old_states[i], actions[i], states[i], rewards[i])
```



<!-- ROADMAP -->
## Roadmap
TBD next meeting, Nov 20 / 27.
<!-- CONTRIBUTING -->
## Contributing

Reach out to me before the next meeting if you want to see a specific scenario implemented.
If you want to contribute your own scenarios to discuss in the meeting, feel free to fork and send a pull request.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.