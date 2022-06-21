from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query

# login post request
@app.post('/api/client-login')
def client_login():
    pass

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
