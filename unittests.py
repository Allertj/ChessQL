from schema.schema import schema
from main import create_app
import unittest
from flask import Flask
from flask_testing import TestCase

import random, string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str


class MyTest1(TestCase):
    def create_app(self):
        return create_app()

    def create_new_token(self):
        res = """mutation { signup(username: "SomeUserName4", email: "someEmail4", password: "SomePassword4") { result {
              username email id wins draws loses openGames } } }"""
        result = schema.execute(res)
        res4 = """mutation { login( email: "someEmail4", password: "SomePassword4") { result {
                    username email id wins draws loses openGames accessToken} } }"""   
        result = schema.execute(res4)   
        # print(result)
        return result.to_dict()["data"]["login"]["result"]["accessToken"]

    # def test_login(self):    
    #     res2 = """mutation { login( email: "someEmail", password: "SomePassword") { result {
    #                 username email id wins draws loses openGames accessToken} } }"""   
    #     result = schema.execute(res2)
    #     print(result.to_dict()["data"])

    def test_signup(self):     
        token = self.create_new_token()
        print(token)



# class MyTest(TestCase):
#     def create_app(self):
#         return create_app()

#     def setUp(self):
#         # print("hello")
#         app = create_app()
#         with app.test_request_context():
#           print("hello")
#         # db.create_all()

#     def test_first(self):
#         res = """mutation { signup(username: "15", email: "15", password: "14") { result {
#               username email id wins draws loses openGames } } }"""
#         result = schema.execute(res)
#         res4 = """mutation { login(email: "15", password: "14") { result {
#                   username email id wins draws loses openGames accessToken} } }"""   
#         result = schema.execute(res4)
#         print(result.to_dict()["data"])

#     def tearDown(self):
#         print("hello")
#         # db.session.remove()
#         # db.drop_all()

if __name__ == '__main__':
    unittest.main()  
# # class TestCases(unittest.TestCase):
# #     def __init__(self):
# #         super().__init__()

# #     def test_schema1(self):
# #         app = create_app()
# #         with app.test_request_context(headers={'x-access-token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc4UsImlhdCI6MTY4NDM5NjAxMCwianRpIjoiZGVkMWE4NDYtZDZkOC00ZmNkLThhMjQtMzcwZTEyZjAwOTYzIiwidHlwZSI6ImFjY4VzcyIsInN1YiI6NywibmJmIjoxNjY0Mzk4MDEwLCJleHAiOjE4NjQzOTY5MTB9.8mzbPzAItfxPSmEXfByOVV0CeFVB1AD1spFChTpOyuA"}):
# #             # result = schema.execute("""query { user(userid:7) { username id } }""")
     
# #             res = """mutation {
# #               signup(username: "14", email: "14", password: "14") {
# #                 result {
# #                   username
# #                   email
# #                   id
# #                   wins
# #                   draws
# #                   loses
# #                   openGames
# #                 }
# #               }
# #             }"""
# #             result = schema.execute(res)
# #             print(result.to_dict()["data"])   
# # # mutation {
# # #   signup(username: "7", email: "7", password: "7") {
# # #     result {
# # #       username
# # # 
# # #     }
# # #   }
# # # }


