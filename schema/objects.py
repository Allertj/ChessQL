from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database.models import User as UserModel, Games as GameModel
from database.create import create_user, get_user_by_email, login_user, create_new_game
from graphene import relay, ObjectType, Schema, String, Field, Mutation, Boolean, Int, List
from graphql import GraphQLError
from werkzeug.security import check_password_hash
from .login import Login
from .signup import Signup
from flask_jwt_extended import jwt_required, decode_token, exceptions

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

class Games(SQLAlchemyObjectType):
    class Meta:
        model = GameModel
        interfaces = (relay.Node,)        

class SendMove(Mutation):
    class Arguments:
        move = String()

    result = String()

    @jwt_required()
    def mutate(self, info, move):
        return SendMove(result="EMAIL TEST")        

class StartGame(Mutation):
    class Arguments:
        userid = Int()
    
    result = String()
    # new_game = SQLAlchemyConnectionField(Games.connection)

    # @jwt_required()
    def mutate(self, info, userid):
        game = create_new_game(userid)
        if type(game) is str:
            raise GraphQLError(game)
        else:    
            # print(game.player0id)
            print(dir(Games))
            return StartGame(result=game["msg"])        

class MyMutations(ObjectType):
    signup = Signup.Field()
    login = Login.Field()
    sendMove = SendMove.Field()
    startGame = StartGame.Field()


# class Users(ObjectType):
    # users = List(lambda: UserModel)


class Query(ObjectType):
    node = relay.Node.Field()
    # users = Field(Users)
    # customer = Field(Customer)
    # all_tuitions = FilterableConnectionField(TuitionObject, filters=TuitionFilter())
    all_users = String()
        # return Something(customer="HELLO")
    # all_users = List(lambda: User, username=String())
    # all_users = SQLAlchemyConnectionField(User)
    # allGames = SQLAlchemyConnectionField(Games)

    def resolve_all_users(parent, info):
        # print(UserModel.query)
        print(dir(UserModel))
        # users = UserModel.query.all()
        return "GOODDAY"
    
# schema = Schema(query=Query, types=[User, Games], mutation=MyMutations)         
schema = Schema(query=Query, mutation=MyMutations)   