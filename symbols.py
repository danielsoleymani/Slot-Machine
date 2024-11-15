import pygame 

class Symbols:

    def __init__(self, symbolNum, column, stoppingPoint):
        imageTable = {
            1: ("images/J.png", "images/J_Popped.png"),
            2: ("images/K.png", "images/K_Popped.png"),
            3: ("images/Q.png", "images/Q_Popped.png"),
            4: ("images/Crest.png", "images/Crest_Popped.png"),
            5: ("images/Seal.png", "images/Seal_Popped.png"),
            6: ("images/Logo.png", "images/Logo_Popped.png"),
            7: ("images/Football.png", "images/Football_Popped.png"),
            8: ("images/Roc.png", "images/Roc_Popped.png"),
            9: ("images/Scatter.png", "images/Scatter.png"),
            10:("images/2x.png", "images/2x.png"),
            11:("images/3x.png", "images/3x.png"),
            12:("images/4x.png", "images/4x.png"),
            13:("images/5x.png", "images/5x.png"),
            14:("images/10x.png","images/10x.png"),  
            15:("images/100x.png","images/100x.png")
        }

        columnToPixelTable = {
            1 : 250,
            2 : 322.5,
            3 : 395,
            4 : 467.5,
            5 : 540,
            6 : 612.5,
            7 : 685
        }
        
        self.BLUEIMAGE = pygame.image.load(imageTable[symbolNum][0])
        self.YELLOWIMAGE = pygame.image.load(imageTable[symbolNum][1])
        self.image = self.BLUEIMAGE
        self.x = columnToPixelTable[column]
        self.y = 50 
        self.rect = self.image.get_rect()
        self.gravity = 1
        self.velocity = 0
        self.stoppingPoint = stoppingPoint
        self.pop_start_time = None
         


    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

    def falling(self):
        self.velocity = self.velocity + self.gravity
        self.y = self.y + self.velocity
        if self.rect.colliderect(self.stoppingPoint):
            self.y = self.stoppingPoint.top - self.rect.height  
            self.velocity = 0 
        return abs((self.rect.y + 65) - self.stoppingPoint.y) > 1
    
    def clear(self, timer):
        while timer.active:
            self.velocity = self.velocity + self.gravity
            self.y = self.y + self.velocity
            return True 
        return False
    

    def swapColors(self):
        self.image = self.YELLOWIMAGE

