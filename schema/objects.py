from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database.models import User as UserModel, Games as GameModel
from graphene import relay, ObjectType, Schema, String, Field

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

class Games(SQLAlchemyObjectType):
    class Meta:
        model = GameModel
        interfaces = (relay.Node,)        

class Customer(ObjectType):
    id = String()
    name = String()
    email = String()
    password  = String()

    def resolve_id(self, info):
        return "HELLO TEST"

    def resolve_name(self, info):
        return "NAME TEST"

    def resolve_email(self, test):
        return "EMAIL TEST"        



class Something(ObjectType):
   x = String()
   def resolve_x(self, info):
      return "HELLO"

class Query(ObjectType):
    node = relay.Node.Field()
    # something = Something()
    customer = Field(Customer)
    def resolve_customer(parent, info):
        return "HELLO"
    # users = List(lambda: User, username=String())
    allUsers = SQLAlchemyConnectionField(User)
    allGames = SQLAlchemyConnectionField(Games)
    allPets = SQLAlchemyConnectionField(Games)
    
schema = Schema(query=Query, types=[User, Games])        