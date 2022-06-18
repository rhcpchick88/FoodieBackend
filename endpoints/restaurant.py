from app import app
from flask import jsonify
from helpers.dbhelpers import run_query

@app.get('/client')
def user_get():
    return jsonify("endpoint"), 200
