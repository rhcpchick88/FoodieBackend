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
        return jsonify ("Missing required argument : email"), 422
    if not password:
        return jsonify ("Missing required argument : password"), 422
    run_query("SELECT FROM client WHERE email=? and password=? VALUES(?,?)", [email,password])
    client_token = uuid.uuid4().hex
    print(uuid.uuid4)
    run_query("INSERT INTO client_session (token) VALUES(?)", [client_token])
    #TODO  if not argument???? for login fail? using bcrypt to compare passwords error 401
    return jsonify("Email and password accepted, user logged in"), 201


# @app.delete('/api/client-login')
# def client_logout():
#     # TODO CONNECT TO CLIENT LOGIN TO GET TOKEN
#     data = request.json
#     client_token = data.get("sessionId")
#     run_query("DELETE FROM client_session WHERE token=? VALUES(?)", [client_token])





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

