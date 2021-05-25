from ..utils.vector import Vector2


class ICamera:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1
        
        
    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        raise NotImplementedError

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        raise NotImplementedError
        
class Camera(ICamera):

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to a screen-coordinate. """
        screen_coord= position*self.scale + self.screen_size/2-self.position*self.scale
        return screen_coord

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        coord_screen = 1/self.scale * (position + self.position*self.scale - self.screen_size/2)
        return coord_screen


