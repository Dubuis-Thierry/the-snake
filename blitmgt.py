"""
Blit management
Simplifies the process of blitting on screen and rendering text
"""

from constants import *

def text_img(text, font="small", color=(200, 200, 200)):
    return FONTS[font].render(text, True, color)


def blit_centered(img, offset_x=0, offset_y=0):
    x, y = img.get_size()
    get_display().blit(img, (W_WIDTH//2-x//2 + offset_x, W_HEIGHT//2-y//2+offset_y))