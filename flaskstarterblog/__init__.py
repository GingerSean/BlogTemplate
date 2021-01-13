from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os




app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

####### DB Setup ##################
directory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join (directory , 'dbdata.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

####### Login manager ############
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'



####### Blueprint register########
from flaskstarterblog.core.views import core
from flaskstarterblog.errors.errorHnd import err_pages
from flaskstarterblog.users.views import users
from flaskstarterblog.blogPosts.views import blog_posts

app.register_blueprint(core)
app.register_blueprint(err_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
