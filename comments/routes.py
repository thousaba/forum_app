from flask import Blueprint, jsonify, request
from extensions import db
from comments.models import Comment
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__)


# YORUM EKLE
@comments_bp.route('/<int:post_id>', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    data= request.get_json()
    if not data or not data.get('content'):
     return jsonify({"error": "Missing content"}), 400

    user_id = int(get_jwt_identity())
    comment = Comment(content=data['content'], post_id=data['post_id'], user_id=user_id)
    
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully", "comment_id": comment.id}), 201



# BELİRLİ BİR YAZIYA AİT YORUMLARI GETİR
@comments_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    return jsonify([{
    "id": c.id, "content": c.content, "user_id": c.user_id, "post_id": c.post_id} for c in comments]), 200



# YORUM GÜNCELLE
@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({"error": "Missing content"}), 400
    
    current_user_id = int(get_jwt_identity())
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id !=current_user_id:
        return jsonify({"error": "User not authenticated"}), 401
    
    
    comment.content = data['content']
    db.session.commit()
    return jsonify({"message": "Comment updated successfully"}), 200



# YORUM SİL
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    current_user_id = int(get_jwt_identity())
    comment= Comment.query.get_or_404(comment_id)

    if comment.user_id != current_user_id:
        return jsonify({"error": "You can only delete your own comments"}), 403
    
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully"}), 200

