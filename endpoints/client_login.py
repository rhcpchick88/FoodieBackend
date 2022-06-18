from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query

@app.post('/api/client-login')
def client_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email:
        return jsonify ("Missing required argument : email"), 422
    if not password:
        return jsonify ("Missing required argument : password"), 422
    run_query("INSERT INTO client (email, username, firstName, lastName, pictureUrl) VALUES (?,?,?,?,?)", [email, username, firstName, lastName, pictureUrl])
    return jsonify("Client added successfully"), 201