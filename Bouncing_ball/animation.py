import pygame
from numpy import sqrt,cbrt

# Animation constantes

WIN_WIDTH = 500 # px
WIN_HEIGHT = 500 # px

fen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
COLOR_BG = (255, 87, 51) # RGB
COLOR_DROP = (97, 156, 231) # RGB
Clock = pygame.time.Clock()
FPS = 10
radius = 60 # px

# Oval caracteristics dimensions (arbritrary)
# a0: intial width
# b0: inital heignt
# min_b: Minimal b to go when compressing the ball

a0 = 2 * radius
b0 = 2 * radius

min_b = radius/1.3

# Oval position functions

y0 = 220 - b0 # Start height (arbitrary)

def get_x (a): 
    """
    Need to define a function because a will increase when the drop will 'bounce'
    """

    return (WIN_WIDTH - a) // 2

def get_y (b):
    """
    Needed when the ball is bouncing
    """
    
    return WIN_WIDTH - b

# Event handler (only leaving action take into a count)

def event_leave (events):
    """
    Needed in order to have access to the close windows button
    """

    for e in events:
        if e.type == pygame.QUIT: return True

    return False

# Compute y position

def compute_position (t, factor, y0):
    """
    Factor used to change both ball's speed and direction
    """

    return y0 + factor * t ** 2

# Compute new caractéristics values 

def compute_caracteristics(t, factor, x0):
    """
    Factor used to change both ball's speed and direction
    """

    a0, b0 = x0

    a = a0 + factor * t ** 2
    b = b0 - factor * t ** 2
    
    return int(a), int(b)

# Calculate differente phase times

def get_times (factor):
    """
    To create a time based animation and not a collide based one.
    return the differents value when hiting critical point.
    """

    t1 = sqrt(abs(WIN_HEIGHT - y0 - b0) / factor)
    t2 = t1 + sqrt(abs(b0 - min_b) / factor)
    t3 = t2 + sqrt(abs(min_b - b0) / factor)
    t4 = t3 + t1

    return t1, t2, t3, t4

factor = FPS * 2 # Defining the animation's speed
t1, t2, t3, t4 = get_times(factor)

def get_values (t):
    """
    Calculate the position of the ball according to the current phase
    """

    if t <= t1: # Ball is falling down

        a, b = a0, b0

        x = get_x(a)
        y = compute_position(t, factor, y0)

    elif t <= t2: # COmpression

        a, b = compute_caracteristics(abs(t2 - t), -1 * factor, compute_caracteristics(t1 - t2, factor, [a0, b0]))

        x = get_x(a)
        y = get_y(b)

    elif t <= t3: # Expansion

        a, b = compute_caracteristics(abs(t - t2), -1 * factor, compute_caracteristics(t1 - t2, factor, [a0, b0]))

        x = get_x(a)
        y = get_y(b)

    elif t <= t4: # Ball going back to its original point

        a, b = a0, b0

        x = get_x(a)
        y = compute_position(t4 - t, factor, y0)

    else:
        a, b, x, y = [None] * 4

    return a, b, x, y

t = 0 # The time variable
i = 1 # Just a variable to name my different images files to create the animation

# Infinite loop

while True:
    Clock.tick(FPS) # Force the while loop to execute at the FPS speed
    fen.fill(COLOR_BG) # Reset screen 

    e = pygame.event.get() # Prevents crashes
    if event_leave(e): break # When the close window button is pressed, the application close

    a, b, x, y = get_values(t)
    if a == None: break # The animation end

    rect = pygame.Rect(x, y, a, b) # Define the rect to draw the ellispe in
    pygame.draw.ellipse(fen, COLOR_DROP, rect) # Draw the ellipse inside the rect previously defined

    pygame.image.save(fen, "screenshot/img_{}.png".format(i)) # A bit of code to save the surface and so create the gif
    i += 1

    t +=  1 / FPS
    pygame.display.update() # Update screen

pygame.quit() # To properly quit pygame