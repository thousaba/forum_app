from flask.cli import with_appcontext
import click
from users.models import User
from extensions import db



@click.command(name='make_admin')
@click.argument('username')
@with_appcontext
def make_admin(username):
    user=User.query.filter_by(username=username).first()
    if not user:
         click.echo(f"User {username} does not exist.")
         return
    user.role = 'admin'
    db.session.commit()
    click.echo(f"User {username} has been promoted to admin.")
    
