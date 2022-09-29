from graphene import String, Field, Mutation
from graphql import GraphQLError
from database.db_user_mutations import create_user 
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
            result = UserR(userid=user.userid, 
                            username=user.username, 
                            email=user.email, 
                            wins=user.wins, 
                            draws=user.draws,
                            loses=user.loses,
                            open_games=user.open_games)
            return Signup(result=result)