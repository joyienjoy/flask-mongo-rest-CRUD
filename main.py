from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId #create unique data ID
from flask import jsonify, request

@app.route('/')
def home():
    message = {
        'status': 200,
        'message': 'Working Link: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/add', methods=['POST'])
def add_user():
	json = request.json
	name = json['name']
	email = json['email']
	location = json['location']
	# validate the received values
	if name and email and location and request.method == 'POST':
		# save details
		id = mongo.db.user.insert_one({'name': name, 'email': email, 'location': location})
		resp = jsonify('User added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
@app.route('/users')
def users():
	users = mongo.db.user.find()
	resp = dumps(users)
	return resp
		
@app.route('/users/<id>')
def user(id):
	user = mongo.db.user.find_one({'_id':ObjectId(id)})
	resp = dumps(user)
	return resp

@app.route('/update', methods=['PUT'])
def update_user():
	json = request.json
	id = json['id']
	name = json['name']
	email = json['email']
	location = json['location']		
	# validate the received values
	if name and email and location and id and request.method == 'PUT':
		# save edits
		mongo.db.user.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {'name': name, 'email': email, 'location': location}})
		resp = jsonify('User updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	mongo.db.user.delete_one({'_id': ObjectId(id)})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
