from database.models import User as UserModel, Games as GameModel, Admin
from graphene import relay, ObjectType, Schema, Field, Int, List
from graphql import GraphQLError
from .login import Login
from .signup import Signup
from flask_jwt_extended import jwt_required, get_jwt_identity
from .admin_required import admin_required
from .mutations.send_move import SendMove
from .mutations.start_game import StartGame
from .objects import Games, User

class MyMutations(ObjectType):
    signup = Signup.Field()
    login = Login.Field()
    sendMove = SendMove.Field()
    startGame = StartGame.Field()
    
class Query(ObjectType):
    all_users = List(User)
    all_games = List(Games)
    admins = List(User)
    game = Field(Games, gameid=Int())
    user = Field(User, userid=Int())

    # @jwt_required()
    def resolve_user(parent, info, userid):
        if True:
        # if get_jwt_identity() == userid or get_jwt_identity() == "admin_user":
            return UserModel.query.filter_by(userid=userid).first()
        else:
            raise GraphQLError("Clients can only view their own data.")

    # @jwt_required()
    def resolve_game(parent, info, gameid):
        caller = get_jwt_identity()
        game = GameModel.query.filter_by(gameid=gameid).first()
        if game.player1id == caller or game.player0id == caller or caller == "admin_user":
            return game
        else:
            raise GraphQLError("Client is not a participant in this game")

    # @admin_required()
    def resolve_all_users(parent, info):
        return UserModel.query.all()

    # @admin_required()
    def resolve_all_games(parent, info):
        return GameModel.query.all()

    # @admin_required()
    def resolve_admins(parent, info):
        ids = [admin.adminid for admin in Admin.query.all()]
        return UserModel.query.filter(UserModel.userid.in_(ids)).all()

schema = Schema(query=Query, mutation=MyMutations)   