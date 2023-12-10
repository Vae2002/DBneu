# DBneu
# Yelp Review System

This project was developed as part of the Databases module at DHBW Lörrach by students Vae Tiolamon, Mihabt Aeido, and Tristan Hein. The Yelp Review System facilitates the management of reviews, users, businesses, and administrators. Below are the key components of the project.

## Functionalities

### 1. Search for Reviews

The system allows administrators to search for reviews for a specific business. This can include all reviews or those within a specified time range and with a particular star rating.

### 2. Insert Administrator Data

Administrators can be added to the system by providing relevant information such as name, username, email, password, threshold for negative reviews, and the number of last reviews checked.

### 3. Insert Review Data

It is possible to insert review data by specifying usernames, business information, and other relevant details.

### 4. Email Notifications

The system can automatically send email notifications to administrators when the threshold for negative reviews is exceeded. This is based on the last reviews checked for a business.

## Technologies Used

The Yelp Review System utilizes various technologies, including MongoDB for the database, Redis for publishing notifications, SMTP for sending emails, and FastAPI for implementing an API.

## Note

This project was developed as part of the Databases module at DHBW Lörrach and serves as a practical example of applying database concepts and technologies in real-world scenarios. It enables effective review management and provides an automated notification function for administrators to respond to negative reviews.
