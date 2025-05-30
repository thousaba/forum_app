from flask import Blueprint, jsonify, request
from extensions import db
from users.decorators import admin_required
from users.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

#TÜM KULLANICILARIN LİSTESİNİ GETİR
@users_bp.route('/admin', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username,} for u in users])

#KULLANICI KAYDI
@users_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully"}), 201



#KULLANICI GİRİŞİ
@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    #Kullanıcıyı veritabanında kontrol et
    user = User.query.filter_by(username=data['username']).first()

    #Kullanıcı adı ve şifreyi kontrol et
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Login successful", "access_token": access_token}), 200


#BELİRLİ BİR KULLANICININ PROFİLİNİ GETİR
@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = [{"id": p.id, "title": p.title, "content": p.content} for p in user.posts]
    return jsonify({"id": user.id, "username": user.username, "posts": posts}), 200


#KULLANICIYI GÜNCELLE
@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_username = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400

    if user.username != current_username:
        return jsonify({"error": "You can only update your own account"}), 403

    user.username = data['username']
    user.password = generate_password_hash(data['password'], method='scrypt')
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200


#KULLANICIYI SİL
@users_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)

    if user.username != current_user_id:
        return jsonify({"error": "You can only delete your own account"}), 403

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


#ADMİN KULLANICIYI SİL
@users_bp.route('/admin/<user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user_admin(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
