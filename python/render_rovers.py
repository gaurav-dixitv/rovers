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

    def __init__(self, env):
        self.env = env
        screen = pyglet.canvas.get_display().get_default_screen()
        self.viewport_width = int(screen.width * 0.5)
        self.viewport_height = int((self.env.height()/self.env.width()) * self.viewport_width)
        super().__init__(self.viewport_width, self.viewport_height)

        self.window.close()
        self.window = pyglet.window.Window(
           self.viewport_width, self.viewport_height, config=gl.Config(sample_buffers=1, samples=4))
        self.window.on_close = self.window_closed_by_user

        camera_width = self.env.width()
        camera_height = self.env.height()
        padding = 1.0
        self.set_bounds(
            -padding,
            camera_width + padding,
            -padding,
            camera_height + padding)

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
    
    
    def render(self):
        self.update()
        super().render()
        
    def update(self):

        for i in range(self.env.width() + 1):
            self.draw_line((float(i), 0.0), (float(i), float(self.env.height())), color=(0.0, 0.0, 0.0, 0.1))
        for i in range(self.env.height() + 1):
            self.draw_line((0.0, float(i)), (float(self.env.width()), float(i)), color=(0.0, 0.0, 0.0, 0.1))

        # draw rovers
        for rover in self.env.rovers():
            position = rover.position()
            transform = rendering.Transform(translation=(position.x, position.y))
            color = (1.0, 0.0, 0.0) # choose color by type
            # rover
            self.draw_circle(0.5, 30, color=(*color, 0.5), filled=True).add_attr(transform)
            # observation radius
            self.draw_circle(rover.obs_radius(), 30, color=(*color, 0.1), filled=True).add_attr(transform)

        # draw pois
        for poi in self.env.pois():
            position = poi.position()
            transform = rendering.Transform(translation=(position.x, position.y))
            color = (0.0, 0.0, 1.0) # choose color by type
            # poi
            self.draw_circle(0.5, 30, color=(*color, 0.05 if poi.observed() else 0.5), filled=True).add_attr(transform)
            # observation radius
            self.draw_circle(poi.obs_radius(), 30, color=(*color, 0.05 if poi.observed() else 0.1), filled=True).add_attr(transform)


if __name__ == "__main__":

    # rendering test
    from librovers import *  # import bindings.

    # aliasing some types to reduce typing
    Dense = rovers.Lidar[rovers.Density]        # lidar with density composition
    Close = rovers.Lidar[rovers.Closest]        # lidar for closest rover/poi
    Discrete = thyme.spaces.Discrete            # Discrete action space

    agents = [
        rovers.Rover[Close, Discrete](5.0, Close(90)),
        rovers.Rover[Close, Discrete](5.0, Close(90))
    ]
    pois = [
        rovers.POI[rovers.CountConstraint](3, 2.0, 1),
        rovers.POI[rovers.TypeConstraint](2.0, 1.0),
        rovers.POI[rovers.TypeConstraint](5),
        rovers.POI[rovers.TypeConstraint](2, 5.0, rovers.TypeConstraint(2))
    ]
    
 

    # Environment with rovers and pois placed in the corners. Defaults to random initialization if unspecified.
    Env = rovers.Environment[rovers.CornersInit]
    
    width = 50
    height = 50
    # create a (width * height) environment
    env = Env(rovers.CornersInit(width), agents, pois, width, height)
    states, rewards = env.reset()
    
    env.rovers()[0].set_position(22, 27)
    env.rovers()[1].set_position(27, 22)

    # test
    env.pois()[0].set_position(1, 1)
    env.pois()[1].set_position(width - 1, 1)
    env.pois()[2].set_position(1, height - 1)
    env.pois()[3].set_position(width - 10, height - 10)

    renderer = RoversViewer(env)
    steps = 10000
    
    for step in range(steps):
        states, rewards = env.step([
            # rovers.tensor([random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]) 
            rovers.tensor([0.05, 0.05])
            for rover in env.rovers()])
        renderer.update()
        renderer.render()