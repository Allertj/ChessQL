from graphene import String, Field, Mutation
from graphql import GraphQLError
from database.db_user_mutations import create_user 
from ..objects import User

class Signup(Mutation):
    class Arguments:
        username = String()
        email = String()
        password = String()

    user = Field(User)

    def mutate(root, info, username, email, password):
        user = create_user(username, email, password)
        if type(user) is str:
            raise GraphQLError(user)    
        else:    
            return Signup(user=user)