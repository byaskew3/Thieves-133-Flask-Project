from . import api
from flask import request, jsonify
from app.models import Post, db

# CRUD

# Creating a post (CREATE)
@api.post('/create_post')
def create_post_api():
    # This is coming from Postman Body
    data = request.get_json()
    
    # Extracting our post data from "data"
    title = data["title"]
    caption = data["caption"]
    img_url = data["img_url"]
    user_id = data["user_id"]
    
    # Create an instance of our Post class
    post = Post(title, caption, img_url, user_id)
    
    # add post to database
    db.session.add(post)
    db.session.commit()
    
    return jsonify({
        'status': 'ok',
        'message': f'Post {title} has been posted!'
    })

# Read all posts (Read)
@api.get('/all_posts')
def all_posts_api():
    posts = Post.query.all()
    
    posts_lst = []
    
    for post in posts:
        post_dict = {
            "title": post.title,
            "caption": post.caption,
            "img_url": post.img_url,
            "user_id": post.user_id
        }
        posts_lst.append(post_dict)
    
    return jsonify({
        "status": "ok",
        "posts": posts_lst
    })
    
# Get a singular post (Read)
@api.get('/post/<int:post_id>')
def get_post_api(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify({
            "status": "ok",
            "post": {
                "title": post.title,
                "caption": post.caption,
                "img_url": post.img_url,
                "user_id": post.user_id    
            }
        })
    else:
        return jsonify({
            "status": "not ok",
            "message": "Post does not exist!"
        })

# Update a Post (PUT/Update)
@api.put('/update_post/<int:post_id>')
def update_post_api(post_id):
    post = Post.query.get(post_id)
    data = request.get_json()
    
    if post:
        post.title = data["title"]
        post.caption = data["caption"]
        post.img_url = data["img_url"]
        
        db.session.commit()
        
        return jsonify({
            'status': 'ok',
            'message': f'Post {post.title} has been updated!'
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'Post does not exist'
        })

# Delete a post (Delete)
@api.delete('/delete_post/<int:post_id>')
def delete_post_api(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({
            "status": "ok",
            "message": f"Post {post.title} successfully deleted"
        })
    else:
        return jsonify({
            'status': 'not ok',
            'message': 'Post does not exist'
        })
