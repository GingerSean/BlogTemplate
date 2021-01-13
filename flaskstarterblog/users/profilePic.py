from PIL import Image
from flask import url_for , current_app
import os

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def add_pic(pic , username):
        filename = pic.filename
        pic_type = filename.split('.')[-1]
        store_pic = str(username)+'.'+pic_type
        print(store_pic)
        save_path = os.path.join(current_app.root_path , 'static\profilePics' , store_pic)
        size = (200 , 200)
        pict = Image.open(pic)
        pict = crop_center(pict, min(pict.size), min(pict.size))
        pict = pict.resize(size)
        pict.save(save_path)

        return store_pic
