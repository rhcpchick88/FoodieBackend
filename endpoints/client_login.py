from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query
import uuid
import bcrypt

# login post request
@app.post('/api/client-login')
def client_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email:
        return jsonify ("Missing required argument : email"), 401
    if not password:
        return jsonify ("Missing required argument : password"), 401
    password_check = run_query("SELECT password FROM client WHERE email=?", [email])
    response = password_check[0]
    client_password = response[0]
    # check entered password against the hashed password in the DB
    if bcrypt.checkpw(password.encode(), client_password.encode()):
        client_token = uuid.uuid4().hex
        print(uuid.uuid4)
        client_check = run_query("SELECT id FROM client WHERE email=?",[email])
        response = client_check[0]
        client_id = response[0]
        client_token = str(uuid.uuid4().hex)
        print(client_token)
        run_query("INSERT INTO client_session (id, token) VALUES (?,?)", [client_id, client_token])
        return jsonify("Email and password accepted, user logged in"), 201
    else:
        return jsonify("Error logging in, email and password combination not valid."), 401


#login delete request
@app.delete('/api/client-login')
def client_logout():
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Error, missing token"), 401
    client_check = run_query("SELECT id from client_session WHERE token=?",[token])
    response = client_check[0]
    client_id = response[0]
    print(client_id)
    # If the client is logged in you can log out
    if client_id == True:
        run_query("DELETE FROM client_session WHERE id=?", [client_id])
        return jsonify ("Logout successful"),204
    else: 
        return jsonify("Error logging out"),401