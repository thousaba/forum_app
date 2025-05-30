from extensions import db

class Post(db.Model):
    __tablename__ = 'post'

    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(100), nullable=False)
    content= db.Column(db.Text, nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image= db.Column(db.String(200), nullable=True)

    comments = db.relationship('Comment', back_populates='post', lazy=True)


    