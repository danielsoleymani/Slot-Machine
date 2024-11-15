import sys
import pygame
import button
import backend
import symbols
import timer

pygame.init()

running = True 

LOGO_IMAGE = pygame.image.load("images/Cathy_logo.png")
START_BUTTON_IMAGE = pygame.image.load("images/startbutton.png")
QUIT_BUTTON_IMAGE = pygame.image.load("images/quitbutton.png")
SPIN_BUTTON_IMAGE = pygame.image.load("images/SpinButton.png")
BOARDER_IMAGE = pygame.image.load("images/boarder.png")
BACKGROUND_IMAGE = pygame.image.load("images/backgroundImage.png")
BOARD_BACKGROUND = pygame.image.load("images/Board_Background.png")

HEIGHT = 700
WIDTH = 1000
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cathy's Casino Slot")
clock = pygame.time.Clock()
global grid

start_button = button.Button(START_BUTTON_IMAGE,100, 600, 0.5)
quit_button = button.Button(QUIT_BUTTON_IMAGE,400, 600, 0.6)
spin_button = button.Button(SPIN_BUTTON_IMAGE, 600, 590, 1)
baseline = pygame.Rect(250, 577.5, 500, 5)
back = backend.Backend()
# timer1 - timer2 = time spent yellow 
timer1 = timer.Timer(500)
timer2 = timer.Timer(250)
timer3 = timer.Timer(650)

balence = 10000.00
betsize = 5.00


##GAME STATES 
HOME_SCREEN = 1
GAME_SCREEN_IDLE = 2 
GAME_SCREEN_PLAYING_MOVING = 3
GAME_SCREEN_PLAYING_IDLE = 4
GAME_SCREEN_TUMBLE = 5
GAME_SCREEN_GAME_OVER = 6
GAME_SCREEN_CLEAR = 7 
state = HOME_SCREEN

font = pygame.font.SysFont("impact" , 20)
font2 =  pygame.font.SysFont("impact" , 40)
def drawText(text, font, color, x, y):
     img = font.render(text, True, color)
     SCREEN.blit(img, (x,y))

def homeScreen():
    SCREEN.fill(pygame.Color(255,255,255))
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    SCREEN.blit(LOGO_IMAGE,(100,100))
    if start_button.draw(SCREEN):
       return GAME_SCREEN_IDLE
    elif quit_button.draw(SCREEN):
        pygame.quit()
        sys.exit()
    else:
        return HOME_SCREEN

def gameScreenIdle():
    global balence
    SCREEN.fill(pygame.Color(255,255,255))
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    SCREEN.blit(BOARD_BACKGROUND,(250,122.5))
    pygame.draw.rect(SCREEN, "black", baseline)
    SCREEN.blit(BOARDER_IMAGE,(0,0))
    drawText(f"Balance: ${balence}", font,(255,255,255), 200,600)
    drawText(f"Bet Size: ${betsize}", font,(255,255,255), 200,630)
    if spin_button.draw(SCREEN):
          if balence > betsize:
             balence -= betsize
             startGame()
             return GAME_SCREEN_PLAYING_MOVING
    return GAME_SCREEN_IDLE

def startGame():
     global grid
     grid = back.createGrids(baseline)
     return GAME_SCREEN_PLAYING_MOVING

def gameScreenPlayingMoving():
    SCREEN.fill(pygame.Color(255,255,255))
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    SCREEN.blit(BOARD_BACKGROUND,(250,122.5))
    pygame.draw.rect(SCREEN, "black", baseline)
    falling = False
    for row in grid:
         for symbol in row:
              symbol.draw(SCREEN)
              if symbol.falling():
                   falling = True
    SCREEN.blit(BOARDER_IMAGE,(0,0))
    drawText(f"Balance: ${balence}", font,(255,255,255), 200,600)
    drawText(f"Bet Size: ${betsize}", font,(255,255,255), 200,630)
    if falling == True:
         return GAME_SCREEN_PLAYING_MOVING
    else:
         timer1.activate()
         timer2.activate()
         return GAME_SCREEN_PLAYING_IDLE
    
    
def gameScreenPlayingIdle():
    global balence 
    SCREEN.fill(pygame.Color(255,255,255))
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    SCREEN.blit(BOARD_BACKGROUND,(250,122.5))
    pygame.draw.rect(SCREEN, "black", baseline)
    for row in grid:
         for symbol in row:
              if symbol != None:
                    symbol.draw(SCREEN)
    SCREEN.blit(BOARDER_IMAGE,(0,0))
    drawText(f"Balance: ${balence}", font,(255,255,255), 200,600)
    drawText(f"Bet Size: ${betsize}", font,(255,255,255), 200,630)
    if not back.checkGrid():
         if not timer1.active:
              timer1.deactivate()
              print(f"Winnings: {back.winnings}, Multiplier: {back.multi}, Bet Size: {betsize}")
              if back.multi != 0:
                    balence += (back.winnings * back.multi) * betsize
              else:
                   balence += (back.winnings * betsize)
              print(f"Updated Balance: {balence}")
              return GAME_SCREEN_GAME_OVER
    elif back.checkGrid():
         if back.popIslands(grid, timer1, timer2):
              back.tumble(grid, baseline)
              back.refillGrid(grid, baseline)
              return GAME_SCREEN_TUMBLE
    return GAME_SCREEN_PLAYING_IDLE

