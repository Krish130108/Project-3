import pygame, math

# Initialize the game
pygame.init()

# Set the screen size and constants
size = WIDTH, HEIGHT = 1000, 700
GRAVITY = -9.81
velocity = 0
speed_tank = 5
MAX_HEIGHT = 200
theta = 0
run = True
bullet_fired = False
time = 0
x = 0
y = 0

# Initialise the screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tank buster")

# Load tank image
tank = pygame.image.load("assets/tank.png").convert_alpha()
tank = pygame.transform.scale(tank, (150, 150))
tank_rect = tank.get_rect(bottomleft=(0, 590))

# Load target image
target = pygame.image.load("assets/target.png").convert_alpha()
target = pygame.transform.scale(target, (100, 100))
target_rect = target.get_rect(bottomright=(1000, 7 * HEIGHT // 9))

# Load ammunition image
ammunition = pygame.image.load("assets/ammunition.png").convert_alpha()
ammunition = pygame.transform.scale(ammunition, (40, 40))

# Load background image
background = pygame.image.load("assets/background.jpg").convert()
background = pygame.transform.scale(background, size)


class Ammunition(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    @staticmethod
    def path(startx, starty, velocity, ang, time):
        velx = math.cos(ang) * velocity
        vely = math.sin(ang) * velocity

        distX = velx * time
        distY = (vely * time) + ((-9.81 * (time)**2)/2)

        newx = round(distX + startx)
        newy = round(starty - distY)

        return (newx, newy)
    

def redrawWindow():
    screen.blit(background, (0, 0))
    screen.blit(tank, tank_rect)
    screen.blit(target, target_rect)
    pygame.display.update()


def draw_line(mouse_pos, start_pos=tank_rect.midright):
    dx = mouse_pos[0] - tank_rect.midright[0]
    dy = mouse_pos[1] - tank_rect.midright[1]

    distance = math.sqrt(dx**2 + dy**2)

    if distance > MAX_HEIGHT:
        scale = MAX_HEIGHT / distance
        end_x = tank_rect.midright[0] + dx * scale
        end_y = tank_rect.midright[1] + dy * scale
        pygame.draw.line(screen, (255, 0, 0), start_pos, (end_x, end_y), 2)
    
    else:
        pygame.draw.line(screen, (255, 0, 0), start_pos, mouse_pos, 2)

    return (end_x, end_y)


def findAngle(pos):
    sX = ammunition.x
    sY = ammunition.y

    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)

    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle

    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)

    else:
        angle = (math.pi * 2) - angle
    
    return angle
        

ammunition = Ammunition(bottomleft=(tank_rect.midright))

while run:
    pygame.time.Clock().tick(30)

    if shoot:
        if ammunition.rect.y < 700 - HEIGHT:
            time += 0.05
            po = ammunition.path(x, y, velocity, theta, time)
            ammunition.rect.x = po[0]
            ammunition.rect.y = po[1]
        else:
            shoot = False
            ammunition.rect.bottomleft = tank_rect.midright

    mouse_pos = pygame.mouse.get_pos()
    line = draw_line(mouse_pos)
    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT] and tank_rect.x > 0:
        tank_rect.x -= speed_tank 

    if keys_pressed[pygame.K_RIGHT]:
        tank_rect.x += speed_tank

    if keys_pressed[pygame.K_SPACE] and not bullet_fired:
        bullet_fired = True
        x = ammunition.rect.x
        y = ammunition.rect.y
        time = 0
        power = 20
        theta = findAngle(mouse_pos)

    pygame.display.update()

