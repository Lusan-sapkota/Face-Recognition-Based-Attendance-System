# Face-Recognition-Based-Attendance-System
This project implements a Face Recognition-based Attendance System using Python, Flask, OpenCV, and machine learning techniques. The system automates the process of attendance tracking by recognizing faces captured through a webcam and marking attendance in a CSV file.

Key Components
Flask Application:

Provides a web interface for interacting with the system.
Contains routes for home, taking attendance, and adding new users.
OpenCV:

Used for capturing images from the webcam.
Implements face detection using Haar cascades (haarcascade_frontalface_default.xml).
Machine Learning:

Uses K-Nearest Neighbors (KNN) algorithm for face recognition.
Trains a model on the captured face images and saves it as face_recognition_model.pkl.
Data Management:

Stores captured face images in a directory structure.
Saves attendance records in CSV files, one for each day.
Project Structure
Directories:

Attendance/: Contains daily attendance CSV files.
static/: Contains static files such as face images and the trained model.
static/faces/: Stores individual face images for each user.
Files:

app.py: Main Flask application file.
haarcascade_frontalface_default.xml: Pre-trained model for face detection.
Functionality
Home Page:

Displays today's attendance records.
Shows the total number of registered users.
Provides buttons to take attendance and add new users.
Take Attendance:

Captures frames from the webcam.
Detects faces in real-time.
Identifies recognized faces using the trained model.
Marks attendance for identified users in the daily CSV file.
Add New User:

Captures multiple face images of a new user.
Stores the captured images in a directory named after the user.
Trains the face recognition model with the new data.
Key Functions
extract_faces(img): Detects faces in an image.
identify_face(facearray): Identifies a face using the trained KNN model.
train_model(): Trains the KNN model with the images of all registered users.
extract_attendance(): Extracts attendance records from the daily CSV file.
add_attendance(name): Adds a user's attendance record to the daily CSV file.
How to Run the Project
Setup:

Ensure you have Python and the required libraries installed (Flask, OpenCV, joblib, numpy, pandas, sklearn).
Run the Flask Application:

Execute python app.py in the terminal.
Open the web browser and go to http://127.0.0.1:5000/.
Use the Web Interface:

Use the "Take Attendance" button to start the attendance process.
Use the "Add New User" form to register new users by capturing their face images.
This project showcases the integration of computer vision, machine learning, and web development to create a functional and automated attendance system.

![Screenshot 2024-06-26 222155](https://github.com/Lusan-sapkota/Face-Recognition-Based-Attendance-System/assets/91797475/a306f668-d223-4450-99e7-f4181ef9ad5f)


