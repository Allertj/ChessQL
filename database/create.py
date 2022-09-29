from .models import db
from sqlalchemy_utils import database_exists

def create_db(app, database_url):
    db.init_app(app) 
    # if not database_exists(database_url):
    with app.app_context():
        db.create_all()