from graphene import String, Mutation, Int
from graphql import GraphQLError
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db_game_mutations import check_if_user_is_participant

class SendMove(Mutation):
    class Arguments:
        userid = Int()
        gameid = Int()
        move = String()

    result = String()

    @jwt_required()
    def mutate(self, info, userid, gameid, move):
        if str(get_jwt_identity()) == str(userid):
            print("FIRST CHECK", str(get_jwt_identity()), str(userid))
            if check_if_user_is_participant(gameid, userid):
                print("SECOND", check_if_user_is_participant(gameid, userid), userid, gameid)
                return SendMove(result=move)        
        else:
            raise GraphQLError("client is not a participant in this game")