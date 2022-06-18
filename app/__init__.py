from flask import Flask, request, jsonify

app = Flask(__name__)

from endpoints import client_login, client, menu, orders, restaurant_login, restaurant