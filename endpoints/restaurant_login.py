from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

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
    password_check = run_query("SELECT password FROM restaurant WHERE email=?", [email])
    response = password_check[0]
    restaurant_password = response[0]
    print(restaurant_password)
    if bcrypt.checkpw(password.encode(), restaurant_password.encode()):
        restaurant_token = uuid.uuid4().hex
        print(uuid.uuid4)
        restaurant_check = run_query("SELECT id FROM restaurant WHERE email=?",[email])
        response = restaurant_check[0]
        restaurant_id = response[0]
        restaurant_token = str(uuid.uuid4().hex)
        print(restaurant_token)
        run_query("INSERT INTO restaurant_session (id, token) VALUES (?,?)", [restaurant_id, restaurant_token])
        return jsonify("Email and password accepted, user logged in"), 201
    else:
        return jsonify("Error logging in, email and password combination not valid."), 401

@app.delete('/api/restaurant-login')
def restaurant_logout():
    # TODO CONNECT TO RESTAURANT LOGIN TO GET TOKEN
    data = request.json
    restaurant_token = data.get("token")
    if token == 1:
        run_query("DELETE FROM restaurant_session WHERE token=? VALUES(?)", [restaurant_token])
        return jsonify ("Logout successful")
    else:
        return jsonify("Error logging out")




# per mark
# logic of token authorizaiton. 
# when a specific operation requires a user to identify themselves they do it with a token.
# you cannot just let anyone patch a client or resto etc etc etc.
# request a user to send a token. FE sends a token, reference the session table and select
# the row with that token, if that token exists grab the ID associated to that token and that
# is how you know who made the request.Token is good enough verification for the user identification
# if it returns nothing it is not valid
# once you have that you have the ID and you can do whatever operation is required.
