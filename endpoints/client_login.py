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
    if True:
    # if bcrypt.checkpw(password.encode(), password_check.encode()):
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
        return jsonify("Error logging in, invalid password"), 401

        # return jsonify("Email and password combination not valid. Please try again.")
        #TODO  if not argument???? for login fail? using bcrypt to compare passwords error 401



@app.delete('/api/client-login')
def client_logout():
    # TODO CONNECT TO CLIENT LOGIN TO GET TOKEN
    data = request.json
    client_token = data.get("token")
    if token == 1:
        run_query("DELETE FROM client_session WHERE token=? VALUES(?)", [client_token])
        return jsonify ("Logout successful")
    else: 
        return jsonify("Error logging out")
    




# login logic:
# user gives you a username and pw
# you check the client table to see if there is a username and pw that matches
# if that query returns nothing you need to return an error saying doesnt match
# otherwise generate a token and return the token along side the user id that matched w/ username and password
# this is assuming w/o password encrypton

# select username from table, get their pw, then see if that pw
# for that user matchse the pw for the api call.

# you cannot do a select directly w/ hashed password
# mariadb does not know about encrypted pw so it will always return nothing
# basiclaly select for user and see what pw is, if it matches api call pw then that user is who they say they are.

# use select for password, do not use password in WHERE clause b/c it will never
# be satisfied as the password is ecrypted.

# extract encrypted password and use bcrypt to compare it to the
# password that was passed.
# if encryption taking too much time leeave and come back later.

