from graphene import String, Mutation, Int
from graphql import GraphQLError
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db_game_mutations import check_if_user_is_participant, change_element_in_db

class SendMove(Mutation):
    class Arguments:
        userid = Int()
        gameid = Int()
        move = String()

    result = String()

    @jwt_required()
    def mutate(self, info, userid, gameid, move):
        if str(get_jwt_identity()) in  [str(userid), "admin_user"]:
            if check_if_user_is_participant(gameid, userid):
                change_element_in_db(gameid, {"unverified_move": move})
                return SendMove(result=move)        
        raise GraphQLError("client is not a participant in this game")