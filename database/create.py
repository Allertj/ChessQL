import json
import os

from dotenv import load_dotenv
from .models import db
from sqlalchemy_utils import database_exists
from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp
from .models import User, Games
from flask_jwt_extended import create_access_token
from .newgame import game as gameasjson
from .utc_time import utc_time

load_dotenv()
MAX_OPEN_GAMES = int(os.environ.get("MAX_OPEN_GAMES"))

def get_all_games_from_user(userid):
    white_games =  Games.query.filter_by(player0id=userid).all()
    black_games =  Games.query.filter_by(player1id=userid).all()
    return white_games + black_games

def get_user_stats(userid):
    user =  User.query.filter_by(id=userid).first()
    if user:
        return { "stats": json.loads(user.stats), "open_games" : user.open_games}
    else:
        return { "msg": "No such user"}

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
    
def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

def get_game_by_id(gameid):
    return Games.query.filter_by(id=gameid).first()


# CHANGE gameasjson BACK TO gameasjson!!
def create_new_game(userid):
    game = Games(player0id=userid,
                player1id="0",
                gameasjson= "HELLO",
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
    game =  Games.query.filter(Games.player0id != user.id, Games.player1id == "0").first()
    if game:
        start_game(game, user)
        return {"msg": "Joined New Game. Ready to play", "game": game }
    if not game:
        game = create_new_game(user.id)        
        return {"msg": "New game created. Invite open.", "game": game }

def end_game(game):
    gameasjson = json.load(game["gameasjson"])
    gameasjson["status"] = "Ended"
    game["draw_proposed"] = None
    game["last_change"] = utc_time()
    game["gameasjson"] = gameasjson
    db.session.commit()

def start_game(game, user):
    game.time_started = utc_time()
    game.last_change = utc_time()
    game.status = "Playing"
    game.player1id = user.id  
    user.open_games += 1 
    db.session.commit()

def change_element_in_db(gameid, dict_of_changes):
    game = get_game_by_id(gameid)
    if game:
        for item, new_value in dict_of_changes.items():
            setattr(game, item, new_value)
    db.session.commit()        

def add_stat_to_user(userid, single_stat):
    user = get_user_by_id(userid)
    if user:
        original_stats = json.load(user["stats"])
        original_stats[single_stat] += 1
        user["stats"] = original_stats
        user["open_games"] -= 1
        db.session.commit()

def get_other_player(game, userid):
    if userid == game["player0id"]: return game["player1id"]
    if userid == game["player1id"]: return game["player0id"]

def add_statistics(game, draw, winner, loser):
    if draw:
        if game["player0id"] and game["player1id"]:
            add_stat_to_user(game["player0id"], "D")
            add_stat_to_user(game["player1id"], "D")
    if winner:
        add_stat_to_user(winner, "W")
        add_stat_to_user(get_other_player(game, winner), "L")
    if loser:
        add_stat_to_user(loser, "L")
        add_stat_to_user(get_other_player(game, loser), "W")    

def end_game_and_add_statistics(gameid, draw, winner, loser):
    game = get_game_by_id(gameid)
    if game:
        end_game(game)
        add_statistics(game, draw, winner, loser)

def login_user(email, password):
    user = get_user_by_email(email)
    if not user:
        return "Unknown user"
    if check_password_hash(user.password, password):
        return {"id":    user.id,
            "stats": user.stats,
            "username": user.username,
            "email": user.email,
            "open_games": user.open_games,
            "roles": ["User"],
            "accessToken": create_access_token(user.id)}
    return "Invalid password"    

def create_user(username, email, password):
    password_hash = generate_password_hash(password)
    user = User(username=username, 
                email=email, 
                password=password_hash, open_games = 0)    
    try:
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        if e.args[0].endswith('email'):
            return "Email already in use"
        elif e.args[0].endswith('username'):
            return "Username already in use" 
        else:
            return f"Failed because of ${e.args[0]}"     

def create_db(app, database_url):
    db.init_app(app) 
    # if not database_exists(database_url):
    with app.app_context():
        db.create_all()