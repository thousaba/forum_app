import os
from users.models import User
from flask import Flask
from flask import send_from_directory
from extensions import db, jwt
from users.routes import users_bp
from posts.routes import posts_bp
from comments.routes import comments_bp
from datetime import timedelta
from commands import make_admin

def create_app():
  app= Flask(__name__)
  
  
  app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///blog.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
  app.config['JWT_SECRET_KEY']= 'starwars'
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
  app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
  app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

  app.cli.add_command(make_admin)

  db.init_app(app)
  jwt.init_app(app)

  app.register_blueprint(users_bp, url_prefix='/users')
  app.register_blueprint(posts_bp, url_prefix='/posts')
  app.register_blueprint(comments_bp, url_prefix='/comments')

  @app.route('/uploads/<filename>')
  def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

  with app.app_context():
   db.create_all()
  return app



if __name__ == '__main__':
 app = create_app()
 app.run(debug=True)
