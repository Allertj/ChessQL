from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp
from flask_jwt_extended import create_access_token
from .db_queries  import get_user_by_email
from .models import User, Admin, db

def generate_access_token(userid):
    access_token = create_access_token(userid) 
    admin_role = Admin.query.filter_by(adminid=userid).first()
    if admin_role:
        access_token = create_access_token(
            "admin_user", additional_claims={"is_administrator": True})
    return access_token   

def login_user(email, password):
    user = get_user_by_email(email)
    if not user:
        return "Unknown user"
    if check_password_hash(user.password, password):
        return user, generate_access_token(user.userid)
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

def promote_user_to_admin(userid):
    db.session.add(Admin(adminid=userid))
    db.session.commit()

def delete_user_by_id(userid):
    User.query.filter_by(userid=userid).delete()

def demote_user_to_commoner(userid):    
    Admin.query.filter_by(adminid=userid).delete()