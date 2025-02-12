import pygame, sys, random

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()

def image_update():
    screen.blit(bg,(fl_xp,0))
    screen.blit(bg,(fl_xp + 288,0))
    screen.blit(fl,(fl_xp,450))
    screen.blit(fl,(fl_xp + 288,450))
    
def create_pipe():
    rc = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350, rc))
    top_pipe = pipe_surface.get_rect(midbottom = (350, rc -150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if birdr.colliderect(pipe):
            ds.play()
            return False
    if birdr.top <= -50 or birdr.bottom >= 450:
            ds.play()
            return False
    return True

def animations(bird):
    new_bird = pygame.transform.rotozoom(bird, -birdm * 6, 1)
    return new_bird

def birdpoz(poz):
    new_bird =  pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
    if poz % 3 == 1:
        new_bird =  pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
    if poz % 3 == 2:
        new_bird =  pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
    return new_bird
        
def score_display(game_state):
    if game == True:
        score_surface = game_font.render(str(int(score)) ,True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface, score_rect)
    if game == False:
        score_surface = game_font.render('Score: ' + str(int(score)) ,True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface, score_rect)
        hscore_surface = game_font.render('High Score: ' + str(int(high_score)) ,True, (255,255,255))
        hscore_rect = hscore_surface.get_rect(center = (144,425))
        screen.blit(hscore_surface, hscore_rect)

def hs():
    if score > high_score:
        return score
    return high_score
    
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf' ,20)
fs = pygame.mixer.Sound('sound/sfx_wing.wav')
ds = pygame.mixer.Sound('sound/sfx_hit.wav')
ss = pygame.mixer.Sound('sound/sfx_point.wav')
sc = 100
cb = 0

bg = pygame.image.load('assets/background-day.png').convert()
fl = pygame.image.load('assets/base.png').convert()
sfl = pygame.image.load('assets/base.png').convert()
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
bird = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
go_screen = pygame.image.load('assets/message.png').convert_alpha()

fl_xp = 0
gravity = 0.25
jumpp = 7
birdm = 0
game = True
score = 0
high_score = 0
poz = 0

pipe_list = []
pipe_height = [200, 300, 400]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
CA = 0
birdr = bird.get_rect(center = (50,256))
gore = go_screen.get_rect(center = (144, 256))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()  
            sys.exit()

            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fs.play();
                birdm = 0
                birdm -= jumpp

                
            if event.key == pygame.K_SPACE and game == False:
                 game = True
                 birdr.center = (50, 256)
                 birdm = 0
                 score = 0
                 cb = 0
                 bg = pygame.image.load('assets/background-day.png').convert()
                 pipe_list.clear()

           
        if event.type == SPAWNPIPE:
              pipe_list.extend(create_pipe())
              
    if CA >= 500:
        poz += 1
        CA = 0
    bird = birdpoz(poz)
    image_update()
    if game:
        if fl_xp <= -288:
            fl_xp = 0
        fl_xp -=  1

        birdm += gravity
        rotated_bird = animations(bird)
        birdr.centery += int(birdm)
        screen.blit(rotated_bird,birdr)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        cb += 1
        sc -= 1
        game = check_collision(pipe_list)
        CA += 120
        score_display('actual game')
        if cb == 1000:
            bg = pygame.image.load('assets/background-night.png').convert()
        if cb == 2000:
            bg = pygame.image.load('assets/background-day.png').convert()
            cb = 0
        if sc <= 0:
            ss.play()
            sc = 100
    else:
        screen.blit(go_screen, gore)
        high_score = hs()
        score_display("game over")
        
    pygame.display.update()
    clock.tick(120)
