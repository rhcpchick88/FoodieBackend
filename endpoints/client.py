from app import app
from flask import request, jsonify
from helpers.dbhelpers import run_query
import bcrypt
import hashlib


# client get request
@app.get('/api/client')
def client_get():
    client_list = run_query("SELECT * FROM client")
    resp = []
    for client in client_list:
        client_obj= {}
        client_obj["clientId"] = client[0]
        client_obj["email"] = client[1]        
        client_obj["username"] = client[2]
        client_obj["firstName"] = client[4]
        client_obj["lastName"] = client[5]
        client_obj["createdAt"] = client[6]        
        client_obj["pictureUrl"] = client[7]
        resp.append(client_obj)
    return jsonify(client_list), 200

# client post request
@app.post('/api/client')
def client_post():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    pictureUrl = data.get("pictureUrl")
    if not email:
        return jsonify ("Missing required argument : email"), 422
    if not username:
        return jsonify ("Missing required argument : username"), 422
    if not password:
        return jsonify ("Missing required argument : password"), 422
    if not firstName:
        return jsonify ("Missing required argument : first name"), 422
    if not lastName:
        return jsonify ("Missing required argument : last name)"), 422
    clientPassword = password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(clientPassword.encode(), salt)
    print(hashed_password)
    run_query("INSERT INTO client (email, username, password, first_name, last_name, picture_url) VALUES (?,?,?,?,?,?)", [email, username, hashed_password, firstName, lastName, pictureUrl])
    return jsonify("Client added successfully"), 201