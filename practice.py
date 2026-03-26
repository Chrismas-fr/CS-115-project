# importing files
import pygame

pygame.init()

# setting screen size
screen = pygame.display.set_mode((640, 640))

# importing image
boxandstick_img = pygame.image.load('boxandstick.png').convert()

# scaling image
boxandstick_img = pygame.transform.scale(boxandstick_img,
                                         (boxandstick_img.get_width() * 0.5,
                                         boxandstick_img.get_height() * 0.5))

font = pygame.font.Font(None, size=30)

# game loop variables
running = True
x = 0
clock = pygame.time.Clock()
delta_time = 0.1
moving = False

while running:
    # fills background
    screen.fill((255, 255, 255))

    # drawing image to screen
    screen.blit(boxandstick_img, (x, 30))

    # hitbox of image, which is placed at the same location and uses the same width and height
    hitbox = pygame.Rect(x, 30, boxandstick_img.get_width(), boxandstick_img.get_height())

    # mouse cursor position
    mpos = pygame.mouse.get_pos()

    # collision detection
    target = pygame.Rect(300, 0, 160, 280) #rectangle in middle of screen
    collision = hitbox.colliderect(target) # checking collision of image and rect
    m_collision = target.collidepoint(mpos) # checking collission of mouse and rect
    pygame.draw.rect(screen, (255 * collision, 255 * m_collision, 0), target) # draws rect to screen, and changes colors with collisions

    # moves image
    if moving:
        x += 50 * delta_time

    # text rendering
    text = font.render('Hello World!', True, (0, 0, 0))
    screen.blit(text, (300, 100))

    # closes game, and handles key movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving = False

    # renders full screen
    pygame.display.flip()

    # sets delta_time
    delta_time = clock.tick(180) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

# closes game when game loop is over
pygame.quit()