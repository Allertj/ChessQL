import json
import os
import datetime

from dotenv import load_dotenv

from .models import db, Games
from .newgame import game as gameasjson
from .db_queries  import get_user_by_id, get_game_by_id

load_dotenv()
MAX_OPEN_GAMES = int(os.environ.get("MAX_OPEN_GAMES"))

def create_new_game(userid):
    game = Games(player0id=userid,
                player1id=1,
                gameasjson= gameasjson,
                status="Open")
    db.session.add(game)
    db.session.commit()
    return game                

def join_game(userid):
    user = get_user_by_id(userid)
    if not user:
        return "User not found"  
    if user.open_games >= MAX_OPEN_GAMES:
        return "All Slots filled"
    game =  Games.query.filter(Games.player0id != str(user.userid), Games.player1id == 1).first()
    if game:
        start_game(game, user)
        return {"msg": "Joined New Game. Ready to play", "game": game }
    if not game:
        game = create_new_game(user.userid)        
        return {"msg": "New game created. Invite open.", "game": game }

def end_game(game):
    gameasjson = json.load(game["gameasjson"])
    gameasjson["status"] = "Ended"
    game["draw_proposed"] = None
    game["last_change"] = datetime.datetime.now()
    game["gameasjson"] = gameasjson
    db.session.commit()

def start_game(game, user):
    game.time_started = datetime.datetime.now()
    game.last_change = datetime.datetime.now()
    game.status = "Playing"
    game.player1id = user.userid  
    game.turn = game.player0id
    user.open_games += 1 
    db.session.commit()

def check_if_user_is_participant(gameid, userid):
    game = Games.query.filter_by(gameid=gameid).first()
    return game.player1id == userid or game.player0id == userid

def delete_game_by_id(gameid):
    Games.query.filter_by(gameid=gameid).delete()

def change_element_in_db(gameid, dict_of_changes):
    game = get_game_by_id(gameid)
    if game:
        for item, new_value in dict_of_changes.items():
            setattr(game, item, new_value)
    db.session.commit()   