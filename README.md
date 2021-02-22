# **Flask Starter Blog**

this web page is a starter blog with flask , jquery and bootstrap. you can signup or login -nav links- and test this website.
also you can post a blog. you can update or delete a blog post if you post it with your own account. this website's DB powered by Sqlite but you can change it in [SQLALCHEMY](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) config and use other database.

### ok let's check the pages here:

**1. Home Page**
all blogs sorted by date.all posts all paginated. each cards show blog's title and author and date. the author is clickable and if you click on that you can see all posts from that author( number 10 )
![flask , Flask Blog](https://uupload.ir/files/rusq_home.png "Home page")

**2. Signup**
the email and other things will check by [Flask Form](https://flask-wtf.readthedocs.io/). password will saved in database in hash version with [Werkzeug](https://werkzeug.palletsprojects.com/). **check model.py**
![flask , Flask Blog](https://uupload.ir/files/p0l9_signup.png "Signup")

**3. Login**
![flask , Flask Blog](https://uupload.ir/files/i96o_login.png "Login")

**4. posts**
here if you try to delete a post that is not your post you will see 403 error page
![flask , Flask Blog](https://uupload.ir/files/oy9u_other-user-post.png "Posts")

**5. New post**
![flask , Flask Blog](https://uupload.ir/files/1wa3_new_post.png "New post")

**6. User post**
here you have access to delete or update your post
![flask , Flask Blog](https://uupload.ir/files/776b_user-post-view.png "User Post")

**7. 403 error Page**
it's really cute :)
![flask , Flask Blog](https://uupload.ir/files/m88_403.gif "403")

**8. User Profile edit**
here you can change your account info or change your profile defualt picture.
![flask , Flask Blog](https://uupload.ir/files/gb2i_profile.png "Profile Edit")

**9. 404 error Page**
also this one is cute too :))
![flask , Flask Blog](https://uupload.ir/files/pio0_404.gif "404")

**10. User's Posts**
![flask , Flask Blog](https://uupload.ir/files/80rn_other-user-posts.png "User's Posts")



Libraries in use:

> FLASK

> SQLALCHEMY

> WERKZEUG

> FLASK LOGIN

> FLASK FORM
