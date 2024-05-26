
from flask import abort , render_template , url_for , flash , request , redirect , Blueprint, current_app
from flask_login import current_user , login_required
import re
import os
from werkzeug.utils import secure_filename
from flaskstarterblog import db, app
from flaskstarterblog.models import BlogPost
from flaskstarterblog.blogPosts.forms import BlogPostInfo
from flaskstarterblog.blogPosts.utils import save_image_and_get_url


blog_posts = Blueprint('blog_posts' , __name__)

@blog_posts.route('/new_post' , methods=['GET' , 'POST'])
@login_required
def create_post():
    form = BlogPostInfo()
    if form.validate_on_submit():
        # Create a new blog post instance
        blog_post = BlogPost(
            title=form.title.data,
            synopsis=form.synopsis.data,
            text='',  # Initialize text argument as empty string
            userId=current_user.id
        )

        # Add the blog post to the database session
        db.session.add(blog_post)
        db.session.commit()

        # Get the blog post ID after it's been saved to the database
        blog_id = blog_post.id

        # Handle base image upload
        base_image_url = None
        if form.base_image.data:
            # Save and get the URL of the base image
            base_image_url = save_image_and_get_url(form.base_image.data, blog_id, blog_post.title)

        # Handle text content with images
        text_with_images = form.text.data

        # Extract image URLs from the text content
        image_urls = re.findall(r'<img.*?src="(.*?)".*?>', text_with_images)

        # Process each image URL
        for image_url in image_urls:
            # Extract the relative path from the image URL
            relative_path = image_url[len(url_for('static', filename='')):]
            image_file_path = os.path.join(current_app.static_folder, relative_path)

            # Check if the image file exists
            if os.path.exists(image_file_path):
                # Open the image file from the temporary folder
                with open(image_file_path, 'rb') as image_file:
                    # Save and get the URL of each image
                    new_image_url = save_image_and_get_url(image_file, blog_id, blog_post.title, is_temp_file=True)
                    # Replace original URL with new URL in the text content
                    text_with_images = text_with_images.replace(image_url, new_image_url)
            else:
                print(f"Image file '{image_url}' not found.")

        # Update the blog post with the base image URL and text content
        blog_post.base_image = base_image_url
        blog_post.text = text_with_images  # Update text content
        db.session.commit()

        flash('Posted successfully!')
        return redirect(url_for('core.index'))
    else:
        print("Form validation failed:", form.errors)

    return render_template('new_post.html', form=form)


def remove_images_from_temp_folder(image_names):
    temp_folder = os.path.join(app.static_folder, 'blogposts/temp')
    for image_name in image_names:
        temp_image_path = os.path.join(temp_folder, image_name)
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)



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
        return abort(403, description="Unauthorized to edit this post")

    form = BlogPostInfo()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.synopsis = form.synopsis.data

        # Check if a new base image file was uploaded and update the image URL
        if form.base_image.data:
            image_url = save_image_and_get_url(form.base_image.data, blog_id, blog_post.title)
            blog_post.base_image = image_url

        # Handle text content with images
        text_with_images = form.text.data

        # Extract image URLs from the text content
        image_urls = re.findall(r'<img.*?src="(.*?)".*?>', text_with_images)

        # Process each image URL
        for image_url in image_urls:
            # Extract the relative path from the image URL
            relative_path = image_url[len(url_for('static', filename='')):]
            image_file_path = os.path.join(current_app.static_folder, relative_path)

            # Check if the image file exists
            if os.path.exists(image_file_path):
                # Open the image file from the temporary folder
                with open(image_file_path, 'rb') as image_file:
                    # Save and get the URL of each image
                    new_image_url = save_image_and_get_url(image_file, blog_id, blog_post.title, is_temp_file=True)
                    # Replace original URL with new URL in the text content
                    text_with_images = text_with_images.replace(image_url, new_image_url)
            else:
                print(f"Image file '{image_url}' not found.")

        # Update the blog post with the new text content
        blog_post.text = text_with_images

        db.session.commit()

        flash('Post updated successfully!')
        return redirect(url_for('blog_posts.blog_post', blog_id=blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        form.synopsis.data = blog_post.synopsis

    return render_template('new_post.html', title='Update', form=form)


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









@blog_posts.route('/upload/image', methods=['POST'])
def upload_image():
    # Get the uploaded file from the request
    uploaded_file = request.files['upload']

    # Save the file to a temporary holding folder
    temp_folder = os.path.join(app.static_folder, 'blogposts/temp')
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Generate a unique filename to avoid overwriting existing files
    filename = secure_filename(uploaded_file.filename)
    unique_filename = os.path.join(temp_folder, filename)

    # Save the file to the temporary holding folder
    uploaded_file.save(unique_filename)

    # Return a JSON response with the URL of the uploaded image
    return {
        'uploaded': True,
        'url': url_for('static', filename=f'blogposts/temp/{filename}')
    }
#
# # Function to save base image
# def save_base_image(image, blog_id, title):
#     filename = secure_filename(image.filename)
#     save_path = os.path.join(app.config['UPLOAD_FOLDER'], str(blog_id))
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     image_path = os.path.join(save_path, filename)
#     image.save(image_path)
#     return '/' + os.path.join(app.config['UPLOAD_FOLDER'], str(blog_id), filename)
#
# # Function to save image from base64 data
# def save_image_from_base64(image_data, blog_id, title):
#     imgdata = base64.b64decode(image_data)
#     filename = f"{title}_{blog_id}.jpg"  # Or use any other logic to generate the filename
#     save_path = os.path.join(app.config['UPLOAD_FOLDER'], str(blog_id))
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     image_path = os.path.join(save_path, filename)
#     with open(image_path, 'wb') as f:
#         f.write(imgdata)
#     return '/' + os.path.join(app.config['UPLOAD_FOLDER'], str(blog_id), filename)




