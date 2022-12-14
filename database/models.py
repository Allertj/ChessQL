from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255)) 
    wins = db.Column(db.Integer, default=0, nullable=False)
    draws = db.Column(db.Integer, default=0,  nullable=False)
    loses = db.Column(db.Integer, default=0,  nullable=False)
    open_games = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"""USER: {self.userid}, 
                   username: {self.username} 
                   email: {self.email} 
                   wins: {self.wins} 
                   draw: {self.draws}
                   loses: {self.loses} 
                   open games: {self.open_games}"""

class Admin(db.Model):
    adminid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False, primary_key=True)

class Games(db.Model):
    gameid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player0id = db.Column(db.Integer, db.ForeignKey('user.userid'))
    player1id = db.Column(db.Integer, db.ForeignKey('user.userid'))
    status = db.Column(db.String(20))
    result = db.Column(db.String(20))
    time_started = db.Column(db.DateTime)
    last_change = db.Column(db.DateTime)
    turn = db.Column(db.Integer, db.ForeignKey('user.userid'))
    unverified_move = db.Column(db.String(20))
    draw_proposed = db.Column(db.String(20))
    gameasjson = db.Column(db.String(4000))

    def __repr__(self):
        return f"""GAME {self.gameid}, 
                   player1id: {self.player1id}, 
                   player0id: {self.player0id} 
                   status: {self.status} 
                   result: {self.result}"""