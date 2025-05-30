from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    __tablename__ = 'user'
    
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(100), unique=True, nullable=False)
    password_hash= db.Column(db.String(200), nullable=False)
    role= db.Column(db.String(50), default='user', nullable=False)
    



    posts= db.relationship('Post', backref='author', lazy=True)
    comments= db.relationship('Comment', back_populates='author', lazy=True)
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.password_hash= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    

    