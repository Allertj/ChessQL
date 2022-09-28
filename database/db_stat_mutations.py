import json
from .db_queries  import get_user_by_id, get_game_by_id
from .models import User, db
from .db_game_mutations import end_game

def get_user_stats(userid):
    user =  User.query.filter_by(id=userid).first()
    if user:
        return { "stats": json.loads(user.stats), "open_games" : user.open_games}
    else:
        return { "msg": "No such user"}
  
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