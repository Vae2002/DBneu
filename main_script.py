import pymongo
import redis
import uuid
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime

from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Establish connection to Redis using Docker container host
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Access the database
db = client['yelp']

# Access the collections
review_collection = db['review']
user_collection = db['user']
business_collection = db['business']
admin_collection = db['admin']

def add_review(user_name, business_name, business_address, business_city, stars, useful, funny, cool, text):
    # Generate new random IDs for review and user
    review_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # Get current date and time
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Find business_id based on business_name, business_address, and business_city
    business = business_collection.find_one({"name": business_name, "address": business_address, "city": business_city})
    if not business:
        return "Business not found"
    business_id = business['business_id']

    # Find user_id based on user_name
    user = user_collection.find_one({"name": user_name})
    if not user:
        return "User not found"
    user_id = user['user_id']

    stars = int(stars)
    useful = int(useful)
    funny = int(funny)
    cool = int(cool)

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
        "text": text,
        "date": current_date
    }

    # Insert the review document into the review collection
    review_collection.insert_one(review_doc)
    return "Review added successfully"

# Homepage, um Bewertungen hinzuzufügen
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpunkt zum Hinzufügen einer Bewertung über ein Formular
@app.post("/add_review/", response_class=HTMLResponse)
def add_review_form(
    request: Request,
    user_name: str = Form(...),
    business_name: str = Form(...),
    business_address: str = Form(...),
    business_city: str = Form(...),
    stars: int = Form(...),
    useful: int = Form(...),
    funny: int = Form(...),
    cool: int = Form(...),
    text: str = Form(...),
):
    result = add_review(user_name, business_name, business_address, business_city, stars, useful, funny, cool, text)
    return templates.TemplateResponse("result.html", {"request": request, "result": result})


app.mount("/static", StaticFiles(directory="static"), name="static")

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

# New route for admin registration form
@app.post("/register_admin", response_class=HTMLResponse)
async def register_admin(
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
    last_n_reviews: int = Form(...),
):
    result = add_admin(
        business_name,
        business_address,
        business_city,
        admin_name,
        admin_username,
        admin_email,
        admin_password,
        admin_password_confirm,
        threshold_percentage,
        last_n_reviews,
    )
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

# Home route for the main form
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})