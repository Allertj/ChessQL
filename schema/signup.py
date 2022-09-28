from graphene import String, Field, Mutation
from graphql import GraphQLError
from database.create import create_user 
from .response_types import UserR

class Signup(Mutation):
    class Arguments:
        username = String()
        email = String()
        password = String()

    result = Field(UserR)

    def mutate(root, info, username, email, password):
        user = create_user(username, email, password)
        if type(user) is str:
            raise GraphQLError(user)    
        else:    
            result = UserR(id=user.id, 
                            username=user.username, 
                            email=user.email, 
                            stats=user.stats, 
                            open_games=user.open_games)
            return Signup(result=result)