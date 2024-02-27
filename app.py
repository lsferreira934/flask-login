from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model): 
  __tablename__ = 'users'

  id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
  name = db.Column(db.String(100), nullable=False)
  lastname = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)

  def json(self):
    return {
        'id': self.id,
        'name': self.name,
        'lastname': self.lastname,
        'email': self.email
    }
  
with app.app_context():
  db.create_all()
  
@app.route('/', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'Bem vindo ao Flask-Login'}), 200)

@app.route('/user', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
  
    required_fields = ['name', 'lastname', 'email', 'password']
    if not all(field in data for field in required_fields):
      return make_response(jsonify({'error': 'All fields are required'}), 400)
    
    new_user = User(name=data['name'], lastname=data['lastname'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': 'User created successfully'}), 201)
  except Exception as e:
    return make_response(jsonify({'message': f'Error creating user: {str(e)}'}), 500)
  
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify({'users': [user.json() for user in users]}), 200)
  except Exception as e:
    return make_response(jsonify({'message': f'Error getting users: {str(e)}'}), 500)
  

@app.route('/users/<uuid:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user: 
      return make_response(jsonify({'user': user.json() }), 200)
    else:
      return make_response(jsonify({'message': 'User not found' }), 400)
  except Exception as e:
    return make_response(jsonify({'message': f'Error getting user: {str(e)}'}), 500)
  
@app.route('/users/<uuid:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.name = data['name']
      user.lastname = data['lastname']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'User updated' }), 200)
    else:
      return make_response(jsonify({'message': 'User not found' }), 400)
  except Exception as e:
    return make_response(jsonify({'message': f'Error updating user: {str(e)}'}), 500)
  
  
@app.route('/user/<uuid:id>', methods=['GET'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user: 
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'User deleted' }), 200)
    else:
      return make_response(jsonify({'message': 'User not found' }), 400)
  except Exception as e:
    return make_response(jsonify({'message': f'Error deleting user: {str(e)}'}), 500)