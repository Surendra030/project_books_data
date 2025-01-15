from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps
import os
app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection string
MONGO_URI = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URI)

# Database and collection
db = client.books_db
collection = db.books_data

@app.route('/')
def home():
    return jsonify({"message": "Backend server is running successfully"}), 200



@app.route('/save-page-num', methods=['POST'])
def save_page_num():
    data = request.get_json()
    file_name = data.get('file_name')
    page_number = data.get('page_number')

    if not file_name or not page_number:
        return jsonify({"error": "file_name and page_number are required"}), 400

    # Check if the book already exists in the database
    existing_book = collection.find_one({"book_name": file_name})

    if existing_book:
        # Update the current_page field for the existing book
        collection.update_one(
            {"book_name": file_name},
            {"$set": {"current_page": page_number}}
        )
    else:
        # Insert a new book entry
        collection.insert_one({"book_name": file_name, "current_page": page_number})

    return jsonify({"message": "Book data saved successfully"}), 200

@app.route('/get-page-num', methods=['GET'])
def get_page_num():
    # Fetch all documents from the collection
    books_data = list(collection.find({}, {"_id": 0}))  # Exclude the '_id' field from the response
    return jsonify(books_data), 200

if __name__ == '__main__':
    app.run(debug=True)
