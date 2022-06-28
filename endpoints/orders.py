from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query

# getting order info
@app.get('/api/order')
def order_get():
    # checking on client and/or restaurant tokens.
    client_check = run_query("SELECT id FROM client_session WHERE token=?", [token])
    response = client_check[0]
    client_id = response[0]
    return jsonify(client_check),200
    restaurant_check = run_query("SELECT id FROM restaurant_session WHERE token=?", [token])
    response = restaurant_check[0]
    restaurant_id = response[0]
    return jsonify(restaurant_check),200
# if a client is logged in
    if client_check:
        order_info = run_query("SELECT * FROM orders WHERE client_id=?", [client_id])
        resp = []
        for info in order_info:
            order_obj = {}
            order_obj["clientId"] = order_obj[5]
            order_obj["createdAt"] = order_obj[1]
            order_obj["isCancelled"] = order_obj[4]
            order_obj["isComplete"] = order_obj[3]
            order_obj["isConfirmed"] = order_obj[2]
            order_obj["orderId"] = order_obj[0]
            order_obj["restaurantId"] = order_obj[6]
            resp.append(order_obj)
        return jsonify (order_info)
        restaurant_check = run_query("SELECT restaurant_id FROM orders WHERE client_id=?", [client_id])
        response = restaurant_check[0]
        restaurant_id = response[0]    
        item_info = run_query("SELECT * FROM menu_items WHERE restaurant_id=?",[restaurant_id])
        resp = []
        for item in item_info:
            item_obj={}
            item_obj["items"] = item_info[0]
            resp.append(item_obj)
        return jsonify(item_info),200
            # if a restaurant logged in
    elif restaurant_check:
        order_info = run_query("SELECT * FROM orders WHERE restaurant_id=?", [restaurant_id])
        for order in order_info:
            resp = []
            order_obj = {}
            order_obj["clientId"] = order_obj[5]
            order_obj["createdAt"] = order_obj[1]
            order_obj["isCancelled"] = order_obj[4]
            order_obj["isComplete"] = order_obj[3]
            order_obj["isConfirmed"] = order_obj[2]
            order_obj["orderId"] = order_obj[0]
            order_obj["restaurantId"] = order_obj[6]
            resp.append(order_obj)
        return jsonify (order_info),200
        item_info = run_query("SELECT * FROM menu_items WHERE restaurant_id=?",[restaurant_id])
        resp = []
        for item in item_info:
            item_obj={}
            item_obj["items"] = item_info[0]
            resp.append(item_obj)
        return jsonify(item_info),200
    else:
        return jsonify("Not authorized"), 401

@app.post('/api/order')
def create_order():
    # requesting a token header to prove client is logged in to make this request.
    token = request.headers.get("Token")
    token_check = run_query("SELECT id FROM client_session WHERE token=?", [token])
    response = token_check[0]
    client_id = response[0]    
    if not client_id:
        return jsonify("Not authorized"),401
    data = request.json
    restaurant_id = data.get("restaurantId")
    if not restaurant_id:
        return jsonify ("Error, no restaurant ID"), 422
    items = data.get("items")
    if not items:
        return jsonify ("Error, no menu items selected"), 422
    run_query("INSERT INTO orders (client_id, restaurant_id) VALUES (?,?)", [client_id, restaurant_id])
    #I dont need to insert boolean values as they are already assigned "0" as soon as an order w/ restaurant ID and client ID is made.
    order = run_query("SELECT id FROM orders WHERE client_id=? AND restaurant_id=?", [client_id, restaurant_id])
    order_response = order[0]
    order_query = order_response[0]
    order_id = int(order_query)
    run_query("INSERT INTO order_menu_item (order_id, item_id) VALUES (?,?)", [order_id, items])
    return jsonify("Item successfully added to order"),200
# couldn't get this one working

