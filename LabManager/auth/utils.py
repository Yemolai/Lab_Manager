import os
import secrets
from PIL import Image
from LabManager import app


def save_profile_picture(form_picture, image_path):
    """
    Logic to update account pictures. Used on the '/account'
    route. Generates random filename and concatenates to the
    original file extensions before saving it to the system.
    Also resizes the image using the Pillow Package. Returns
    the filename to be applied on the database.
    """
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    pic_filename = random_hex + file_ext
    pic_path = os.path.join(app.root_path, "static/profile_pics", pic_filename)
    
    if image_path != os.path.join(app.root_path, "static/profile_pics", "default.jpg"):
        os.remove(image_path)

    output_size = (125, 125)
    output_pic = Image.open(form_picture)
    output_pic.thumbnail(output_size)
    
    output_pic.save(pic_path)

    return pic_filename, os.path.join("static/profile_pics", pic_filename)
