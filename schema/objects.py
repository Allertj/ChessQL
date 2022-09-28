from functools import wraps
# import re
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database.models import User as UserModel, Games as GameModel, Admin
# from database.db_user_mutations import create_user, get_user_by_email, login_user, create_new_game, join_game, promote_user_to_admin
from graphene import relay, ObjectType, Schema, String, Field, Mutation, Boolean, Int, List
from graphql import GraphQLError

from .login import Login
from .signup import Signup
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
from .admin_required import admin_required

class Games(SQLAlchemyObjectType):
    class Meta:
        model = GameModel
        interfaces = (relay.Node,)        

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)
    games = List(Games)    

    def resolve_games(parent, info):
        if info.path[0] == "allUsers":
            gameid = str(info.path[1])
            white_games =  GameModel.query.filter_by(player0id=gameid).all()
            black_games =  GameModel.query.filter_by(player1id=gameid).all()
            return white_games + black_games