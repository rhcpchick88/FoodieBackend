from flask import Flask

app = Flask(__name__)

from endpoints import client_login
from endpoints import client
from endpoints import menu
from endpoints import orders
from endpoints import restaurant_login
from endpoints import restaurant