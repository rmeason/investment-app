from flask import Blueprint, jsonify

# Define the Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Investment AI Application is running!"})
