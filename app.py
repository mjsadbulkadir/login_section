from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)
# ma = Marshmallow(app)

class User(db.Model):
     id = db.Column(db.Integer,primary_key = True)
     email =db.Column(db.String(50))
     user_name = db.Column(db.String(100))
     password = db.Column(db.Integer)
     
     def __init__(self,email,user_name, password):
        self.email = email
        self.user_name = user_name
        self.password = password
        
# class PostSchema(ma.Schema):
#     class Meta:
#         fields = ("email", "user_name", "password")
        
# post_schema = PostSchema()
# posts_schema = PostSchema(many=True)

@app.route('/sign_up/', methods = ['POST'])
def Signup():
    email = request.json['email']
    user_name = request.json['user_name']
    password = request.json['password']

    my_post = User(email, user_name,password)
    db.session.add(my_post)
    db.session.commit()
    
#   return post_schema.jsonify(my_post)
    return jsonify({"msg":"updated"})

@app.route('/login', methods = ["POST"])
def Login():
     email = request.json['email']
     password = request.json['password']
     
     post = User.query.filter_by(email=email).first()
     # print("this is post password.................",post.password,type(post.password))
     # print("this is password,,,,,,,,,,,,,,,,,,,,,, ",password,type(password))
     if post.password ==password:
          return jsonify({"msg":"succesful"})
     return jsonify({"msg":"invalid details"})
with app.app_context():
     db.create_all()

if __name__ == "__main__":
     app.run(debug=True,port=8000,use_reloader = False)