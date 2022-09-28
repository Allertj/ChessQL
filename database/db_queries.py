from .models import User, Games

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
    
def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

def get_game_by_id(gameid):
    return Games.query.filter_by(id=gameid).first()

def get_all_games_from_user(userid):
    white_games =  Games.query.filter_by(player0id=userid).all()
    black_games =  Games.query.filter_by(player1id=userid).all()
    return white_games + black_games    