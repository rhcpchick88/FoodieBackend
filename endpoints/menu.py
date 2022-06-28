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
        menu_obj["restaurantId"] = item[5]
        resp.append(menu_obj)
    return jsonify(menu_list), 200
#TODO 401 error code 

@app.post('/api/menu')
def menu_post():
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Error, missing token"), 401
    restaurant_check = run_query("SELECT id from restaurant_session WHERE token=?",[token])
    response = restaurant_check[0]
    restaurant_id = response[0]
    if not restaurant_id:
        return jsonify("Error adding menu item")
    else:    
        data = request.json
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        imageUrl = data.get("imageUrl")
        token = request.headers.get("Token")        
        restaurant_check = run_query("SELECT id from restaurant_session WHERE token=?",[token])
        response = restaurant_check[0]
        restaurant_id = response[0]      
        if not name:
            return jsonify ("Missing required argument : name"), 422
        if not description:
            return jsonify ("Missing required argument : description"), 422
        if not price:
            return jsonify ("Missing required argument : price"), 422
        run_query("INSERT INTO menu_items (name, description, price, image_url, restaurant_id) VALUES (?,?,?,?,?)", [name, description, price, imageUrl, restaurant_id])
        return jsonify("Menu item added successfully"), 201

@app.patch('/api/menu')
def menu_patch():
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Error, missing token"), 401
    restaurant_check = run_query("SELECT id from restaurant_session WHERE token=?",[token])
    response = restaurant_check[0]
    restaurant_id = response[0]
    print(restaurant_id)
    if restaurant_id == True:     
        data = request.json
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        imageUrl = data.get("imageUrl")
        token_check = run_query("SELECT id FROM restaurant_session WHERE token=?", [token])
        response = token_check[0]
        restaurant_id = response[0]          
        if name:
            run_query("UPDATE menu SET name=? WHERE id=?", [name, restaurant_id])
            return jsonify("Name updated successfully")
        if description:
            run_query("UPDATE menu SET description=? WHERE id=?", [description, restaurant_id])
            return jsonify("Description updated successfully")
        if price:
            run_query("UPDATE menu SET price=? WHERE id=?", [price, restaurant_id])
            return jsonify("Price updated successfully")
        if imageUrl:
            run_query("UPDATE menu SET image_url WHERE id=?", [imageUrl, restaurant_id])
            return jsonify("Image URL updated successfully")
        else:
            return jsonify("Error updating menu item")

@app.delete('/api/menu')
def menu_delete():
    data = request.json
    menuId = data.get("menuId")
    run_query("DELETE FROM menu_items WHERE id=?"), [menuId]
    return jsonify("Menu item deleted successfully"), 204