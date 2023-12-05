# add_admin.py

import pymongo
from datetime import datetime
import uuid
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access the database
db = client['yelp']

# Access the collections
admin_collection = db['admin']
business_collection = db['business']

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def username_exist(username):
    # Check if the username exists in the admin collection
    existing_admin = admin_collection.find_one({"admin_username": username})
    return existing_admin is not None

def add_admin(business_name, business_address, business_city, admin_name, admin_username, admin_email, admin_password, admin_password_confirm, threshold_percentage, last_n_reviews):
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

@app.post("/add_admin", response_class=HTMLResponse)
async def add_admin_route(
    request: Request,
    business_name: str = Form(...),
    business_address: str = Form(...),
    business_city: str = Form(...),
    admin_name: str = Form(...),
    admin_username: str = Form(...),
    admin_email: str = Form(...),
    admin_password: str = Form(...),
    admin_password_confirm: str = Form(...),
    threshold_percentage: int = Form(...),
    last_n_reviews: int = Form(...)
):
    result = add_admin(
        business_name=business_name,
        business_address=business_address,
        business_city=business_city,
        admin_name=admin_name,
        admin_username=admin_username,
        admin_email=admin_email,
        admin_password=admin_password,
        admin_password_confirm=admin_password_confirm,
        threshold_percentage=threshold_percentage,
        last_n_reviews=last_n_reviews
    )

    return templates.TemplateResponse("add_admin_result.html", {"request": request, "result": result})
