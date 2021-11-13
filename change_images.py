#!/usr/bin/env python3
import os
from PIL import Image


def get_image_paths(mypath):
    return [ os.path.abspath(os.path.join(mypath, f)) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    

#print(onlyfiles)
#os.mkdir("./new_images")
def convert_image(image_path_list, save_path):
    for image_path in image_path_list:
        pic = Image.open(image_path)
        new_pic=os.path.abspath(os.path.join(save_path,os.path.basename(image_path)))
        pic.rotate(-90).resize((128,128)).convert("RGB").save(new_pic,"JPEG")

convert_image(get_image_paths("./image"), "./image/new_images")