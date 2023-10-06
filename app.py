import os
import json
from flask import Flask, request
from flask_restful import Api, Resource
from collections import OrderedDict

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-RESTful API
api = Api(app)

# Check if JSON file exists
def json_file_exists():
    return os.path.exists("data.json")

# Function to load data from the JSON file
def load_data():
    if json_file_exists():
        with open("data.json", "r") as file:
            return json.load(file)
    return []

# Function to save data back to the JSON file
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

# Function to get the next available ID based on the highest existing ID
def get_next_id(data):
    max_id = max([item["id"] for item in data])
    return max_id + 1

# Function to validate inputs
def check_data(item_data):
    if not item_data.get('units') or not isinstance(item_data.get('units'), int) or item_data.get('units') <= 0:
        return {"message": "The 'units' field is required and must be a positive integer."}, 400
    if not item_data.get('description') or len(item_data.get('description').strip()) == 0:
        return {"message": "The 'description' field is required and cannot be empty."}, 400
    return None

# Function to validate inputs
def check_missing_data(item):
    if not item:
        return {"message": "Item not found"}, 404  # If item was not found, return an error   
    return None

# Resource for handling multiple items (GET to retrieve all, POST to add new)
class ItemList(Resource): # This class inherits from Resource, which is a class provided by the flask_restful extension. This allows the class to leverage various functionalities offered by flask_restful for creating API endpoints (as will be done later with the add_resource method).
    def get(self):
        return load_data(), 200

    def post(self):
        input_data = request.get_json()  # Get data from request payload        
        error = check_data(input_data)  # Validation
        if error:
            return error
        data = load_data()  # Load current data
        new_id = get_next_id(data)  # Get next ID for the new item
        # Create a new item using OrderedDict to maintain order
        new_item = OrderedDict([
            ("id", new_id),
            ("units", input_data["units"]),
            ("description", input_data["description"])
        ])
        data.append(new_item)  # Add new item to the list
        save_data(data)  # Save updated data back to the JSON file
        return new_item, 201  # Return the new item with HTTP status 201 (created)

# Resource for handling individual items (PUT to update, DELETE to remove)
class Item(Resource): 
    def put(self, item_id):
        input_data = request.get_json()  # Get data from request payload
        error = check_data(input_data)  # Validation
        if error:
            return error
        data = load_data()  # Load current data
        # Find the item with the specified ID
        item = next(filter(lambda x: x["id"] == item_id, data), None)
        error = check_missing_data(item) # If item was not found, return an error  
        if error:
            return error         
        input_data.pop('id', None) # Remove 'id' from input data to prevent ID updates
        item.update(input_data)  # Update the item with new data
        save_data(data)  # Save updated data back to the JSON file
        return item, 200  # Return the updated item with HTTP status 200 (OK)
        
    def delete(self, item_id):
        data = load_data()  # Load current data
        # Find the item with the specified ID
        item = next(filter(lambda x: x["id"] == item_id, data), None)
        error = check_missing_data(item) # If item was not found, return an error  
        if error:
            return error         
        # Create a new list excluding the item with the provided ID
        updated_items = [item for item in data if item["id"] != item_id]
        save_data(updated_items)  # Save updated data back to the JSON file
        return {"message": "Item deleted"}, 200  # Confirm deletion with HTTP status 200 (OK)

# Add resources to the API with their respective routes
api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<int:item_id>")

# Start the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
