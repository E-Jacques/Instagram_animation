from PIL import Image
from os import listdir

n = len(listdir("screenshot"))

im_ls = [Image.open("screenshot/img_{}.png".format(i)) for i in range(1, n+1)]
im_ls[0].save("out.gif", save_all=True, append_images=im_ls[1:], loop=0, optimize=False, duration=5)