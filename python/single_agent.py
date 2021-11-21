from librovers import * # import bindings.
from render_rovers import RoversViewer # import renderer
import random
random.seed(27)
 
# aliasing some types to reduce typing
Dense = rovers.Lidar[rovers.Density]        # lidar with density composition
Close = rovers.Lidar[rovers.Closest]        # lidar for closest rover/poi
Discrete = thyme.spaces.Discrete            # Discrete action space
CC = rovers.CountConstraint

pois = [
    rovers.POI[CC](1.0, 4.0, CC(1)),
    rovers.POI[CC](1.0, 4.0, CC(1)),
    rovers.POI[CC](3.0, 4.0, CC(1)),
    rovers.POI[CC](1.0, 5.0, CC(1))
]
#env.pois()[0].set_position(width - 5, height - 5)
#env.pois()[1].set_position(width - 10, height - 10)
    
# Environment with rovers and pois placed in the corners. Defaults to random initialization if unspecified.
Env = rovers.Environment[rovers.CornersInit]

width = 50
height = 50
# create a (width * height) environment
env = Env(
    rovers.CornersInit(width),
    [rovers.Rover[Close, Discrete](5.0, Close(90))], 
    pois, 
    width, 
    height
)
renderer = RoversViewer(env)

episodes = 3
for episode in range(0, episodes):

    states, rewards = env.reset()
    done = False
    
    while not done:
        states, rewards = env.step([
            rovers.tensor([random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]) 
            #rovers.tensor([0.09, 0.09])
            for rover in env.rovers()])
        renderer.render()
        done = all (poi.observed() for poi in env.pois()) 