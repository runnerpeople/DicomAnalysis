#!python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw

def edit_image(filename,data,version=None):
    im = Image.open(filename)

    draw = ImageDraw.Draw(im)
    draw.line([(0, 0),(100,100)], fill=(255,0,0,128))
    draw.line([(0,100),(100,0)], fill=(0,255,0,128))
    del draw

    new_filename = filename.replace(".jpg","v1.jpg")

    im.save(new_filename)
    return new_filename
