import os
import secrets
from typing import IO
from PIL import Image, UnidentifiedImageError
from pavshop import app
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)

    output_size = (125, 125)
    try:
        img = Image.open(form_picture)
    except UnidentifiedImageError:
        print('No image data')
    # i = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

# pip install pillow