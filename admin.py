# admin.py

import pymongo
from datetime import datetime
import uuid

# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access the database
db = client['yelp']  

# Access the collections
review_collection = db['review']
user_collection = db['user']
business_collection = db['business']
admin_collection = db['admin']

def username_exist(username):
    # Check if the username exists in the admin collection
    existing_admin = admin_collection.find_one({"admin_username": username})
    return existing_admin is not None

def add_admin(business_name, business_address, business_city, admin_name, admin_username, 
              admin_email, admin_password, admin_password_confirm, threshold_percentage, last_n_reviews):
    if username_exist(admin_username):
        return "Username already exists for another admin"
    
    business = business_collection.find_one({"name": business_name, "address": business_address, "city": business_city})
    if not business:
        return "Business not found"
    business_id = business['business_id']

    existing_admin_with_business = admin_collection.find_one({"business_id": business_id})
    if existing_admin_with_business:
        return "Business already exists for another admin"

    if admin_password != admin_password_confirm:
        return "Passwords do not match"
    
    admin_id = str(uuid.uuid4())

    # Construct the admin document
    admin_doc = {
        "_id": admin_id,
        "admin_id": str(uuid.uuid4()),
        "admin_name": admin_name,
        "business_id": business_id,
        "admin_username": admin_username,
        "admin_email": admin_email,
        "admin_password": admin_password,
        "threshold_percentage": int(threshold_percentage),
        "last_n_reviews": int(last_n_reviews)
    }

    # Insert the admin document into the admin collection
    admin_collection.insert_one(admin_doc)
    return "Admin data added successfully"
