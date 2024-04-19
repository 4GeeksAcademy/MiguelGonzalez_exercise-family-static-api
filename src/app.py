"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
# Import necessary modules
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

# Initialize Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object and add initial members
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]})
jackson_family.add_member({"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]})
jackson_family.add_member({"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint to get all family members
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Endpoint to retrieve a single family member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        member["last_name"] = jackson_family.last_name
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404


# Endpoint to add a new family member
@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    if not all(key in data for key in ('first_name', 'age', 'lucky_numbers')):
        return jsonify({"error": "Bad request, missing fields"}), 400
    jackson_family.add_member(data)
    return jsonify({"message": "Member added successfully"}), 200

# Endpoint to delete a family member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result["done"]:
        return jsonify({"message": "Member deleted successfully"}), 200
    else:
        return jsonify({"error": "Member not found"}), 404
def delete_member(self, member_id):
    for index, member in enumerate(self.members):
        if member['id'] == member_id:
            del self.members[index]
            return {"done": True}
    return {"done": False}

# Run the application
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)