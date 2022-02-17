#!/usr/bin/env python3

from PIL import Image
import os

def get_image_paths(mypath):
    return [ os.path.abspath(os.path.join(mypath, f)) 
    for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f)) and f.startswith("ic_")]

def convert_image(image_path_list, save_path):
    for image_path in image_path_list:
        pic = Image.open(image_path)
        new_pic=os.path.abspath(os.path.join(save_path,os.path.basename(image_path)))
        print(new_pic)
        pic.rotate(-90).resize((128,128)).convert("RGB").save(new_pic,"JPEG")

   
print(get_image_paths("./images"))
convert_image(get_image_paths("./images"), "/opt/icons")
