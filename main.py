import pygame, math, random
import tkinter as tk
from Login import *

# Initialize the game
pygame.init()

# Set the screen size and constants
size = WIDTH, HEIGHT = 1000, 700
GRAVITY = -9.8
speed_tank = 2
MAX_HEIGHT = 200
power = 50
angle = 0
run = True
shoot = False
win = False
time = 0
x = 0
y = 0
ammunition_left = 3
level = 1
bird_start_position = (0, random.randint(100, HEIGHT // 3))
hit_bird = False
game_over_state = False

# Initialise the screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tank buster")

def update_power(val):
    """Update the power variable from the Tkinter slider."""
    global power
    power = int(val)


# Create Tkinter window
root = tk.Tk()
root.title("Velocity Control")
root.geometry("300x100")

tk.Label(root, text="Adjust Velocity").pack(pady=5)
slider = tk.Scale(root, from_=10, to=99, orient="horizontal", command=update_power)
slider.set(power)
slider.pack(pady=5)

# Load tank image
tank = pygame.image.load("assets/tank2.png").convert_alpha()
tank = pygame.transform.scale(tank, (150, 150))
tank_rect = tank.get_rect(bottomleft=(0, 600))  #590

# Load target image
target = pygame.image.load("assets/target2.png").convert_alpha()
target = pygame.transform.scale(target, (100, 100))

# Load ammunition image
ammunition = pygame.image.load("assets/ammunition2.png").convert_alpha()
ammunition = pygame.transform.scale(ammunition, (30, 20))

# Load bird image
bird_images = [pygame.image.load("assets/bird_down.png"), pygame.image.load("assets/bird_mid.png"), pygame.image.load("assets/bird_up.png")]

# Load background image
background = pygame.image.load("assets/background.jpg").convert()
background = pygame.transform.scale(background, size)

# Load game over image
game_over = pygame.image.load("assets/game_over.png")
game_over = pygame.transform.scale(game_over, (200, 200))

# Load win image
win_image = pygame.image.load("assets/win_image.jpg")
win_image = pygame.transform.scale(win_image, (200, 200))

l = pygame.mixer.music.load("assets/Sound/background_music.mp3")
l = pygame.mixer.music.set_volume(0.5)
l = pygame.mixer.music.play(-1)


class Ammunition(pygame.sprite.Sprite):
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = tank_rect.midright
        self.ammunition_mask = pygame.mask.from_surface(ammunition)
        self.mask_image = self.ammunition_mask.to_surface()

    @staticmethod
    def path(startx, starty, velocity, ang, time):
        angle = ang
        velx = math.cos(angle) * velocity
        vely = math.sin(angle) * velocity

        distX = velx * time
        distY = (vely * time) + ((GRAVITY * (time)**2)/2)

        newx = round(distX + startx)
        newy = round(starty - distY)

        return (newx, newy)
    
    def get_height(self):
        return self.rect.height
    

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.vel = 2
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.bird_mask = pygame.mask.from_surface(bird_images[0])
        self.mask_image = self.bird_mask.to_surface()
        self.image_index = 0

    def update(self):
        # Animate Bird
        self.image_index += 1

        if self.image_index >= 30:
            self.image_index = 0

        self.image = bird_images[self.image_index // 10]
        self.vel = 2


class Target(pygame.sprite.Sprite):
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomright = (WIDTH/1.1, 7 * HEIGHT // 8.8)
        self.target_mask = pygame.mask.from_surface(target)
        self.mask_image = self.target_mask.to_surface()

        self.start_x = self.rect.x  # Store the initial x position
        self.time_counter = 0   


def redrawWindow(game_over_state):
    if game_over_state:
        screen.fill((0, 0, 128))
        screen.blit(game_over, (WIDTH//2.5, HEIGHT//3))
        target_object.rect.bottomright = (WIDTH/1.1, 7 * HEIGHT // 8.8)
        
    else:
        screen.blit(background, (0, 0))
        screen.blit(tank, tank_rect)
        screen.blit(target_object.image, target_object.rect)

        font = pygame.font.Font("assets/fonts/Montserrat.ttf", 30)
        text = font.render(f"Velocity: {power}", True, (0, 0, 255))
        screen.blit(text, (WIDTH*0.84, 0))

        font2 = pygame.font.Font("assets/fonts/Montserrat.ttf", 30)
        text2 = font2.render(f"Level: {level}", True, (0, 0, 255))
        screen.blit(text2, (0, 0))

        font = pygame.font.Font("assets/fonts/Montserrat.ttf", 30)
        text = font.render(f"Ammunitions used: {ammunition_left}", True, (0, 0, 255))
        screen.blit(text, (WIDTH//3, 0))

        if shoot and not hit and not hit_bird:
            screen.blit(ammunition_object.image, ammunition_object.rect)

        if level == 3:
            screen.blit(bird.image, bird.rect)

        if level == 4:
            screen.blit(bird.image, bird.rect)
            screen.blit(bird1.image, bird1.rect)
            screen.blit(bird2.image, bird2.rect)

        if level == 5:
            global win
            win = True
            screen.fill((0, 0, 0))
            screen.blit(win_image, (WIDTH//2.5, HEIGHT//2.5))
            font3 = pygame.font.Font("assets/fonts/Montserrat.ttf", 30)
            text3 = font3.render(f"Press R to restart", True, (0, 0, 255))
            screen.blit(text3, (0, 0))
            game_over_state = True
        
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

        return (end_x, end_y)
    
    else:
        pygame.draw.line(screen, (255, 0, 0), start_pos, mouse_pos, 2)

        return mouse_pos
        

def findAngle(pos):
    sX = ammunition_object.rect.x
    sY = ammunition_object.rect.y

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

    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle


def move_object(start, object, vel):
    if level == 5:
        object.time_counter += 0.05  
        amplitude = 100            
        object.rect.x = object.start_x + amplitude * math.sin(object.time_counter)

    else:
        if object.rect.y <= 0 or object.rect.y >= start:
            vel = -vel
        object.rect.y += vel

    return vel


def randomise_y(bird, bird_objects):
    new_y = random.choice(range(100, HEIGHT // 2, 40))

    while new_y in [b.rect.y for b in bird_objects]:
        new_y = random.choice(range(100, HEIGHT // 2, 40))

    bird.rect.y = new_y


def bird_update(bird_objects):
    for bird in bird_objects:
        bird.rect.x += bird.vel

        if bird.rect.x > WIDTH:
            bird.rect.x = 0

            randomise_y(bird, bird_objects) 

        bird.update()

hit = False  
ammunition_object = Ammunition(ammunition)
bird = Bird()
bird1 = Bird()
bird2 = Bird()
target_object = Target(target)
start_pos = target_object.rect.y
vel = (2**level)

while run:
    pygame.time.Clock().tick(200)

    if level == 2:
        vel = move_object(start_pos, target_object, vel)

    if level == 3:
        vel = move_object(start_pos, target_object, vel)
        bird_update([bird])

        # vel = move_object(start_pos, target_object, vel)
        # bird.rect.x += bird.vel

        # if bird.rect.x > WIDTH:
        #     bird.rect.x = 0
        #     bird.rect.y = random.randint(100, HEIGHT // 2)

        # bird.update()

    if level == 4:
        vel = move_object(start_pos, target_object, vel)
        bird_update([bird, bird1, bird2])


    if shoot:
        if 0 - ammunition_object.get_height() < ammunition_object.rect.y < HEIGHT and 0 < ammunition_object.rect.x < WIDTH + ammunition_object.get_height():
            time += 0.1
            po = ammunition_object.path(x, y, power, angle, time)
            ammunition_object.rect.x = po[0]
            ammunition_object.rect.y = po[1]

            birds = [bird, bird1, bird2]

            for bird_obj in birds:
                offset_x = bird_obj.rect.x - ammunition_object.rect.x
                offset_y = bird_obj.rect.y - ammunition_object.rect.y
        
                if ammunition_object.ammunition_mask.overlap(bird_obj.bird_mask, (offset_x, offset_y)) and not hit_bird:
                    hit_bird = True
                    ammunition_object.rect.bottomleft = tank_rect.midright

            offset_x = target_object.rect.x - ammunition_object.rect.x
            offset_y = target_object.rect.y - ammunition_object.rect.y

            if ammunition_object.ammunition_mask.overlap(target_object.target_mask, (offset_x, offset_y)) and not hit:
                hit = True
                level += 1
                vel = (2**level)
                ammunition_left = 3
        else:
            shoot = False
            time = 0
            ammunition_object.rect.bottomleft = tank_rect.midright
            hit_bird = False
            hit = False
            
            if ammunition_left == 0 and not shoot:
                game_over_state = True

    redrawWindow(game_over_state)
    draw_line(pygame.mouse.get_pos())    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    root.update()

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT] and 0 < tank_rect.x and not game_over_state:        
        tank_rect.x -= speed_tank 

    if keys_pressed[pygame.K_RIGHT] and tank_rect.x < WIDTH/15 and not game_over_state:
        tank_rect.x += speed_tank

    if keys_pressed[pygame.K_r] and game_over_state:
        game_over_state = False
        ammunition_left = 3
        level = level

        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/Sound/background_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    if keys_pressed[pygame.K_SPACE] and not shoot and ammunition_left > 0:
        shoot = True
        ammunition_left -= 1

        x = ammunition_object.rect.x
        y = ammunition_object.rect.y
        pos = pygame.mouse.get_pos()
        angle = findAngle(pos)
