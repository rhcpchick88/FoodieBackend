from app import app
from flask import request, jsonify
from helpers.dbhelpers import run_query

@app.get('/api/menu')
def menu_get():
    menu_list = run_query("SELECT * FROM menu_items")
    resp = []
    for item in menu_list:
        menu_obj= {}
        menu_obj["menuId"] = item[0]
        menu_obj["name"] = item[1]        
        menu_obj["description"] = item[2]
        menu_obj["price"] = item[3]
        menu_obj["imageUrl"] = item[4]
        resp.append(menu_obj)
    return jsonify(menu_list), 200
#TODO 401 error code 

@app.post('/api/menu')
# TODO CONNECT TO RESTO LOGIN TO GET TOKEN
def menu_post():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    imageUrl = data.get("imageUrl")
    if not name:
        return jsonify ("Missing required argument : name"), 422
    if not description:
        return jsonify ("Missing required argument : description"), 422
    if not price:
        return jsonify ("Missing required argument : price"), 422
    run_query("INSERT INTO menu_items (name, description, price, image_url) VALUES (?,?,?,?)", [name, description, price, imageUrl])
    return jsonify("Menu item added successfully"), 201

@app.patch('/api/menu')
# TODO CONNECT TO RESTO LOGIN TO GET TOKEN
def menu_patch():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    imageUrl = data.get("imageUrl")
    if not name:
        return jsonify ("Missing required argument : name"), 422
    if not description:
        return jsonify ("Missing required argument : description"), 422
    if not price:
        return jsonify ("Missing required argument : price"), 422
    run_query("UPDATE menu_items (name, description, price, image_url) VALUES (?,?,?,?) WHERE id=?", [name, description, price, imageUrl])
    return jsonify("Menu item updated successfully"), 204

@app.delete('/api/menu')
def menu_delete():
    data = request.json
    menuId = data.get("menuId")
    run_query("DELETE FROM menu_items WHERE id=?"), [menuId]
    return jsonify("Menu item deleted successfully"), 204