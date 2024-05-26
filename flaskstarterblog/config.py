import os

class Config:
    SECRET_KEY = 'mysecret'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    BLOG_IMAGE_UPLOAD_FOLDER = 'flaskstarterblog/static/blogposts/images'

    # SQLite database configuration
    directory = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(directory, 'dbdata.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False