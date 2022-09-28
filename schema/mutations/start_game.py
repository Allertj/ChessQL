from graphene import String, Mutation, Int
from graphql import GraphQLError
from flask_jwt_extended import jwt_required
from database.models import Games
from database.db_game_mutations import join_game

class StartGame(Mutation):
    class Arguments:
        userid = Int()
    
    result = String()
    new_game = Games

    @jwt_required()
    def mutate(self, info, userid):
        game = join_game(userid)
        if type(game) is str:
            raise GraphQLError(game)
        else:    
            return StartGame(result=game["msg"])  