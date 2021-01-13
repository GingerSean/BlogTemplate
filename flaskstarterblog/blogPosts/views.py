
from flask import abort , render_template , url_for , flash , request , redirect , Blueprint
from flask_login import current_user , login_required
from flaskstarterblog import db
from flaskstarterblog.models import BlogPost
from flaskstarterblog.blogPosts.forms import BlogPostInfo

blog_posts = Blueprint('blog_posts' , __name__)

@blog_posts.route('/new_post' , methods=['GET' , 'POST'])
@login_required
def create_post():
        form = BlogPostInfo()
        if form.validate_on_submit():
                blog_post = BlogPost(title = form.title.data, text=form.text.data, userId=current_user.id )

                db.session.add(blog_post)
                db.session.commit()
                flash('Posted!!')
                return redirect(url_for('core.index'))

        return render_template('new_post.html' , form = form)


@blog_posts.route('/<int:blog_id>')
def blog_post(blog_id):
        blog_post = BlogPost.query.get_or_404(blog_id)
        return render_template('blog_post.html' , title = blog_post.title 
                                ,date = blog_post.date , post = blog_post)


@blog_posts.route('/<int:blog_id>/update' , methods=['GET' , 'POST'])
@login_required
def update_post(blog_id):
        blog_post = BlogPost.query.get_or_404(blog_id)

        if blog_post.author.username != current_user.username:
               return abort(403, description="sdsdsdsd")

        form = BlogPostInfo()
        if form.validate_on_submit():

                blog_post.title = form.title.data
                blog_post.text = form.text.data
                db.session.commit()
                
                flash('updated')

                return redirect(url_for('blog_posts.blog_post' , blog_id = blog_post.id ))

        elif request.method == 'GET' :
                form.title.data = blog_post.title
                form.text.data = blog_post.text

        return render_template('new_post.html' , title='Update' , form = form)

@blog_posts.route('/<int:blog_id>/delete' , methods=['GET' , 'POST'])
@login_required
def delete_post(blog_id):
        blog_post = BlogPost.query.get_or_404(blog_id)

        if blog_post.author.username != current_user.username:
               return abort(403, description="sdsdsdsd")
        
        db.session.delete(blog_post)
        db.session.commit()
        flash('deleted')
        return redirect(url_for('core.index'))






