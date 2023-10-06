from flask import Flask, request
from flask_restful import Api, Resource
import json
from collections import OrderedDict

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-RESTful API
api = Api(app)

# Function to load data from the JSON file
def load_data():
    with open("data.json", "r") as file:
        return json.load(file)

# Function to save data back to the JSON file
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

# Function to get the next available ID based on the highest existing ID
def get_next_id(data):
    max_id = max([item["id"] for item in data])
    return max_id + 1

# Resource for handling multiple items (GET to retrieve all, POST to add new)
class ItemList(Resource):
    def get(self):
        return load_data(), 200

    def post(self):
        input_data = request.get_json()  # Get data from request payload
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
        item_data = request.get_json()  # Get data from request payload
        data = load_data()  # Load current data
        # Find the item with the specified ID
        item = next(filter(lambda x: x["id"] == item_id, data), None)
        if item:
            item.update(item_data)  # Update the item with new data
            save_data(data)  # Save updated data back to the JSON file
            return item, 200  # Return the updated item with HTTP status 200 (OK)
        return {"message": "Item not found"}, 404  # Item not found error

    def delete(self, item_id):
        data = load_data()  # Load current data
        # Remove the item with the specified ID from the list
        data = [item for item in data if item["id"] != item_id]
        save_data(data)  # Save updated data back to the JSON file
        return {"message": "Item deleted"}, 200  # Confirm deletion with HTTP status 200 (OK)

# Add resources to the API with their respective routes
api.add_resource(ItemList, "/items")
api.add_resource(Item, "/item/<int:item_id>")

# Start the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
