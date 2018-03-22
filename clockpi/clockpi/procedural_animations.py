import random
import time


class ProceduralAnimation(object):
    ANIMATION_FREQ = 1  # Hz

    def __init__(self):
        self.last_frame_time = 0
        self.current_frame = []

    def should_draw_next_frame(self, current_time=None):
        if not current_time:
            current_time = time.time()
        time_since_last_frame = current_time - self.last_frame_time
        if time_since_last_frame >= (1.0 / self.ANIMATION_FREQ):
            self.last_frame_time = current_time
            return True
        return False

    def get_next_frame(self):
        """
        Returns the next frame if it's time for it, otherwise, return the frame
        that was already being displayed. The frame's first index is the Y
        coordinate, and the second is the X, like if they were the other hand-
        drawn artwork.
        """
        if not self.should_draw_next_frame():
            return self.current_frame
        raise NotImplementedError


class ProceduralRain(ProceduralAnimation):
    """
    Uses the frame like a queue, adding to the front and popping off the back
    since the rain is just falling down.
    """
    DROPLET_DENSITY = 0.12  # Average number of droplets per pixel
    DROPLET_LENGTH = 2  # Vertical length of droplets

    def __init__(self, animation_width, animation_height):
        super(ProceduralRain, self).__init__()
        self.animation_width = animation_width
        self.animation_height = animation_height
        self.current_frame = []
        # Generate a blank frame
        for _ in xrange(self.animation_height):
            self.current_frame.append([0] * self.animation_width)

    def should_draw_next_frame(self):
        # Sync up with clock seconds by casting to int
        current_time = int(time.time())
        return super(ProceduralRain, self).should_draw_next_frame(current_time)

    def get_next_frame(self):
        if not self.should_draw_next_frame():
            return self.current_frame
        # Remove the old raindrops at the end of the queue
        self.current_frame.pop()
        # Add new droplets
        self.current_frame.insert(0, [0] * self.animation_width)
        for xx in xrange(self.animation_width):
            if random.random() <= self.DROPLET_DENSITY:
                # Draw the droplet downwards
                for yy in xrange(self.DROPLET_LENGTH):
                    if yy < self.animation_height:
                        self.current_frame[yy][xx] = 1
        return self.current_frame
