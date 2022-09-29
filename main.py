import os
import eventlet

from dotenv import load_dotenv

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_graphql import GraphQLView

from database.create import create_db
from schema.schema import schema

def create_app():
    load_dotenv()
    database_url = "postgresql://" + os.environ["DBUSERNAME"] + ":" \
                                + os.environ["DBPASSWORD"] + "@" \
                                + os.environ["DBHOST"] + ":" \
                                + os.environ["DBPORT"] + "/" \
                                + os.environ["DBDATABASE"]
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_HEADER_NAME"] = "x-access-token"
    app.config["JWT_HEADER_TYPE"] = ""
    app.config["JWT_SECRET_KEY"] = str(os.environ.get("JWT_SECRET KEY"))
    
    JWTManager(app)
    create_db(app, database_url)

    app.add_url_rule("/graphql", view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    return app

if __name__ == '__main__':
    app = create_app()
    host = "0.0.0.0"
    port = int(os.environ.get("PORT"))
    production = bool(os.environ.get("PRODUCTION"))
    if production:
        eventlet.wsgi.server(eventlet.listen((host, port)), app) 
    else:        
        app.run(host, port)
