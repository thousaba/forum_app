import os
from flask import Blueprint, jsonify, request, current_app
from extensions import db
from posts.models import Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from users.decorators import admin_required

posts_bp = Blueprint('posts', __name__)

#MAX_UPLOAD_SIZE = 1024

#POST OLUŞTUR
@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id= int(get_jwt_identity())

    title= request.form.get('title')
    content= request.form.get('content')
    image = request.files.get('image')

    if not title or not content:
        return jsonify({"error": "Missing title or content"}), 400
    
    image_path = None

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    if image:
        if not allowed_file(image.filename):
            return jsonify({"error": "File type not allowed"}), 400
        
        filename = secure_filename(image.filename)

        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        image.save(os.path.join(upload_folder, filename))
        image_path = f"uploads/{filename}"

    new_post = Post(
        title=title,
        content=content,
        user_id=current_user_id,
        image=image_path
    )

    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully", "image_url": image_path}), 201    



#BELİRLİ BİR POST GETİR
@posts_bp.route('/search/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "user_id": post.user_id,
        "image": post.image,
        "comments": [{"id": c.id, "content": c.content} for c in post.comments]
    }), 200



#POST GÜNCELLE
@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id= int(get_jwt_identity())
    post= Post.query.get_or_404(post_id)
    data= request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Missing title or content"}), 400
    
    if post.user_id != current_user_id:
        return jsonify({"error": "User not authorized to update this post"}), 403
    
    post.title= data['title']
    post.content= data['content']
    db.session.commit()
    return jsonify({"message": "Post updated successfully"}), 200



#POST SİL
@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id= int(get_jwt_identity())
    post= Post.query.get_or_404(post_id)

    if post.user_id != current_user_id:
        return jsonify({"error": "You can only delete your own posts"}), 403
    
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200



#ADMİN POST SİL
@posts_bp.route('/admin/<int:post_id>', methods=['DELETE'])
@jwt_required()
@admin_required

def delete_post_admin(post_id):
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200



#ADMİN TÜM POSTLARI GETİR
@posts_bp.route('/admin', methods=['GET'])
@jwt_required()
@admin_required

def get_all_posts():
    posts= Post.query.all()
    
    return jsonify([{
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "user_id": post.user_id,
        "image": post.image
    } for post in posts]), 200



#SELECT id, title, content, user_id, image FROM POST values (id,title,asd,asd,asd,as,d)