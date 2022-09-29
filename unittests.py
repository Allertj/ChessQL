from schema.schema import schema
from main import create_app
import unittest
from flask_testing import TestCase
from database.db_game_mutations import delete_game_by_id
from database.db_user_mutations import delete_user_by_id, promote_user_to_admin, demote_user_to_commoner
import random, string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class MyTest(TestCase):
    def create_app(self):
        return create_app()

    def create_random_login(self):
        user =  get_random_string(15) 
        email = get_random_string(15) 
        passw = get_random_string(15) 
        return user, email, passw
 
    def mock_signup(self, user, email, passw, for_test=False):    
        res = f"""mutation {{ signup(username: "{user}" email: "{email}" password: "{passw}") 
                   {{ user {{ username email userid wins draws loses openGames }}}}}}"""
        result = schema.execute(res)
        if for_test:
            return result.to_dict()["data"]["signup"]["user"]
        return result.to_dict()["data"]["signup"]["user"]["userid"] 

    def mock_login(self, email, passw, for_test=False):
        res4 = f"""mutation {{ login( email: "{email}", password: "{passw}") 
                     {{ user {{ username email userid wins draws loses openGames }} accessToken }}}}"""   
        result = schema.execute(res4)  
        result_login = result.to_dict()["data"]["login"]
        if for_test:
            return result_login["user"]
        return result_login["accessToken"], result_login["user"]["userid"]

    def create_new_token(self, is_admin=False):
        user, email, passw = self.create_random_login()
        id = self.mock_signup(user, email, passw)
        if is_admin:
            promote_user_to_admin(id)
        return self.mock_login(email, passw)

    def setUp(self):
        token, self.userid = self.create_new_token(True)
        self.requestcontext = create_app().test_request_context(headers={"x-access-token": token})

    def test_admin(self):
        res = """query { admins { userid username } }"""             
        with self.requestcontext:
            result = schema.execute(res)
        self.assertEqual(type(result.to_dict()["data"]["admins"]), list)   

    def test_new_game(self, for_test=False):
        res = f"""mutation {{ startGame(userid: {str(self.userid)}) {{ result newGame {{ gameid }} }}}}"""
        with self.requestcontext:
            result = schema.execute(res)
        possible_results = ["New game created. Invite open.", 'Joined New Game. Ready to play']
        self.assertIn(result.to_dict()["data"]["startGame"]["result"], possible_results)
        gameid = result.to_dict()["data"]["startGame"]["newGame"]["gameid"]
        if not for_test:
            delete_game_by_id(int(gameid))
        return gameid    

    def test_send_move(self): 
        res = f"""mutation {{ sendMove(userid: 22, gameid:1, move: "{{move: move}}") {{ result }} }}"""
        with self.requestcontext:
            result = schema.execute(res)
        self.assertEqual(result.to_dict()["errors"][0]["message"],'client is not a participant in this game')
        gameid = self.test_new_game(True)    
        res = f"""mutation {{ sendMove(userid: {self.userid}, gameid:{gameid}, move: "{{move: move}}") {{ result }} }}"""
        with self.requestcontext:
            result = schema.execute(res)
        self.assertEqual(result.to_dict()["data"]["sendMove"]["result"],"{move: move}")    
        delete_game_by_id(int(gameid))

    def test_signup(self):
        user, email, passw = self.create_random_login()
        result = self.mock_signup(user, email, passw, True)
        self.assertEqual(result["username"], user)
        self.assertEqual(result["email"], email)
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["loses"], 0)
        self.assertEqual(result["draws"], 0)
        self.assertEqual(result["openGames"], 0)

    def test_login(self):
        user, email, passw = self.create_random_login()
        id = self.mock_signup(user, email, passw)
        result = self.mock_login(email, passw, True)
        self.assertEqual(result["username"], user)
        self.assertEqual(result["email"], email)
        self.assertEqual(result["wins"], 0)
        self.assertEqual(result["loses"], 0)
        self.assertEqual(result["draws"], 0)
        self.assertEqual(result["openGames"], 0)

    def tearDown(self):
        demote_user_to_commoner(self.userid)
        delete_user_by_id(self.userid)

if __name__ == '__main__':
    unittest.main()  