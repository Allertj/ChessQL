from graphene import ObjectType, String, Int

class UserR(ObjectType):
    id = Int()
    username = String()
    email = String()
    stats = String()
    open_games = Int()

class LoggedInUser(UserR):
    accessToken = String()

class Message(ObjectType):
    message = String()    