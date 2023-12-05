from flask import Flask, render_template, request
import pymongo
import redis
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import uuid

app = Flask(__name__)

# Establish connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['yelp']  

# Access the collections
review_collection = db['review']
user_collection = db['user']
business_collection = db['business']
admin_collection = db['admin']

# Establish connection to Redis using Docker container host
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def email_exists(email):
    existing_admin = admin_collection.find_one({"admin_email": email})
    return existing_admin is not None

def business_exists(business_id):
    existing_admin = admin_collection.find_one({"business_id": business_id})
    return existing_admin is not None

def get_negative_reviews_count(business_id):
    # Get the count of negative reviews for a business
    negative_reviews_count = review_collection.count_documents({
        "business_id": business_id,
        "stars": {"$lt": 3}
    })
    return negative_reviews_count

def send_email(receiver_email, subject, body):
    sender_email = "aeidom@dhbw-loerrach.de"  # Replace with your email
    sender_password = "Maho2001;"   # Replace with your email password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def add_review_and_notify(business_name, stars, admin_email):
    # Find business_id based on business_name
    business = business_collection.find_one({"name": business_name})
    if not business:
        return "Business not found"
    business_id = business['business_id']

    # Generate new random IDs for review
    review_id = str(uuid.uuid4())

    # Get current date and time
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construct the review document
    review_doc = {
        "_id": review_id,
        "review_id": str(uuid.uuid4()),
        "business_id": business_id,
        "stars": stars,
        "date": current_date
    }

    # Insert the review document into the review collection
    review_collection.insert_one(review_doc)

    # Check if there are two or more negative reviews
    negative_reviews_count = get_negative_reviews_count(business_id)
    if negative_reviews_count >= 2:
        # Publish a message to Redis channel
        redis_channel = "admin_negative_reviews_channel"
        redis_message = f"Business: {business_name} received {negative_reviews_count} negative reviews"
        redis_client.publish(redis_channel, redis_message)

        # Send email notification
        email_subject = "Negative Reviews Notification"
        email_body = f"Dear Admin,\n\nYour business ({business_name}) has received {negative_reviews_count} negative reviews.\n\nSincerely,\nThe Review System"
        send_email(admin_email, email_subject, email_body)

    return "Review added successfully"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_review', methods=['POST'])
def add_review():
    business_name = request.form['business_name']
    stars = int(request.form['stars'])
    admin_email = request.form['admin_email']

    result = add_review_and_notify(business_name, stars, admin_email)
    return result

if __name__ == '__main__':
    app.run(debug=True)
