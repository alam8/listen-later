from flask import Flask, jsonify, request

app = Flask(__name__)

items = [
    { 'description': 'salary', 'amount': 5000 }
]

@app.route("/items")
def get_items():
    return jsonify(items)

@app.route("/items", methods=['POST'])
def add_item():
    items.append(request.get_json())
    return '', 204