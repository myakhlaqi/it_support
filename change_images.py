#!/usr/bin/env python3

from PIL import Image


im = Image("example.jpg")
im.rotate(180).resize((640,480)).save("flipped_and_resized.jpg")
