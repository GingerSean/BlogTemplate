from flask import (render_template , url_for , flash , redirect 
                        , request , Blueprint)
from flask_login import  login_user , current_user , logout_user , login_required
from flaskstarterblog import db
from flaskstarterblog.models import User , BlogPost
from flaskstarterblog.users.forms import LoginForm , UserInfoUpdate , SignupForm
from flaskstarterblog.users.profilePic import add_pic
from werkzeug.local import LocalProxy
from flask import current_app

from werkzeug.security import generate_password_hash

logger = LocalProxy(lambda: current_app.logger)

users = Blueprint('users' , __name__)

@users.route('/logout')
def logout():
        logout_user()
        return redirect(url_for('core.index'))

@users.route('/signup' , methods=['GET' , 'POST'])
def signup():
        form = SignupForm()

        if form.validate_on_submit():
                user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
                
                db.session.add(user)
                db.session.commit()
                flash("now , you are a new member of Spider's web")               
                return redirect(url_for('users.login'))  

        return render_template('signup.html' , form = form)


@users.route('/login' , methods=['GET' , 'POST'])
def login():
        form = LoginForm()

        if form.validate_on_submit():
                
                user = User.query.filter_by(username=form.username.data).first()           
                if User.pass_check(user , form.password.data) and user is not None:
                        login_user(user)
                        return redirect(url_for('core.index'))

                flash("welcome back to Spider's web")
                
                next  = request.args.get('next')
                if next == None or not next[0] == '/':
                        next = url_for('core.index')

                return redirect(next)
        
        return render_template('login.html' , form = form)


@users.route('/profile-update' , methods=['GET' , 'POST'])
@login_required
def profile_update():
        form = UserInfoUpdate()
        if form.validate_on_submit():

                
                current_user.username = form.username.data
                logger.info('%s logged in successfully', form.username.data)
                if form.password.data is not None:
                        current_user.password = generate_password_hash(form.password.data)
                        logger.info('%s logged in successfully', form.password.data)
                if form.profile_pic.data is not None:
                        current_user.profile_pic = add_pic(form.profile_pic.data ,  current_user.username)
                        logger.info('%s logged in successfully', current_user.profile_pic)

                current_user.email = form.email.data
                db.session.commit()
                logger.info('%s %s Dataaaaaas:  successfully',  current_user.username , current_user.password)

                flash('updated')
                return redirect(url_for('users.profile_update'))

        elif request.method == "GET":
                form.username.data = current_user.username
                form.email.data = current_user.email

        profile_img = url_for('static' , filename = 'profilePics/' + current_user.profile_pic)
        return render_template('profile.html' , profile_img=profile_img , form = form)

@users.route('/<username>')
def user_posts(username):
        page = request.args.get('page' , 1 , type=int)
        user =  User.query.filter_by(username = username).first_or_404()
        posts = BlogPost.query.filter_by(author = user).order_by(BlogPost.date.desc()).paginate(page=page , per_page =9)
        
        return render_template('user_posts.html' , posts = posts , user = user)