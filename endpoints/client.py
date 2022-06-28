from app import app
from flask import request, jsonify
from helpers.dbhelpers import run_query
import bcrypt
import uuid


# client get request
@app.get('/api/client')
def client_get():
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM client_session WHERE token=?", [token])
        response = token_check[0]
        client_id = response[0]        
        client_list = run_query("SELECT * FROM client WHERE id=?",[client_id])
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
#TODO 401 error code 

# client post request **does not need token!! **
#TODO email check - unique
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
    client_token = uuid.uuid4().hex
    print(uuid.uuid4)
    client_check = run_query("SELECT id FROM client WHERE email=?",[email])
    response = client_check[0]
    client_id = response[0]
    client_token = str(uuid.uuid4().hex)
    print(client_token)
    run_query("INSERT INTO client_session (id, token) VALUES (?,?)", [client_id, client_token])
    return jsonify("Client added successfully"), 201

#TODO email check - unique
@app.patch('/api/client')
def client_update():
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM client_session WHERE token=?", [token])
        response = token_check[0]
        client_id = response[0]
    if not client_id:
        return jsonify("Error updating client information, invalid login session")
    else:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        pictureUrl = data.get("pictureUrl")
        token_check = run_query("SELECT id FROM client_session WHERE token=?", [token])
        response = token_check[0]
        client_id = response[0]
        print(client_id)        
        if username:
            run_query("UPDATE client SET username=? WHERE id=?", [username, client_id])
            return jsonify("Client username updated successfully"), 201
        if password:
            clientPassword = password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(clientPassword.encode(), salt)
            print(hashed_password)            
            run_query("UPDATE client SET password=? WHERE id=?", [hashed_password, client_id])
            return jsonify("Client password updated successfully"), 201            
        if firstName:
            run_query("UPDATE client SET first_name=? WHERE id=?", [firstName, client_id])
            return jsonify("Client first name updated successfully"), 201              
        if lastName:
            run_query("UPDATE client SET last_name=? WHERE id=?", [lastName, client_id])
            return jsonify("Client last name updated successfully"), 201              
        if pictureUrl:
            run_query("UPDATE client SET picture_url=? WHERE id=?", [pictureUrl, client_id])            
            return jsonify("Client picture URL updated successfully"), 201
        else:
            return jsonify("Error updating client")          

@app.delete('/api/client')
def client_delete():
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM client_session WHERE token=?", [token])
        response = token_check[0]
        client_id = response[0]
        if not client_id:
            return jsonify("Error deleting profile")
        else:
            token_check = run_query("SELECT id FROM client_session WHERE token=?", [token])
            response = token_check[0]
            client_id = response[0]
            run_query("DELETE FROM client_session WHERE id=?", [client_id])
            run_query("DELETE FROM client WHERE id=?", [client_id])
            return jsonify("Profile deleted successfully, logged out"), 204