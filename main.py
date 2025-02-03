import pygame, math
import tkinter as tk

# Initialize the game
pygame.init()

# Set the screen size and constants
size = WIDTH, HEIGHT = 1000, 700
GRAVITY = -4.9
speed_tank = 2
MAX_HEIGHT = 200
power = 10
angle = 0
run = True
shoot = False
time = 0
x = 0
y = 0

# Initialise the screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tank buster")

def update_power(val):
    """Update the power variable from the Tkinter slider."""
    global power
    power = int(val)


# Create Tkinter window
root = tk.Tk()
root.title("Power Control")
root.geometry("300x100")

tk.Label(root, text="Adjust Power").pack(pady=5)
slider = tk.Scale(root, from_=10, to=100, orient="horizontal", command=update_power)
slider.set(power)
slider.pack(pady=5)

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
        self.rect.bottomleft = tank_rect.midright

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
    

def redrawWindow():
    screen.blit(background, (0, 0))
    screen.blit(tank, tank_rect)
    screen.blit(target, target_rect)

    font = pygame.font.Font("assets/fonts/Montserrat.ttf", 36)
    text = font.render(f"Power: {power}", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))

    if shoot:
        screen.blit(ammunition_object.image, ammunition_object.rect)

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
        
        
ammunition_object = Ammunition(ammunition)

while run:
    pygame.time.Clock().tick(200)

    if shoot:
        if 0 - ammunition_object.get_height() < ammunition_object.rect.y < HEIGHT and 0 < ammunition_object.rect.x < WIDTH + ammunition_object.get_height():
            time += 0.1
            po = ammunition_object.path(x, y, power, angle, time)
            ammunition_object.rect.x = po[0]
            ammunition_object.rect.y = po[1]
        else:
            shoot = False
            time = 0
            ammunition_object.rect.bottomleft = tank_rect.midright

    line = pygame.draw.line(screen, (0, 0, 0), WIDTH/5, 0, 1)
    redrawWindow()
    draw_line(pygame.mouse.get_pos())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    root.update()

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT] and 0 < tank_rect.x < line:
        tank_rect.x -= speed_tank 

    if keys_pressed[pygame.K_RIGHT]:
        tank_rect.x += speed_tank

    if keys_pressed[pygame.K_SPACE] and not shoot:
        shoot = True
        x = ammunition_object.rect.x
        y = ammunition_object.rect.y
        #power = 70
        pos = pygame.mouse.get_pos()
        angle = findAngle(pos)
