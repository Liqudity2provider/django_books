import datetime
import jwt
from flask import request, jsonify, make_response
from flask_restful import reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import config
from app import app, db
from app.models.models import UserModel, EventModel, UserSchema, BookModel, AuthorModel

DJ_PATH = 'http://127.0.0.1:8000/'
users_schema = UserSchema(many=True)


@app.route('/')
def home():
    """Welcome page
    """

    return {
        'message': "hello"
    }


@app.route('/test', methods=["GET", "POST"])
def test():
    return {}


@app.route('/register', methods=['POST'])
def signup_user():
    credentials = request.json

    hashed_password = generate_password_hash(credentials['password'], method='sha256')

    new_user = UserModel(username=credentials['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'success registration'})


@app.route('/login', methods=['POST'])
def login_user():
    """Use POST request to send username and password and get token to authenticate"""

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = UserModel.query.filter_by(username=auth.username).first()
    if check_password_hash(user.password, auth.password):
        encoded_jwt = jwt.encode(
            {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=360)},
            config.Config.SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({'token': encoded_jwt})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})
