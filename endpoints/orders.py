from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query

@app.get('/api/order')
def order_get():
    data = request.json
    client_login = run_query("SELECT token FROM client_session WHERE id=?")
    return jsonify(client_login)
    restaurant_login = run_query("SELECT token FROM restaurant_session WHERE id=?")
    return jsonify(restaurant_login)
    if client_login:
        pass
    elif restaurant_login:
        pass
    else:
        pass

# Else if logic - if id is in client session then go to client get, if it is in 
# restuarant session then go to restaurant, If none then it will not work.

# FOR CLIENT:
# NEED LOGIN TOKEN AND CLIENT ID IN ORDER TO VIEW ORDER
# GET ALLOWS CLIENT TO VIEW ALL ORDERS



@app.post('/api/order')
def create_order():
    pass
    # data = request.json
    # restaurantId = data.get("restaurantId")
    # menuItem = data.get("menuItem")
    # if not menuItem:
    #     return jsonify ("Missing required argument : Menu item")
    
    # LOGIC:
    # NEED TO ASSIGN THE POSTED ORDER TO THE CLIENT ID 
    
    # this needs to connect the order_menu_item and orders/menu_item tables.
    # orders : id, booleans created_at, is_confirmed, is_completed
    # is_cancelled.
    #order_menu_item : id
    # This takes the menu item ID and adds them to the order, which then
    # posts the order with the corresponding item ID's in an array to the API.
    # The order_menu_item only has one column ID which contains the order ID
    # and connects to the menu_item table to bring the corresponding menu items 
    # from that table and sends it in an array ALONG SIDE the information
    # from orders.
    
    # I will need three tables for client request.THIS IS ONLY FOR CLIENT.
    # RESTAURANT CANNOT POST ORDERS. SO I NEED A TOKEN TO MAKE THIS REQUEST.
    
    # POST ORDER - sends menu item array from menu_items, creates booleans
    # created_at, is_confirmed, is_completed, is_cancelled (confirmation,
    # completeion, cancellation will not be done by client)and connects them
    # to order_menu_item id.

# post gives restaurant items 



# per mark
# A client provides u with two things as parameters.
# 1) restaurant ID, 2) list of items  (Item ID's)
# insrt 3rd thing which is client ID of client who is making order.
# with those 3 things you can makea table. The ORDER TABLE order ID is auto assigned as well as timestamp
# and the 3 booleans are auto 0 (false) - Provide the client ID and the resto ID to connect to 
# order table.
# 2nd step is an array of order items - once the ORDER IS CREATED - grab that order
# and insert items using cross-ref table w/resto and client ID
# Each new row inserted into the table will have order ID and one by one the items id.
# this is just for posting.

