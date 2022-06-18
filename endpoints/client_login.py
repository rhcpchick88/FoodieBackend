from lib2to3.pgen2 import token
from app import app
from flask import jsonify, request
from helpers.dbhelpers import run_query

# login post request
@app.post('/api/client-login')
def client_login():
    pass