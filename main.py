import pygame, math

# Initialize the game
pygame.init()

# Set the screen size and constants
size = WIDTH, HEIGHT = 1000, 700
GRAVITY = 9.81
VELOCITY = 100
speed_tank = 5
MAX_HEIGHT = 200

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
ammunition_rect = ammunition.get_rect(bottomleft=(tank_rect.midright))

# Load background image
background = pygame.image.load("assets/background.jpg").convert()
background = pygame.transform.scale(background, size)


"""class Canon(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [0, 0]
        self.start_pos = (0, 0)


    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    
    def shoot(self):
        # Release the ball
        mouse_pos = pygame.mouse.get_pos()
        direction = math.atan2(self.start_pos[1] - mouse_pos[1], self.start_pos[0] - mouse_pos[0])
        speed = 10
        self.velocity = [speed * math.cos(direction), speed * math.sin(direction)]"""

run = True
bullet_fired = False
time_elapsed = 0

while run:
    pygame.time.Clock().tick(30)
    delta_time = 1 / 30

    screen.blit(background, (0, 0))
    screen.blit(tank, tank_rect)
    screen.blit(target, target_rect)
    mouse_pos = pygame.mouse.get_pos()

    dx = mouse_pos[0] - tank_rect.midright[0]
    dy = mouse_pos[1] - tank_rect.midright[1]

    distance = math.sqrt(dx**2 + dy**2)

    if distance > MAX_HEIGHT:
        scale = MAX_HEIGHT / distance
        end_x = tank_rect.midright[0] + dx * scale
        end_y = tank_rect.midright[1] + dy * scale
        pygame.draw.line(screen, (255, 0, 0), tank_rect.midright, (end_x, end_y), 2)
    
    else:
        pygame.draw.line(screen, (255, 0, 0), tank_rect.midright, mouse_pos, 2)

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
        bullet_start_pos = ammunition_rect.center
        theta = math.atan2(bullet_start_pos[1] - mouse_pos[1], bullet_start_pos[0] - mouse_pos[0])
        print(math.degrees(theta))
        time_elapsed = 0
        
    if bullet_fired:
        time_elapsed += delta_time
        ammunition_rect.x += int(VELOCITY * math.cos(theta) * time_elapsed)
        ammunition_rect.y = -int(bullet_start_pos[1] - (VELOCITY * math.sin(theta) * time_elapsed) + (0.5 * GRAVITY * time_elapsed**2))
        screen.blit(ammunition, ammunition_rect)
     
    # Reset bullet if it goes out of bounds
    if ammunition_rect.y > HEIGHT or ammunition_rect.x > WIDTH:
        ammunition_rect.bottomleft = tank_rect.midright
        bullet_fired = False

    pygame.display.update()

