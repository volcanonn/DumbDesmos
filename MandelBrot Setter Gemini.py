import pygame
import sys
import numpy as np
import time
import matplotlib.pyplot as plt

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mandelbrot Set")

zoom=1
BaseIterations = 100
pos = [0,0]


Maxiterations = BaseIterations

def Mandelbrot():
    a = np.linspace(-1/zoom-pos[1], 1/zoom-pos[1], WINDOW_HEIGHT).reshape(1, -1)
    b = np.linspace(-1/zoom+pos[0], 1/zoom+pos[0], WINDOW_WIDTH).reshape(-1, 1)
    c = a + b * 1j
    z = np.zeros_like(c)
    iterations = np.zeros(c.shape, dtype=int)
    for _ in range(Maxiterations):
        not_escaped = np.abs(z) < 2
        if not not_escaped.any():
            break
        iterations[not_escaped] += 1
        z[not_escaped] = z[not_escaped]**2 + c[not_escaped]
    iterations[iterations == Maxiterations] = 0
    cmap = plt.get_cmap('plasma')
    normalized_iterations = np.where(iterations > 0, iterations / Maxiterations, 0)
    rgba_image = cmap(normalized_iterations)
    rgb_image = (rgba_image[:, :, :3] * 255).astype(np.uint8)
    rgb_image[iterations == 0] = [0, 0, 0] 
    return rgb_image

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            zoom += event.y/10*zoom
            Maxiterations = max(int(BaseIterations*np.log(zoom)/np.log(3)),BaseIterations)
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w:
                    pos[1] += 1/zoom/10
                case pygame.K_s:
                    pos[1] -= 1/zoom/10
                case pygame.K_a:
                    pos[0] -= 1/zoom/10
                case pygame.K_d:
                    pos[0] += 1/zoom/10
                
    # Drawing
    start = time.time()
    pixels = pygame.surfarray.pixels3d(screen)
    pixels[:,:,:] = Mandelbrot()
    del pixels
    pygame.display.flip()
    print(f"FPS: {round(1/(time.time()-start))}, Iterations: {Maxiterations}")

# Quit Pygame
pygame.quit()
sys.exit()