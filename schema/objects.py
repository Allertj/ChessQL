from graphene_sqlalchemy import SQLAlchemyObjectType
from database.models import User as UserModel, Games as GameModel
from graphene import relay, List

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
            userid = str(info.path[1])
            white_games =  GameModel.query.filter_by(player0id=userid).all()
            black_games =  GameModel.query.filter_by(player1id=userid).all()
            return white_games + black_games