from app import app
from flask import jsonify
from helpers.dbhelpers import run_query

# @app.get('/api/order')
# def order_get():
#     # TODO CONNECT TO CLIENT AND RESTO LOGIN TO GET TOKEN
#     #TODO SPECIFY REQUIREMENTS FOR CLIENT AND RESTO GET REQUEST
#     #TODO CLIENT GET FOR THEIR ORDER ONLY
#     #TODO RESTAURANT GET ALL ORDER FOR THEIR RESTAURANT
#     order_info = run_query("SELECT * FROM orders")
#     resp = []
#     order_id = run_query("SELECT * FROM order_menu_item")
#     resp = []
#     for info in order_info:
#         order_obj={}
#         order_obj[clien] = info[0]
#         order_obj[] = info[1]
#         order_obj[] = info[2]
#         order_obj[] = info[3]
#         order_obj[] = info[4]
#         resp.append(order_obj)
#     return jsonify(order_info), 200
# #TODO 401 error code

# COME BACK TO THIS AS THE ARRAYS NEED TO GRAB DIFFERENT INFO
# FROM DIFFERENT PLAES - DO THE LOGIC