from app import app
from flask import request, jsonify
from helpers.dbhelpers import run_query
import bcrypt
import uuid

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
#TODO 401 error code

# restaurant post request **does not need token!!**
#TODO email check - unique, phone check 
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
    # the city needs to exist in the DB in order fr the restaurant to be posted.
    city_check = run_query("SELECT id FROM city WHERE name=?", [city])
    if not city_check:
        return jsonify("Error, must enter correct city name"), 422
    else:    
        run_query("INSERT INTO restaurant (name, email, password, address, phone_num, bio, banner_url, profile_url, city) VALUES (?,?,?,?,?,?,?,?,?)", [name, email, hashed_password, address, phoneNum, bio, bannerUrl, profileUrl, city])
        restaurant_token = uuid.uuid4().hex
        print(uuid.uuid4)
        restaurant_check = run_query("SELECT id FROM restaurant WHERE email=?",[email])
        print(restaurant_check)
        response = restaurant_check[0]
        restaurant_id = response[0]
        restaurant_token = str(uuid.uuid4().hex)
        print(restaurant_token)
        run_query("INSERT INTO restaurant_session (id, token) VALUES (?,?)", [restaurant_id, restaurant_token])
        return jsonify("Restaurant added successfully"), 201

#TODO email check - unique, phone check 
@app.patch('/api/restaurant')
def restaurant_update():
    # requesting a token header to prove restaurant is logged in to make this request.
    token = request.headers.get("Token")
    if not token:
        return jsonify ("Not authorized"), 401
    else:
        token_check = run_query("SELECT id FROM restaurant_session WHERE token=?", [token])
        response = token_check[0]
        restaurant_id = response[0]
    if not restaurant_id:
        return jsonify("Error updating restaurant information, invalid login session"), 401
    else:
        data = request.json
        name = data.get("name")
        password = data.get("password")    
        address = data.get("address")
        phoneNum = data.get("phoneNum")
        bio = data.get("bio")
        bannerUrl = data.get("bannerUrl")
        profileUrl = data.get("profileUrl")
        city = data.get("city")
        token_check = run_query("SELECT id FROM restaurant_session WHERE token=?", [token])
        response = token_check[0]
        restaurant_id = response[0]     
        # I updated these individually as all the fields do not have to be updated
        # at the same time. What if they only want to update the name, or password etc.
        # EMAIL CANNOT BE CHANGED.
        if name:
            run_query("UPDATE restaurant SET name=? WHERE id=?", [name, restaurant_id])
            return jsonify("Restaurant name updated successfully"), 201
        if password:
            # encrypting the password for DB entry
            restaurantPassword = password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(restaurantPassword.encode(), salt)
            print(hashed_password)
            run_query("UPDATE restaurant SET password=? WHERE id=?", [hashed_password, restaurant_id])
            return jsonify("Restaurant password updated successfully"), 201                        
        if address:
            run_query("UPDATE restaurant SET address=? WHERE id=?", [address, restaurant_id])
            return jsonify("Restaurant address updated successfully"), 201            
        if phoneNum:
            run_query("UPDATE restaurant SET phone_num=? WHERE id=?", [phoneNum, restaurant_id])
            return jsonify("Restaurant phone number updated successfully"), 201
        if bio:
            run_query("UPDATE restaurant SET bio=? WHERE id=?", [bio, restaurant_id])
            return jsonify("Restaurant bio updated successfully"), 201
        if bannerUrl:
            run_query("UPDATE restaurant SET banner_url=? WHERE id=?", [bannerUrl, restaurant_id])
            return jsonify("Restaurant banner URL updated successfully"), 201
        if profileUrl:
            run_query("UPDATE restaurant SET profile_url=? WHERE id=?", [profileUrl, restaurant_id])
        if city:
            city_check = run_query("SELECT id FROM city WHERE name=?", [city])
            if not city_check:
                return jsonify("Error, must enter correct city name"), 422         
            else:
                run_query("UPDATE restaurant SET city=? WHERE id=?", [city, restaurant_id])
                return jsonify("Restaurant city updated successfully"), 201                
        else:
            return jsonify("Error updating restaurant"), 401
