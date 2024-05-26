from flask import request, url_for, current_app
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
from PIL import Image
import os
import requests
from flaskstarterblog.config import Config
from flaskstarterblog import app
from urllib.parse import urljoin



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_image_and_get_url(file, blog_id, title, is_temp_file=False):
    # Construct the folder name based on the blog post ID and title
    upload_folder = current_app.config['BLOG_IMAGE_UPLOAD_FOLDER']
    folder_name = f"{blog_id}_{title.replace(' ', '_')}"
    folder_path = os.path.join(upload_folder, folder_name)

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    if is_temp_file:
        # If the file is a temporary file opened from a path
        filename = os.path.basename(file.name)
        dest_filepath = os.path.join(folder_path, filename)
        # Copy the file to the destination path
        with open(file.name, 'rb') as src_file:
            with open(dest_filepath, 'wb') as dest_file:
                dest_file.write(src_file.read())
        # Delete the temporary file
        os.remove(file.name)
    else:
        # If the file is an uploaded file via Flask form
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dest_filepath = os.path.join(folder_path, filename)
            file.save(dest_filepath)
        else:
            return None  # Return None if the file is not allowed

    # Construct the image URL
    image_url = url_for('static', filename=f'blogposts/images/{folder_name}/{filename}')
    return image_url

