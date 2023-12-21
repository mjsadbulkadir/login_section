from functools import wraps
from flask import Flask, redirect,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] ='ThisIsSecretKey'

db = SQLAlchemy(app)

class User(db.Model):
     id = db.Column(db.Integer,primary_key = True)
     email =db.Column(db.String(50))
     user_name = db.Column(db.String(100))
     password = db.Column(db.Integer)
     
     def __init__(self,email,user_name, password):
        self.email = email
        self.user_name = user_name
        self.password = password
        
blacklisted_tokens = set()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('access-token')

        if not token:
            return jsonify({'msg': 'Token not found'}), 401

        if is_token_blacklisted(token):
            return jsonify({'msg': 'Token is no longer valid'}), 401

        try:
            user_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(user_data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'msg': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'msg': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'msg': 'Error decoding token', 'error': str(e)}), 401

        return f(user, *args, **kwargs)

    return decorator

@app.route('/sign_up/', methods = ['POST'])
def Signup():
    email = request.json['email']
    user_name = request.json['user_name']
    password = request.json['password']

    my_post = User(email, user_name,password)
    db.session.add(my_post)
    db.session.commit()
    
    return jsonify({"msg":"User Created Succesful"})

@app.route('/login', methods = ["POST"])
def login():
    email = request.json['email']
    password = request.json['password']

    post = User.query.filter_by(email=email).first()

    if not post or post.password != password:
        return jsonify({"msg": "Invalid credentials"}), 401

    token = jwt.encode(
        {'user_id': post.id,
         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
        app.config['SECRET_KEY']
    )

    return jsonify({'token': token})
def is_token_blacklisted(token):
    return token in blacklisted_tokens

@token_required 
@app.route('/logout', methods=["POST"])
def logout():
    token = request.headers.get('access-token')

    blacklisted_tokens.add(token)

    return jsonify({"msg": "Successfully logged out"})

with app.app_context():
     db.create_all()

if __name__ == "__main__":
     app.run(debug=True,port=8000,use_reloader = False)