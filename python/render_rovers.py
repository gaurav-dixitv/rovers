import sys
import math
import random

from gym.envs.classic_control import rendering
import pyglet
import pyglet.gl as gl

def set_color(self, r: float, g: float, b: float, a=1.0):
    """Monkey patch to enable alpha
    Arguments:
        r {float} -- red [0.0, 1.0]
        g {float} -- green [0.0, 1.0]
        b {float} -- blue [0.0, 1.0]
    Keyword Arguments:
        a {float} -- alpha (default: {1.0})
    """
    self._color.vec4 = (r, g, b, a)
rendering.Geom.set_color = set_color  # Monkey_patch to allow alpha

class RoversViewer(rendering.Viewer):

    primary_width = 1024.0
    primary_height = 1024.0       #768.0
    screen = pyglet.canvas.get_display().get_default_screen()
    viewport_width = int(screen.width * 0.5)
    viewport_height = int((primary_height/primary_width) * viewport_width)

    camera_width = primary_width * 0.01
    camera_height = primary_height * 0.01

    def __init__(self, env):
        super().__init__(self.viewport_width, self.viewport_height)
        self.window.close()
        self.window = pyglet.window.Window(
           self.viewport_width, self.viewport_height, config=gl.Config(sample_buffers=1, samples=4))
        self.window.on_close = self.window_closed_by_user
        self.set_bounds(
            0.0,
            self.camera_width,
            0.0,
            self.camera_height)

        self.env = env
        # Anti alias hack
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def draw_arc(self, angle, radius=1, res=None, filled=True, **attrs):
        # Use a default of 30 if angle is 2pi, adjust based on the angle
        if res is None:
            res = math.ceil(30 * radius * angle / (2*math.pi))
        geom = make_arc(angle, radius=radius, res=res, filled=filled)
        rendering._add_attrs(geom, attrs)
        self.add_onetime(geom)
        return geom

    def update(self):
        # Environment space of 10x10 grid
        width = 10
        height = 10
        for i in range(width + 1):
            self.draw_line((float(i), 0.0), (float(i), float(height)), color=(0.0, 0.0, 0.0, 0.1))
        for i in range(height + 1):
            self.draw_line((0.0, float(i)), (float(width), float(i)), color=(0.0, 0.0, 0.0, 0.1))

        for rover in self.env.rovers():
            position = rover.position()
            transform = rendering.Transform(translation=(position.x, position.y))
            color = (1.0, 0.0, 0.0, 0.5)
            if hasattr(rover, "color"):
                color = rover.color
            self.draw_circle(rover.obs_radius(), 30, color=color, filled=True).add_attr(transform)

        for poi in self.env.pois():
            position = poi.position()
            transform = rendering.Transform(translation=(position.x, position.y))
            color = (0.0, 0.0, 1.0, 0.2)
            if poi.observed():
                color = (0.0, 0.0, 1.0, 0.7)
            self.draw_circle(poi.obs_radius(), 30, color=color, filled=True).add_attr(transform)









if __name__ == "__main__":

    # rendering test
    from librovers import *  # import bindings.

    """
    Random walk at every step. Weight the movement by the size of the action.
    """
    class RandomWalkRover (rovers.IRover):

        color = (0.0, 1.0, 0.0, 0.5)

        def __init__(self, obs_radius=1.0):
            super().__init__(obs_radius)

        def scan(self, agent_pack):
            return rovers.tensor([9.0 for r in agent_pack.agents])

        def reward(self, agent_pack):
            return rovers.rewards.Difference().compute(agent_pack)

        def apply_action(self):
            # The action is set before `apply_action()` is called
            action = self.action()
            x = self.position().x + random.uniform(-0.01*action, 0.01*action)
            y = self.position().y + random.uniform(-0.01*action, 0.01*action)
            self.set_position(x, y)

    # aliasing some types to reduce typing
    Dense = rovers.Lidar[rovers.Density]        # lidar with density composition
    Close = rovers.Lidar[rovers.Closest]        # lidar for closest rover/poi
    Discrete = thyme.spaces.Discrete            # Discrete action space

    agents = [
        RandomWalkRover(1.0),
        RandomWalkRover(1.0),
        rovers.Rover[Close, Discrete](2.0, Close(90)),
        rovers.Drone()
    ]
    pois = [
        rovers.POI[rovers.CountConstraint](3),
        rovers.POI[rovers.TypeConstraint](2, 1.0),
        rovers.POI[rovers.TypeConstraint](5),
        rovers.POI[rovers.TypeConstraint](2)
    ]

    # Environment with rovers and pois placed in the corners. Defaults to random initialization if unspecified.
    Env = rovers.Environment[rovers.CornersInit]
    # create an environment with our rovers and pois:
    env = Env(rovers.CornersInit(10.0), agents, pois)
    states, rewards = env.reset()

    renderer = RoversViewer(env)
    steps = 2000
    for step in range(steps):
        states, rewards = env.step([10 for rover in env.rovers()])
        renderer.update()
        renderer.render()
