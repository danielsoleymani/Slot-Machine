from pygame.time import get_ticks

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.startingTime = 0
        self.active = False

    def activate(self):
        self.active = True 
        self.startingTime = get_ticks()

    def deactivate(self):
        self.active = False 
        self.startingTime = 0 
    
    def update(self):
        if self.active:
            currentTime = get_ticks()
            if currentTime - self.startingTime >= self.duration:
                self.deactivate()