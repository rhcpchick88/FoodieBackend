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

# creating a menu item.
@app.post('/api/menu')
def menu_post():
    # requesting a token header to prove restaurant is logged in to make this request.    
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Error, missing token"), 401
    restaurant_check = run_query("SELECT id from restaurant_session WHERE token=?",[token])
    response = restaurant_check[0]
    restaurant_id = response[0]
    if not restaurant_id:
        return jsonify("Error adding menu item"),401
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

# updating a menu item.
@app.patch('/api/menu')
def menu_patch():
    # requesting a token header to prove restaurant is logged in to make this request.    
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
            return jsonify("Name updated successfully"), 200
        if description:
            run_query("UPDATE menu SET description=? WHERE id=?", [description, restaurant_id])
            return jsonify("Description updated successfully"), 200
        if price:
            run_query("UPDATE menu SET price=? WHERE id=?", [price, restaurant_id])
            return jsonify("Price updated successfully"), 200
        if imageUrl:
            run_query("UPDATE menu SET image_url WHERE id=?", [imageUrl, restaurant_id])
            return jsonify("Image URL updated successfully"), 200
        else:
            return jsonify("Error updating menu item"), 422

# deleting a menu item.
@app.delete('/api/menu')
def menu_delete():
    # requesting a token header to prove restaurant is logged in to make this request.    
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM restaurant_session WHERE token=?", [token])
        response = token_check[0]
        restaurant_id = response[0]
        if not restaurant_id:
            return jsonify("Error, invalid restaurant ID"), 401
        else:
            data = request.json
            item_id = data.get("menuId")
            if not item_id:
                return jsonify("Error, no menu item ID."), 422
            menu_id = int(item_id)
            run_query("DELETE FROM menu_items WHERE id=?", [menu_id])
            return jsonify("Menu item deleted successfully"), 204