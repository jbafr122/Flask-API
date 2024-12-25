from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import bcrypt

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
api = Api(app)

class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)    
    
    def __repr__(self): 
        return f"User(name = {self.name}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    
    if (not data.get("name") or not data.get("email") or not data.get("password")):
        return {"message": "Name, email, and password are required"}, 400
    
    if UserModel.query.filter_by(email=data["email"]).first():
        return {"message": "A user with this email already exists"}, 409

    if UserModel.query.filter_by(name=data["name"]).first():
        return {"message": "A user with this name already exists"}, 409
    
    new_user = UserModel(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    except:
        db.session.rollback()
        return {"message": "Error registering user"}, 500

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all() 
        return users 
    
    def post(self):
            args = user_args.parse_args()
            existing_user = UserModel.query.filter_by(email=args["email"]).first()
            if existing_user:
                if existing_user.name == args['name']:
                    return {"message": "A user with this name already exists"}, 409
                if existing_user.email == args['email']:
                    return {"message": "A user with this email already exists"}, 409
            try:        
                user = UserModel(name=args["name"], email=args["email"])
                db.session.add(user) 
                db.session.commit()
                users = UserModel.query.all()
                return users, 201
            except Exception as e: 
                db.session.rollback()
                return {"message": f"An error occurred: {str(e)}"}, 500

    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        return user 
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user 
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

    
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True) 