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
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Error, missing token"), 401
    restaurant_check = run_query("SELECT id from restaurant_session WHERE token=?",[token])
    response = restaurant_check[0]
    restaurant_id = response[0]
    print(restaurant_id)
    if restaurant_id == True:
        run_query("DELETE FROM restaurant_session WHERE id=?",[restaurant_id])
        return jsonify ("Logout successful"), 204
    else:
        return jsonify("Error logging out"), 401
