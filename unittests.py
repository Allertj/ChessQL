from schema.schema import schema
from main import create_app
import unittest
from flask import Flask
from flask_testing import TestCase
from database.db_game_mutations import delete_game_by_id
from database.db_user_mutations import delete_user_by_id, promote_user_to_admin, demote_user_to_commoner
from database.db_queries import get_user_by_id, get_user_by_email, get_game_by_id
from database.models import Admin
import random, string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class MyTest(TestCase):
    def create_app(self):
        return create_app()

    def create_random_login(self):
        # user =  '"' + get_random_string(15) + '"'
        # email = '"' + get_random_string(15) + '"'
        # passw = '"' + get_random_string(15) + '"'
        user =  get_random_string(15) 
        email = get_random_string(15) 
        passw = get_random_string(15) 
        return user, email, passw
 
    def mock_signup(self, user, email, passw, for_test=False):    
        res = """mutation { signup(username: """+ '"' + user + '"'+ """, email
        : """  + '"' +email + '"' +""", password: """ + '"' + passw +'"' +""") { result {
              username email userid wins draws loses openGames } } }"""
        result = schema.execute(res)
        if for_test:
            return result.to_dict()["data"]["signup"]["result"]
        return result.to_dict()["data"]["signup"]["result"]["userid"] 

    def mock_login(self, email, passw):
        res4 = """mutation { login( email: """ + '"' + email + '"'+ """, password: """ + '"' + passw + '"' + """) { result {
                    username email userid wins draws loses openGames accessToken} } }"""   
        result = schema.execute(res4)  
        user = result.to_dict()["data"]["login"]["result"] 
        return user["accessToken"], user["userid"]

    def create_new_token(self, is_admin=False):
        user, email, passw = self.create_random_login()
        id = self.mock_signup(user, email, passw)
        if is_admin:
            promote_user_to_admin(id)
        return self.mock_login(email, passw)

    def setUp(self):
        token, self.id = self.create_new_token(True)
        self.requestcontext = create_app().test_request_context(headers={"x-access-token": token})

    def test_admin(self):
        res = """query { admins { userid username } }"""             
        with self.requestcontext:
            result = schema.execute(res)
        self.assertEqual(type(result.to_dict()["data"]["admins"]), list)   

    def test_new_game(self):
        res = """mutation { startGame(userid:"""+ str(self.id) +""") { result newGame { gameid }} }"""
        with self.requestcontext:
            result = schema.execute(res)
        # self.assertEqual(result.to_dict()["data"]["startGame"]["result"], "New game created. Invite open.")
        print(result.to_dict()["data"])

    def test_send_move(self): 
        res = """mutation { sendMove(userid: 2, gameid:1, move: "{move: move}") { result } }"""
        with self.requestcontext:
            result = schema.execute(res)
        self.assertEqual(result.to_dict()["errors"][0]["message"],'client is not a participant in this game')    
        # res = """mutation { sendMove(move:"HEO", userid: """+ str(self.id) +""") { result } }"""
        # with self.requestcontext:
        #     result = schema.execute(res)
        # print(result)    

    def test_signup(self):
        user, email, passw = self.create_random_login()
        result = self.mock_signup(user, email, passw, True)
        self.assertEqual(result["username"], user)
        self.assertEqual(result["email"], email)
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["loses"], 0)
        self.assertEqual(result["draws"], 0)
        self.assertEqual(result["openGames"], 0)

    def tearDown(self):
        pass
        # demote_user_to_commoner(self.id)
        # delete_user_by_id(self.id)

if __name__ == '__main__':
    unittest.main()  