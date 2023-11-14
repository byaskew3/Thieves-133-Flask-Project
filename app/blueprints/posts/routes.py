from . import posts
from flask import request, flash, redirect, url_for, render_template
from app.models import Post, db
from .forms import PostForm
from flask_login import current_user, login_required

# Create a Post (Create)
@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data 
        caption = form.caption.data
        img_url = form.img_url.data
        user_id = current_user.id

        # Create an instance of our Post Class
        post = Post(title, caption, img_url, user_id)

        # add user to database
        db.session.add(post)
        db.session.commit()

        flash(f'Post {title} successfully created!', 'success')
        return redirect(url_for('posts.feed'))
    else:
        return render_template('create_post.html', form=form)

# Reading all posts (Read)
@posts.route('/feed')
@login_required
def feed():
    all_posts = Post.query.all()
    return render_template('feed.html', all_posts=all_posts)