from graphene import String, Field, Mutation
from graphql import GraphQLError
from database.db_user_mutations import login_user 
from .response_types import LoggedInUser

class Login(Mutation):
    class Arguments:
        email = String()
        password = String()

    result = Field(lambda: LoggedInUser)

    def mutate(root, info, email, password):
        user = login_user(email, password)
        if type(user) is str:
            raise GraphQLError(user)
        else:
            result = LoggedInUser(userid=user["userid"], 
                                  username=user["username"], 
                                  email=user["email"], 
                                  wins=user["wins"],
                                  draws=user["draws"],
                                  loses=user["loses"], 
                                  open_games=user["open_games"],
                                  accessToken=user["accessToken"])
            return Login(result=result)    