import os

from dotenv import load_dotenv

from flask import Flask
from database.create import create_db
from flask_graphql import GraphQLView
# from schema.schema import schema

from schema.objects import schema

load_dotenv()

database_url = "postgresql://" + os.environ["DBUSERNAME"] + ":" \
                               + os.environ["DBPASSWORD"] + "@" \
                               + os.environ["DBHOST"] + ":" \
                               + os.environ["DBPORT"] + "/" \
                               + os.environ["DBDATABASE"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

create_db(app, database_url)

@app.route('/hello')
def test():
    return "TEST OK!"

app.add_url_rule("/graphql", view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))




if __name__ == '__main__':
    # print(DBDATABASE)
    # from database.models import User, db 
    # user = User(username="ALLERT", email="HELLO", password="HELLO", open_games = 0)    
    # # try:
    # with app.app_context():
        # db.session.add(user)
        # db.session.commit()
    host = "0.0.0.0"
    port = int(os.environ.get("PORT"))
    app.run(host, port)
