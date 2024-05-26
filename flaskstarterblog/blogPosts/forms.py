from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class BlogPostInfo(FlaskForm):
    title = StringField('Blog Title', validators=[DataRequired()])
    text = TextAreaField('Blog Text')
    base_image = FileField('Base Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    synopsis = TextAreaField('Synopsis')
    submit = SubmitField('Post')
