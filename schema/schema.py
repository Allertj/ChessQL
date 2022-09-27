from graphene import Schema, ObjectType, String
from database.models import User as UserModel, Games as GameModel
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene import relay, ObjectType, Schema

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

class Games(SQLAlchemyObjectType):
    class Meta:
        model = GameModel
        interfaces = (relay.Node,)  

class Query(ObjectType):
   x = String()
   def resolve_x(self, info):
      return "HELLO"



schema = Schema(query=Query)