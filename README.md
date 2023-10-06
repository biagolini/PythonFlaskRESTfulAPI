# Flask Tutorial: Building a mock RESTful API

Welcome to this Flask tutorial! In this guide, you'll learn how to set up a mock RESTful API designed for controlling a shopping list. This API will allow you to add items to your list, update their details, retrieve the entire list, and delete items as needed.

## Prerequisites

- A computer with Python 3 installed.
- Basic knowledge of Python programming.
- Familiarity with terminal or command prompt.

## Setup Project

Python projects typically utilize virtual environments to prevent package conflicts. It's a best practice to have a separate virtual environment for each project.

### Create Virtual Environment

1. **Open a Terminal**.

2. **Update and Install Required Packages**:

```bash
sudo dnf update -y
sudo dnf install -y python3 python3-pip python3-venv
```

3. **Install Flask and Flask-RESTful**:

```bash
pip3 install flask flask-restful

```

_Note_: You can test the installation by running:

```bash
python3
>>> import flask_restful as fr
```

4. **Create a Project Directory**:

```bash
mkdir MockAPI
cd MockAPI
```

5. **Set Up a Virtual Environment**:

```bash
python3 -m venv venv
```

6. **Activate the Virtual Environment**:

```bash
source venv/bin/activate
```

7. **Install Flask Inside the Virtual Environment**:

```bash
pip install flask flask-restful
```

8. **Create Your Flask App**: Create a file named `app.py`. Refer to the `app.py` file in this repository to view the code.

9. **Run Your Flask App**:

```bash
python3 app.py
```

12. **Test your API**: Using tools like Postman or curl, you can send requests to your API and see the responses. The API should be running at http://127.0.0.1:5000/. Below is a breakdown of how to use each method (Remember to replace the example item details and IDs with your own values when testing the API):

- GET (/items): Retrieve the entire shopping list. Example using curl:
  ```bash
  curl http://127.0.0.1:5000/items
  ```
- POST (/items): Add a new item to the shopping list. You need to provide the item's details (excluding the ID) in the request body. Example using curl:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"units": 3, "description": "Apples"}' http://127.0.0.1:5000/items
  ```
- PUT (/item/<int:item_id>): Update the details of an existing item. Replace <int:item_id> with the item's ID and provide the new details in the request body. Example using curl:
  ```bash
  curl -X PUT -H "Content-Type: application/json" -d '{"units": 12, "description": "Apples"}' http://127.0.0.1:5000/item/8
  ```
- DELETE (/item/<int:item_id>): Remove an item from the shopping list. Replace <int:item_id> with the ID of the item you want to delete. Example using curl:
  ```bash
  curl -X DELETE http://127.0.0.1:5000/item/8
  ```
