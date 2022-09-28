from graphene import String, Mutation, Int
from graphql import GraphQLError
from flask_jwt_extended import jwt_required, get_jwt_identity

class SendMove(Mutation):
    class Arguments:
        move = String()
        userid = Int()

    result = String()

    @jwt_required()
    def mutate(self, info, move, userid):
        if str(get_jwt_identity()) == str(userid):
            return SendMove(result=move)        
        else:
            raise GraphQLError("client is not a participant in this game")