from graphene import String, Field, Mutation
from graphql import GraphQLError
from database.db_user_mutations import login_user 
from ..objects import User

class Login(Mutation):
    class Arguments:
        email = String()
        password = String()

    user = Field(User)
    accessToken = String()

    def mutate(root, info, email, password):
        user, accessToken = login_user(email, password)
        if type(user) is str:
            raise GraphQLError(user)
        else:
            return Login(user=user, accessToken=accessToken)    