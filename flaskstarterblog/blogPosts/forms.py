from flask_wtf import FlaskForm
from sqlalchemy.sql.elements import RollbackToSavepointClause
from wtforms import StringField , SubmitField , TextAreaField
from wtforms.validators import DataRequired

class BlogPostInfo(FlaskForm):
        title = StringField( 'Blogs title' , validators=[DataRequired()])
        text = TextAreaField( 'Blogs text' , validators=[DataRequired()])
        submit = SubmitField( ' post')
        