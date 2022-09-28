from graphene import ObjectType, String, Int

class UserR(ObjectType):
    id = Int()
    username = String()
    email = String()
    wins = Int()
    draws = Int()
    loses = Int()
    open_games = Int()

class LoggedInUser(UserR):
    accessToken = String()

class Message(ObjectType):
    message = String()    