def gameScreenTumble():
     SCREEN.fill(pygame.Color(255,255,255))
     SCREEN.blit(BACKGROUND_IMAGE, (0,0))
     SCREEN.blit(BOARD_BACKGROUND,(250,122.5))
     pygame.draw.rect(SCREEN, "black", baseline)
     falling = False
     for row in grid:
          for symbol in row: 
               if symbol != None:
                    symbol.draw(SCREEN)
                    if symbol.falling():
                         falling = True
     SCREEN.blit(BOARDER_IMAGE,(0,0))
     drawText(f"Balance: ${balence}", font,(255,255,255), 200,600)
     drawText(f"Bet Size: ${betsize}", font,(255,255,255), 200,630)
     if falling == True:
         return GAME_SCREEN_TUMBLE
     else:
          timer1.activate()
          timer2.activate()
          return GAME_SCREEN_PLAYING_IDLE
     
def gameScreenGameOver():
     global balence 
     SCREEN.fill(pygame.Color(255,255,255))
     SCREEN.blit(BACKGROUND_IMAGE, (0,0))
     SCREEN.blit(BOARD_BACKGROUND,(250,122.5))
     pygame.draw.rect(SCREEN, "black", baseline)
     for row in grid:
          for symbol in row: 
               if symbol != None:
                    symbol.draw(SCREEN)
     SCREEN.blit(BOARDER_IMAGE,(0,0))
     drawText(f"Balance: ${balence}", font,(255,255,255), 200,600)
     drawText(f"Bet Size: ${betsize}", font,(255,255,255), 200,630)
     if back.winnings > 0:
          if back.multi != 0:
               text = font2.render(f"Win ${((back.winnings * back.multi) * betsize)}", True, (255,255,255))
               text_rect = text.get_rect(center=(WIDTH/2, 600))
               SCREEN.blit(text, text_rect)
          else:
               text = font2.render(f"Win ${round((back.winnings * betsize),2)}", True, (255,255,255))
               text_rect = text.get_rect(center=(WIDTH/2, 600))
               SCREEN.blit(text, text_rect)
     if spin_button.draw(SCREEN):
          if balence > betsize:
               balence -= betsize
               timer3.activate()
               return GAME_SCREEN_CLEAR
     else: 
          return GAME_SCREEN_GAME_OVER
     
def gameScreenClear():
     global grid
     SCREEN.fill(pygame.Color(255,255,255))
     SCREEN.blit(BACKGROUND_IMAGE, (0,0))
     SCREEN.blit(BOARD_BACKGROUND,(250,122.5))
     pygame.draw.rect(SCREEN, "black", baseline)
     falling = False
     for row in grid:
          for symbol in row: 
               symbol.draw(SCREEN)
               if symbol.clear(timer3):  
                    falling = True
     SCREEN.blit(BOARDER_IMAGE,(0,0))
     drawText(f"Balance: ${balence}", font,(255,255,255), 200,600)
     drawText(f"Bet Size: ${betsize}", font,(255,255,255), 200,630)
     if not falling:
          grid = back.createGrids(baseline)
          return GAME_SCREEN_PLAYING_MOVING
     else:
          return GAME_SCREEN_CLEAR

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if state == HOME_SCREEN:
         state = homeScreen()
    elif state == GAME_SCREEN_IDLE:
         state = gameScreenIdle()
    elif state == GAME_SCREEN_PLAYING_MOVING:
         state = gameScreenPlayingMoving()
    elif state == GAME_SCREEN_PLAYING_IDLE:
         state = gameScreenPlayingIdle()
    elif state == GAME_SCREEN_TUMBLE:
         state = gameScreenTumble()
    elif state == GAME_SCREEN_GAME_OVER:
         state = gameScreenGameOver()
    elif state == GAME_SCREEN_CLEAR:
         state = gameScreenClear() 
    pygame.display.update()
    timer1.update()
    timer2.update()
    timer3.update()
    
pygame.quit()

#TODO: create money and make winnings
#TODO: Display winnings when popped
#TODO: Display winsize growing throughout the game and then multiply at the end (sweet bonanza dupe)