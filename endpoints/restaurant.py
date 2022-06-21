from app import app
from flask import request, jsonify
from helpers.dbhelpers import run_query
import bcrypt

#restaurant get request - doesnt need token as its public info
@app.get('/api/restaurant')
def restaurant_get():
    restaurant_list = run_query("SELECT * FROM restaurant")
    resp =[]
    for restaurant in restaurant_list:
        restaurant_obj={}
        restaurant_obj["restaurantId"] = restaurant[0]
        restaurant_obj["name"] = restaurant[1]
        restaurant_obj["email"] = restaurant[2]
        restaurant_obj["address"] = restaurant[4]
        restaurant_obj["phoneNum"] = restaurant[5]
        restaurant_obj["bio"] = restaurant[6]
        restaurant_obj["bannerUrl"] = restaurant[7]
        restaurant_obj["profileUrl"] = restaurant[8]
        restaurant_obj["city"] = restaurant[9]
        resp.append(restaurant_obj)
    return jsonify(restaurant_list), 200

# restaurant post request
@app.post('/api/restaurant')
def restaurant_post():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")    
    address = data.get("address")
    phoneNum = data.get("phoneNum")
    bio = data.get("bio")
    bannerUrl = data.get("bannerUrl")
    profileUrl = data.get("profileUrl")
    city = data.get("city")
    if not name:
        return jsonify ("Missing required argument : name"), 422
    if not email:
        return jsonify ("Missing required argument : email"), 422
    if not password:
        return jsonify ("Missing required argument : password"), 422
    if not address:
        return jsonify ("Missing required argument : address"), 422
    if not phoneNum:
        return jsonify ("Missing required argument : phone number)"), 422
    if not bio:
        return jsonify ("Missing required argument : bio"), 422
    if not city:
        return jsonify ("Missing required argument : city"), 422
    restaurantPassword = password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(restaurantPassword.encode(), salt)
    print(hashed_password)
    run_query("INSERT INTO restaurant (name, email, password, address, phone_num, bio, banner_url, profile_url, city) VALUES (?,?,?,?,?,?,?,?,?)", [name, email, hashed_password, address, phoneNum, bio, bannerUrl, profileUrl, city])
    return jsonify("Restaurant added successfully"), 201