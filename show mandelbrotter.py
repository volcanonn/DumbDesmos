import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

WINDOW_WIDTH = 4320
WINDOW_HEIGHT = 7680

zoom=2
Maxiterations = 300
pos = [-1,0]

start = time.time()

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
image = Image.fromarray(rgb_image)
print(time.time()-start)
image.save("Cool Mandel.png")