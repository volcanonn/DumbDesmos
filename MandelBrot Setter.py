import pygame
import sys
import numpy as np
import time

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mandelbrot Set")

zoom=1
BaseIterations = 10
pos = [0,0]

def Mandelbrot(y,x):
    y,x = x/(WINDOW_WIDTH*zoom)-(.5/zoom)+pos[1],y/(WINDOW_HEIGHT*zoom)-(.5/zoom)+pos[0]
    a,b = x,y
    Iterations = np.zeros((WINDOW_WIDTH,WINDOW_HEIGHT))
    Maxiterations = max(int(BaseIterations*zoom),BaseIterations)
    for _ in range(Maxiterations):
        x,y = pow(x,2)-pow(y,2)-a, 2*x*y-b
        Iterations += np.abs(x+y*1j) < 2
    return Iterations*255/Maxiterations

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            zoom += event.y/10*zoom
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w:
                    pos[1] -= 1/zoom/10
                case pygame.K_s:
                    pos[1] += 1/zoom/10
                case pygame.K_a:
                    pos[0] -= 1/zoom/10
                case pygame.K_d:
                    pos[0] += 1/zoom/10
                
    # Drawing
    start = time.time()
    pixels = pygame.surfarray.pixels2d(screen)
    pixels[:,:] = np.fromfunction(Mandelbrot,(WINDOW_WIDTH,WINDOW_HEIGHT))
    del pixels
    #print("Update")
    # Update the display
    pygame.display.flip()
    print("FPS:",round(1/(time.time()-start)))

# Quit Pygame
pygame.quit()
sys.exit()