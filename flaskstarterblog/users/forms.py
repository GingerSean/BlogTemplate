from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flaskstarterblog.models import User
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm ( FlaskForm ):
        username = StringField ('User name' , validators=[DataRequired()] )
        password = PasswordField ('Password' , validators=[DataRequired()] )
        submit = SubmitField ('Login')

class SignupForm ( FlaskForm ):
        email = StringField ( 'Email' , validators=[DataRequired() , Email()] )
        username = StringField ( 'User name' , validators=[DataRequired()] )
        password = PasswordField ( 'Password' , validators=[DataRequired() , EqualTo('password_retype' , message='passwords must match...' )] )
        password_retype = PasswordField ( 'Confirm Password' , validators=[DataRequired()] )
        submit = SubmitField ('Signup')

        def EmailCheck(self , field):
                if User.query.filter_by(email=field.data).first():
                        raise ValidationError("Your Email is exist in spider's Web")

        
        def UsernameCheck(self , field):
                if User.query.filter_by(username=field.data).first():
                        raise ValidationError("Your username is exist in spider's Web")

class UserInfoUpdate(FlaskForm):

        email = StringField ( 'change Email' , validators=[Email()] )
        username = StringField ( 'change User name' , validators=[] )
        password = PasswordField ( 'change Password' , validators=[ EqualTo('password_retype' , message='passwords must match...' )] )
        password_retype = PasswordField ( 'Confirm Password' )
        profile_pic = FileField ('change profile picture' , validators=[  FileAllowed(['jpeg' , 'png' , 'jpg'])  ])
        submit = SubmitField ('update')

        def EmailCheck(self , field):
                if User.query.filter_by(email=field.data).first():
                        raise ValidationError("Your Email is exist in spider's Web")

        
        def UsernameCheck(self , field):
                if User.query.filter_by(username=field.data).first():
                        raise ValidationError("Your username is exist in spider's Web")