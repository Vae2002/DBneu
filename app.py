# main.py
from flask_cors import CORS

from flask import Flask, render_template, request, jsonify
import pymongo
from datetime import datetime
import uuid
from admin import add_admin  # Import the add_admin function from admin.py

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access the database
db = client['yelp']

# Access the collections
review_collection = db['review']
user_collection = db['user']
business_collection = db['business']
admin_collection = db['admin']

def add_review(data):
    # Generate new random IDs for review and user
    review_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # Get current date and time
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Find business_id based on business_name, business_address, and business_city
    business = business_collection.find_one({"name": data['businessName'], "address": data['businessAddress'], "city": data['businessCity']})
    if not business:
        return "Business not found"
    business_id = business['business_id']

    # Find user_id based on user_name
    user = user_collection.find_one({"name": data['userName']})
    if not user:
        return "User not found"
    user_id = user['user_id']

    stars = int(data['stars'])
    useful = int(data['useful'])
    funny = int(data['funny'])
    cool = int(data['cool'])

    # Construct the review document
    review_doc = {
        "_id": review_id,
        "review_id": str(uuid.uuid4()),
        "user_id": user_id,
        "business_id": business_id,
        "stars": stars,
        "useful": useful,
        "funny": funny,
        "cool": cool,
        "text": data['text'],
        "date": current_date
    }

    # Insert the review document into the review collection
    review_collection.insert_one(review_doc)
    return "Review added successfully"

# Route to handle admin creation
@app.route('/api/add_admin', methods=['POST'])
def api_add_admin():
    data = request.get_json()

    result = add_admin(
        business_name=data['businessName'],
        business_address=data['businessAddress'],
        business_city=data['businessCity'],
        admin_name=data['adminName'],
        admin_username=data['adminUsername'],
        admin_email=data['adminEmail'],
        admin_password=data['adminPassword'],
        admin_password_confirm=data['adminPasswordConfirm'],
        threshold_percentage=data['thresholdPercentage'],
        last_n_reviews=data['lastNReviews']
    )

    if result == "Admin data added successfully":
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": result}), 500

# Route to handle review creation
@app.route('/api/add_review', methods=['POST'])
def api_add_review():
    data = request.get_json()

    result = add_review(data)

    if result == "Review added successfully":
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
