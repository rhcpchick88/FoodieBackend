from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid

# login post request
@app.post('/api/restaurant-login')
def restaurant_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email:
        return jsonify ("Missing required argument : email"), 422
    if not password:
        return jsonify ("Missing required argument : password"), 422
    run_query("SELECT FROM restaurant WHERE email=? and password=? VALUES(?,?)", [email,password])
    restaurant_token = uuid.uuid4().hex
    print(uuid.uuid4)
    run_query("INSERT INTO restaurant_session (token) VALUES(?)", [restaurant_token])
    #TODO  if not argument???? for login fail? check if email and pw matches?
    return jsonify("Email and password accepted, user logged in"), 200
