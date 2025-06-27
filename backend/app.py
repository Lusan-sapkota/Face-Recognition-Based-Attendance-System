import cv2
import os
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import date, datetime, timedelta
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
from dotenv import load_dotenv
import bcrypt
import json
import zipfile
from database import Database

# Load environment variables
load_dotenv()

# Initialize database
db = Database()

# Defining Flask App
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'], 
     allow_headers=['Content-Type', 'Authorization'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
jwt = JWTManager(app)

# Handle OPTIONS requests for CORS preflight
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

# Number of images to take for each user (reduced for faster capture)
nimgs = 3

# Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")

# Initializing VideoCapture object to access WebCam
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# If these directories don't exist, create them
if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static'):
    os.makedirs('static')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if not os.path.isdir('notices'):
    os.makedirs('notices')

# Create attendance file if it doesn't exist
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    with open(f'Attendance/Attendance-{datetoday}.csv', 'w') as f:
        f.write('Name,Roll,Time,Type\n')

# Create users database if it doesn't exist
if not os.path.exists('users.json'):
    with open('users.json', 'w') as f:
        json.dump({}, f)

# Create notices file if it doesn't exist
if not os.path.exists('notices/notices.json'):
    with open('notices/notices.json', 'w') as f:
        json.dump([], f)

# Get the number of total registered users
def totalreg():
    return len(db.get_all_users())

# Extract the face from an image with optimized parameters
def extract_faces(img):
    if img is not None and img.size != 0:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply histogram equalization for better detection
        gray = cv2.equalizeHist(gray)
        
        # Optimized parameters for faster and more accurate detection
        face_points = face_detector.detectMultiScale(
            gray, 
            scaleFactor=1.05,  # More precise scaling
            minNeighbors=4,    # Balanced for accuracy vs speed
            minSize=(100, 100), # Larger minimum for better quality faces
            maxSize=(500, 500), # Maximum size limit
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Filter faces by quality (size and position)
        quality_faces = []
        for (x, y, w, h) in face_points:
            # Check if face is reasonably centered and sized
            if w > 120 and h > 120:  # Ensure minimum quality
                quality_faces.append((x, y, w, h))
        
        return quality_faces
    else:
        return []

# Identify face using ML model
def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

# A function which trains the model on all the faces available in database
def train_model():
    faces = []
    labels = []
    users = db.get_all_users()
    
    if len(users) == 0:
        return False
    
    for user in users:
        user_key = f"{user['name']}_{user['user_id']}"
        user_path = f'static/faces/{user_key}'
        if os.path.isdir(user_path):
            for imgname in os.listdir(user_path):
                img_path = f'{user_path}/{imgname}'
                if os.path.isfile(img_path):
                    img = cv2.imread(img_path)
                    if img is not None:
                        resized_face = cv2.resize(img, (50, 50))
                        faces.append(resized_face.ravel())
                        labels.append(user_key)
    
    if len(faces) > 0:
        faces = np.array(faces)
        knn = KNeighborsClassifier(n_neighbors=min(5, len(set(labels))))
        knn.fit(faces, labels)
        joblib.dump(knn, 'static/face_recognition_model.pkl')
        return True
    return False

# Extract info from today's attendance from database
def extract_attendance():
    try:
        datetoday = date.today().strftime("%m_%d_%y")
        attendance_records = db.get_attendance(datetoday)
        # Convert to old format for compatibility
        formatted_records = []
        for record in attendance_records:
            formatted_records.append({
                'Name': record['name'],
                'Roll': record['user_id'],
                'Time': record['time'],
                'Type': record['type']
            })
        return formatted_records
    except:
        return []

# Add Attendance of a specific user
def add_attendance(name, user_type='student'):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")
    datetoday = date.today().strftime("%m_%d_%y")
    
    return db.add_attendance(userid, username, datetoday, current_time, user_type)



################## API ENDPOINTS #######################

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    data = request.get_json()
    password = data.get('password')
    
    if password == os.getenv('ADMIN_PASSWORD', 'admin123'):
        access_token = create_access_token(identity='admin')
        return jsonify({'access_token': access_token, 'role': 'admin'}), 200
    
    return jsonify({'message': 'Invalid admin credentials'}), 401

@app.route('/api/user/login', methods=['POST'])
def user_login():
    """User login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    # Get user from database
    user = db.get_user_by_username(username)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Check password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Create token for user
    access_token = create_access_token(identity=user['user_id'])
    return jsonify({
        'access_token': access_token, 
        'role': 'user',
        'user': {
            'id': user['user_id'],
            'name': user['name'],
            'type': user['type'],
            'class_section': user['class_section']
        }
    }), 200

# Legacy endpoint for backward compatibility (redirects to admin login)
@app.route('/api/login', methods=['POST'])
def legacy_login():
    """Legacy login endpoint - redirects to admin login"""
    return admin_login()

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    stats = db.get_attendance_stats()
    attendance_data = extract_attendance()
    
    # Calculate attendance rate
    total_users = stats['total_users']
    today_attendance = stats['today_attendance']
    attendance_rate = round((today_attendance / total_users * 100) if total_users > 0 else 0, 1)
    
    return jsonify({
        'total_users': stats['total_users'],
        'total_registered': stats['total_users'],  # Legacy support
        'today_attendance': stats['today_attendance'],
        'present_today': stats['today_attendance'],  # For frontend
        'absent_today': max(0, total_users - today_attendance),
        'students_present': stats['students_today'],
        'employees_present': stats['employees_today'],
        'attendance_rate': attendance_rate,
        'attendance_data': attendance_data
    })

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    attendance_data = extract_attendance()
    return jsonify({'attendance': attendance_data})

@app.route('/api/attendance/start', methods=['POST'])
def start_attendance():
    if not os.path.exists('static/face_recognition_model.pkl'):
        return jsonify({'message': 'No trained model found. Please register users first.'}), 400
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({'message': 'Could not access camera'}), 500
        
        recognized_users = []
        frame_count = 0
        max_frames = 30  # Limit to 30 frames for demo
        
        while frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
                
            if extract_faces(frame):
                (x, y, w, h) = extract_faces(frame)[0]
                face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
                identified_person = identify_face(face.reshape(1, -1))
                
                if identified_person is not None:
                    person_name = identified_person[0]
                    if person_name not in recognized_users:
                        if add_attendance(person_name):
                            recognized_users.append(person_name)
            
            frame_count += 1
        
        cap.release()
        return jsonify({
            'message': f'Attendance recorded for {len(recognized_users)} users',
            'recognized_users': recognized_users
        })
        
    except Exception as e:
        return jsonify({'message': f'Error during attendance: {str(e)}'}), 500

@app.route('/api/admin/register', methods=['POST'])
@jwt_required()
def register_user():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    name = data.get('name')
    user_id = data.get('user_id')
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('type', 'student')  # student or employee
    class_section = data.get('class_section', '')
    
    if not name or not user_id or not username or not password:
        return jsonify({'message': 'Name, ID, username, and password are required'}), 400
    
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Add user to database
    if db.add_user(user_id, name, username, password_hash, user_type, class_section):
        # Create face folder
        user_key = f"{name}_{user_id}"
        userimagefolder = f'static/faces/{user_key}'
        if not os.path.isdir(userimagefolder):
            os.makedirs(userimagefolder)
        
        return jsonify({'message': 'User registered successfully', 'user_folder': userimagefolder})
    else:
        return jsonify({'message': 'User already exists or username is taken'}), 400

@app.route('/api/admin/capture-face', methods=['POST'])
@jwt_required()
def capture_face():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        # Try to get JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                'message': 'No JSON data received. Please ensure you are sending valid JSON data with user_id and name.',
                'expected_format': {
                    'user_id': 'string',
                    'name': 'string'
                }
            }), 400
            
        user_id = data.get('user_id')
        name = data.get('name')
        
        if not user_id or not name:
            return jsonify({'message': 'User ID and name are required'}), 400
        
        user_key = f"{name}_{user_id}"
        userimagefolder = f'static/faces/{user_key}'
        
        if not os.path.isdir(userimagefolder):
            return jsonify({'message': 'User not found. Please register first.'}), 404
        
        # For demo purposes, create placeholder images since camera might not be available
        # In production, this would capture real images from camera
        captured_images = 0
        
        try:
            # Try to access camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                # Camera not available, create placeholder files
                for i in range(nimgs):
                    placeholder_path = f'{userimagefolder}/placeholder_{i + 1}.txt'
                    with open(placeholder_path, 'w') as f:
                        f.write(f'Placeholder for face image {i + 1}')
                    captured_images += 1
                
                return jsonify({
                    'message': f'Camera not available. Created {captured_images} placeholder files for demo.',
                    'images_captured': captured_images,
                    'note': 'In production, this would capture real face images.'
                })
            
            # Camera is available, try to capture real images quickly
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce latency
            
            captured_images = 0
            consecutive_good_frames = 0
            max_attempts = 90  # 3 seconds at 30fps
            frame_count = 0
            
            while captured_images < nimgs and frame_count < max_attempts:
                ret, frame = cap.read()
                if not ret:
                    frame_count += 1
                    continue
                
                frame_count += 1
                faces = extract_faces(frame)
                
                if len(faces) > 0:
                    # Get the best quality face
                    best_face = None
                    best_score = 0
                    
                    for (x, y, w, h) in faces:
                        # Score based on size and center position
                        frame_height, frame_width = frame.shape[:2]
                        center_x = x + w // 2
                        center_y = y + h // 2
                        
                        # Distance from center (lower is better)
                        center_dist = abs(center_x - frame_width // 2) + abs(center_y - frame_height // 2)
                        size_score = w * h  # Larger faces are better
                        
                        # Combined score (higher is better)
                        score = size_score - (center_dist * 2)
                        
                        if score > best_score and w > 150 and h > 150:
                            best_score = score
                            best_face = (x, y, w, h)
                    
                    if best_face:
                        consecutive_good_frames += 1
                        
                        # Only capture if we have stable detection
                        if consecutive_good_frames >= 3:  # 3 stable frames
                            (x, y, w, h) = best_face
                            
                            # Add padding around the face
                            padding = 30
                            x_start = max(0, x - padding)
                            y_start = max(0, y - padding)
                            x_end = min(frame.shape[1], x + w + padding)
                            y_end = min(frame.shape[0], y + h + padding)
                            
                            face = frame[y_start:y_end, x_start:x_end]
                            face_resized = cv2.resize(face, (200, 200))
                            
                            image_path = f'{userimagefolder}/{captured_images + 1}.jpg'
                            cv2.imwrite(image_path, face_resized)
                            captured_images += 1
                            consecutive_good_frames = 0  # Reset for next capture
                            
                            # Small delay between captures for variation
                            import time
                            time.sleep(0.2)
                else:
                    consecutive_good_frames = 0
            
            cap.release()
            
            if captured_images == 0:
                return jsonify({
                    'message': 'No faces detected. Please ensure good lighting and position face in front of camera.',
                    'images_captured': 0
                }), 400
            
            # Train the model after capturing
            if train_model():
                return jsonify({
                    'message': f'Successfully captured {captured_images} images and trained model',
                    'images_captured': captured_images
                })
            else:
                return jsonify({
                    'message': f'Captured {captured_images} images but failed to train model',
                    'images_captured': captured_images
                }), 500
                
        except Exception as camera_error:
            # Camera error, create placeholder files for demo
            for i in range(nimgs):
                placeholder_path = f'{userimagefolder}/placeholder_{i + 1}.txt'
                with open(placeholder_path, 'w') as f:
                    f.write(f'Placeholder for face image {i + 1}')
                captured_images += 1
            
            return jsonify({
                'message': f'Camera error: {str(camera_error)}. Created {captured_images} placeholder files for demo.',
                'images_captured': captured_images,
                'note': 'In production, this would capture real face images.'
            })
            
    except ValueError as json_error:
        return jsonify({
            'message': 'Invalid JSON format in request body',
            'error': str(json_error),
            'expected_format': {
                'user_id': 'string',
                'name': 'string'
            }
        }), 400
    except Exception as e:
        return jsonify({'message': f'Error during face capture: {str(e)}'}), 500

@app.route('/api/admin/scan-face', methods=['POST'])
@jwt_required()
def scan_face():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data received'}), 400
        
        image_data = data.get('image')
        user_id = data.get('user_id')
        name = data.get('name')
        
        if not image_data:
            return jsonify({'message': 'No image data received'}), 400
        
        if not user_id or not name:
            return jsonify({'message': 'User ID and name are required'}), 400
        
        # Create user folder
        user_key = f"{name}_{user_id}"
        userimagefolder = f'static/faces/{user_key}'
        if not os.path.isdir(userimagefolder):
            os.makedirs(userimagefolder)
        
        # Decode base64 image
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({'message': 'Invalid image data'}), 400
            
        except Exception as decode_error:
            return jsonify({'message': f'Error decoding image: {str(decode_error)}'}), 400
        
        # Extract faces from the image
        faces = extract_faces(img)
        
        if len(faces) == 0:
            return jsonify({'message': 'No face detected in image. Please ensure your face is clearly visible.'}), 400
        
        # Save the face image
        face_count = len([f for f in os.listdir(userimagefolder) if f.endswith('.jpg')])
        
        # Get the largest face (best quality)
        best_face = max(faces, key=lambda face: face[2] * face[3])
        x, y, w, h = best_face
        
        # Extract and save the face
        face_img = img[y:y+h, x:x+w]
        face_filename = f'{userimagefolder}/face_{face_count + 1}.jpg'
        
        # Resize face to standard size for better recognition
        face_resized = cv2.resize(face_img, (200, 200))
        cv2.imwrite(face_filename, face_resized)
        
        # Train model if we have enough faces (3 images)
        current_face_count = len([f for f in os.listdir(userimagefolder) if f.endswith('.jpg')])
        
        if current_face_count >= 3:
            # We have enough faces, train the model
            if train_model():
                return jsonify({
                    'success': True,
                    'message': f'Face registered successfully! {current_face_count} faces captured.',
                    'faces_captured': current_face_count,
                    'model_trained': True
                })
            else:
                return jsonify({
                    'success': True,
                    'message': f'Face saved but model training failed. {current_face_count} faces captured.',
                    'faces_captured': current_face_count,
                    'model_trained': False
                })
        else:
            # Need more faces
            needed_faces = 3 - current_face_count
            return jsonify({
                'success': True,
                'message': f'Face {current_face_count}/3 captured. Please capture {needed_faces} more face(s).',
                'faces_captured': current_face_count,
                'needed_faces': needed_faces,
                'model_trained': False
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error during face scanning: {str(e)}'
        }), 500

@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    users = db.get_all_users()
    users_list = []
    
    for user in users:
        # Check if user has face images
        user_key = f"{user['name']}_{user['user_id']}"
        user_folder = f'static/faces/{user_key}'
        has_images = os.path.isdir(user_folder) and len(os.listdir(user_folder)) > 0
        
        users_list.append({
            'id': user['user_id'],
            'name': user['name'],
            'username': user['username'],
            'type': user['type'],
            'class_section': user['class_section'],
            'registered_date': user['registered_date'],
            'has_face_data': has_images,
            'has_password': bool(user['password_hash'])
        })
    
    return jsonify({'users': users_list})

@app.route('/api/admin/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    # Get user info first
    user = db.get_user(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Delete user folder
    user_key = f"{user['name']}_{user['user_id']}"
    user_folder = f'static/faces/{user_key}'
    if os.path.isdir(user_folder):
        import shutil
        shutil.rmtree(user_folder)
    
    # Delete from database
    if db.delete_user(user_id):
        # Retrain model if there are still users
        remaining_users = db.get_all_users()
        if len(remaining_users) > 0:
            train_model()
        
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'Failed to delete user'}), 500

@app.route('/api/admin/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    # Get the current user to validate existence
    existing_user = db.get_user(user_id)
    if not existing_user:
        return jsonify({'message': 'User not found'}), 404
    
    # Update user information
    updated_data = {
        'name': data.get('name', existing_user['name']),
        'user_id': data.get('user_id', existing_user['user_id']),
        'username': data.get('username', existing_user['username']),
        'type': data.get('type', existing_user['type']),
        'class_section': data.get('class_section', existing_user.get('class_section', ''))
    }
    
    # If user_id is being changed, we need to update the face folder too
    if updated_data['user_id'] != existing_user['user_id'] or updated_data['name'] != existing_user['name']:
        old_user_key = f"{existing_user['name']}_{existing_user['user_id']}"
        new_user_key = f"{updated_data['name']}_{updated_data['user_id']}"
        
        old_folder = f'static/faces/{old_user_key}'
        new_folder = f'static/faces/{new_user_key}'
        
        # Rename the face folder if it exists
        if os.path.isdir(old_folder):
            try:
                os.rename(old_folder, new_folder)
            except OSError as e:
                return jsonify({'message': f'Error updating face folder: {str(e)}'}), 500
    
    # Update user in database
    if db.update_user(user_id, updated_data):
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'Failed to update user'}), 500

@app.route('/api/admin/users/<user_id>/password', methods=['PUT'])
@jwt_required()
def reset_user_password(user_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    new_password = data.get('password')
    
    if not new_password:
        return jsonify({'message': 'New password is required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters long'}), 400
    
    # Hash the new password
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Update password in database
    if db.update_user_password(user_id, password_hash):
        return jsonify({'message': 'Password reset successfully'})
    else:
        return jsonify({'message': 'Failed to reset password'}), 500

@app.route('/api/admin/check-face-detection', methods=['POST'])
@jwt_required()
def check_face_detection():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({
                'face_detected': False,
                'ready': False,
                'message': 'Camera not accessible. Please check camera permissions.'
            })
        
        # Try to read a frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return jsonify({
                'face_detected': False,
                'ready': False,
                'message': 'Camera not working properly.'
            })
        
        # Check for faces in the frame
        faces = extract_faces(frame)
        
        if len(faces) > 0:
            # Check face quality
            best_face = max(faces, key=lambda face: face[2] * face[3])
            x, y, w, h = best_face
            
            if w > 150 and h > 150:
                return jsonify({
                    'face_detected': True,
                    'ready': True,
                    'message': 'Face detected and ready for capture!'
                })
            else:
                return jsonify({
                    'face_detected': True,
                    'ready': False,
                    'message': 'Face detected but too small. Please move closer to camera.'
                })
        else:
            return jsonify({
                'face_detected': False,
                'ready': False,
                'message': 'No face detected. Please position your face in front of the camera.'
            })
    
    except Exception as e:
        return jsonify({
            'face_detected': False,
            'ready': False,
            'message': f'Camera error: {str(e)}'
        })

@app.route('/api/admin/test-camera', methods=['POST'])
@jwt_required()
def test_camera():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({
                'camera_available': False,
                'message': 'Camera not accessible. Please check camera permissions.'
            })
        
        # Try to read a frame
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            return jsonify({
                'camera_available': True,
                'message': 'Camera is working properly.',
                'frame_size': {'width': frame.shape[1], 'height': frame.shape[0]}
            })
        else:
            return jsonify({
                'camera_available': False,
                'message': 'Camera not working properly.'
            })
    
    except Exception as e:
        return jsonify({
            'camera_available': False,
            'message': f'Camera error: {str(e)}'
        })

@app.route('/api/admin/notices', methods=['GET'])
@jwt_required()
def get_notices():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        notices = db.get_all_notices()
        return jsonify({'notices': notices})
    except Exception as e:
        return jsonify({'message': f'Error loading notices: {str(e)}'}), 500

@app.route('/api/admin/notices', methods=['POST'])
@jwt_required()
def create_notice():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    priority = data.get('priority', 'normal')
    
    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400
    
    try:
        notice_id = db.add_notice(title, content, priority, 'admin')
        if notice_id:
            return jsonify({
                'message': 'Notice created successfully',
                'notice_id': notice_id
            })
        else:
            return jsonify({'message': 'Failed to create notice'}), 500
    except Exception as e:
        return jsonify({'message': f'Error creating notice: {str(e)}'}), 500

@app.route('/api/admin/notices/<notice_id>', methods=['DELETE'])
@jwt_required()
def delete_notice(notice_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        if db.delete_notice(notice_id):
            return jsonify({'message': 'Notice deleted successfully'})
        else:
            return jsonify({'message': 'Notice not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error deleting notice: {str(e)}'}), 500

@app.route('/api/admin/attendance-history', methods=['GET'])
@jwt_required()
def get_attendance_history():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        history = db.get_attendance_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'message': f'Error loading attendance history: {str(e)}'}), 500

@app.route('/api/admin/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        analytics_data = db.get_analytics_data()
        return jsonify(analytics_data)
    except Exception as e:
        return jsonify({'message': f'Error loading analytics: {str(e)}'}), 500

@app.route('/api/admin/recent-activity', methods=['GET'])
@jwt_required()
def get_recent_activity():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        recent_activity = db.get_recent_activity()
        return jsonify({'recent_activity': recent_activity})
    except Exception as e:
        return jsonify({'message': f'Error loading recent activity: {str(e)}'}), 500

@app.route('/api/admin/backup/database', methods=['POST'])
@jwt_required()
def backup_database():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        import shutil
        import time
        
        # Create backup directory if it doesn't exist
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Create timestamp for backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f'backup_{timestamp}.zip'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Create zip file with all important data
        with zipfile.ZipFile(backup_path, 'w') as zipf:
            # Add database file
            if os.path.exists('attendance.db'):
                zipf.write('attendance.db', 'attendance.db')
            
            # Add users.json if exists
            if os.path.exists('users.json'):
                zipf.write('users.json', 'users.json')
            
            # Add face images
            if os.path.exists('static/faces'):
                for root, dirs, files in os.walk('static/faces'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, '.')
                        zipf.write(file_path, arcname)
            
            # Add attendance records
            if os.path.exists('Attendance'):
                for root, dirs, files in os.walk('Attendance'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, '.')
                        zipf.write(file_path, arcname)
            
            # Add notices
            if os.path.exists('notices'):
                for root, dirs, files in os.walk('notices'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, '.')
                        zipf.write(file_path, arcname)
        
        return jsonify({
            'message': 'Database backup created successfully',
            'backup_file': backup_path,
            'timestamp': timestamp
        })
    
    except Exception as e:
        return jsonify({'message': f'Error creating backup: {str(e)}'}), 500

@app.route('/api/admin/export/json', methods=['POST'])
@jwt_required()
def export_to_json():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        # Create exports directory if it doesn't exist
        export_dir = 'exports'
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        # Create timestamp for export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f'export_{timestamp}.json'
        export_path = os.path.join(export_dir, export_filename)
        
        # Gather all data
        export_data = {
            'export_timestamp': timestamp,
            'users': db.get_all_users(),
            'notices': db.get_all_notices(),
            'attendance_history': db.get_attendance_history(),
            'analytics': db.get_analytics_data()
        }
        
        # Write to JSON file
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return jsonify({
            'message': 'Data exported to JSON successfully',
            'export_file': export_path,
            'timestamp': timestamp
        })
    
    except Exception as e:
        return jsonify({'message': f'Error exporting data: {str(e)}'}), 500

@app.route('/api/admin/export/csv', methods=['POST'])
@jwt_required()
def export_to_csv():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        data = request.get_json()
        date_filter = data.get('date') if data else None
        
        # Create exports directory if it doesn't exist
        export_dir = 'exports'
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        # Create timestamp for export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if date_filter:
            export_filename = f'attendance_{date_filter}_{timestamp}.csv'
        else:
            export_filename = f'attendance_all_{timestamp}.csv'
        
        export_path = os.path.join(export_dir, export_filename)
        
        # Get attendance data
        if date_filter:
            attendance_data = db.get_attendance(date_filter)
        else:
            attendance_history = db.get_attendance_history()
            attendance_data = []
            for date, records in attendance_history.items():
                attendance_data.extend(records)
        
        # Create CSV
        import csv
        with open(export_path, 'w', newline='') as csvfile:
            fieldnames = ['name', 'user_id', 'date', 'time', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in attendance_data:
                writer.writerow(record)
        
        return jsonify({
            'message': 'Attendance data exported to CSV successfully',
            'export_file': export_path,
            'timestamp': timestamp,
            'records_count': len(attendance_data)
        })
    
    except Exception as e:
        return jsonify({'message': f'Error exporting CSV: {str(e)}'}), 500

@app.route('/api/admin/download/<filename>', methods=['GET'])
@jwt_required()
def download_file(filename):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        # Check in backups directory
        backup_path = os.path.join('backups', filename)
        if os.path.exists(backup_path):
            return send_file(backup_path, as_attachment=True)
        
        # Check in exports directory
        export_path = os.path.join('exports', filename)
        if os.path.exists(export_path):
            return send_file(export_path, as_attachment=True)
        
        return jsonify({'message': 'File not found'}), 404
    
    except Exception as e:
        return jsonify({'message': f'Error downloading file: {str(e)}'}), 500

@app.route('/api/admin/class-config', methods=['POST'])
@jwt_required()
def save_class_config():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        data = request.get_json()
        # Save class configuration (implement as needed)
        return jsonify({'message': 'Class configuration saved successfully'})
    except Exception as e:
        return jsonify({'message': f'Error saving class config: {str(e)}'}), 500

@app.route('/api/admin/time-settings', methods=['POST'])
@jwt_required()
def save_time_settings():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        data = request.get_json()
        # Save time settings (implement as needed)
        return jsonify({'message': 'Time settings saved successfully'})
    except Exception as e:
        return jsonify({'message': f'Error saving time settings: {str(e)}'}), 500

@app.route('/api/admin/active-classes', methods=['GET'])
@jwt_required()
def get_active_classes():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    try:
        # Return active classes (implement as needed)
        active_classes = []
        return jsonify({'active_classes': active_classes})
    except Exception as e:
        return jsonify({'message': f'Error loading active classes: {str(e)}'}), 500

# User API endpoints
@app.route('/api/user/attendance', methods=['GET'])
@jwt_required()
def get_my_attendance():
    current_user = get_jwt_identity()
    
    try:
        user_attendance = db.get_user_attendance(current_user)
        return jsonify({'attendance': user_attendance})
    except Exception as e:
        return jsonify({'message': f'Error loading attendance: {str(e)}'}), 500

@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_my_profile():
    current_user = get_jwt_identity()
    
    try:
        user = db.get_user(current_user)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Remove sensitive information
        profile = {
            'id': user['user_id'],
            'name': user['name'],
            'username': user['username'],
            'type': user['type'],
            'class_section': user['class_section'],
            'registered_date': user['registered_date']
        }
        
        return jsonify({'profile': profile})
    except Exception as e:
        return jsonify({'message': f'Error loading profile: {str(e)}'}), 500

@app.route('/api/user/notices', methods=['GET'])
@jwt_required()
def get_user_notices():
    current_user = get_jwt_identity()
    
    try:
        notices = db.get_all_notices()
        # Filter notices for users (you can add user-specific filtering here)
        return jsonify({'notices': notices})
    except Exception as e:
        return jsonify({'message': f'Error loading notices: {str(e)}'}), 500

@app.route('/api/user/mark-attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    current_user = get_jwt_identity()
    
    try:
        user = db.get_user(current_user)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Check if already marked attendance today
        today = date.today().strftime("%m_%d_%y")
        existing_attendance = db.get_user_attendance_for_date(current_user, today)
        
        if existing_attendance:
            return jsonify({'message': 'Attendance already marked for today'}), 400
        
        # Mark attendance
        user_key = f"{user['name']}_{user['user_id']}"
        if add_attendance(user_key, user['type']):
            return jsonify({'message': 'Attendance marked successfully'})
        else:
            return jsonify({'message': 'Failed to mark attendance'}), 500
    
    except Exception as e:
        return jsonify({'message': f'Error marking attendance: {str(e)}'}), 500

@app.route('/api/user/mark-attendance-with-image', methods=['POST'])
@jwt_required()
def mark_attendance_with_image():
    current_user = get_jwt_identity()
    
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'message': 'No image data received'}), 400
        
        user = db.get_user(current_user)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Check if model exists
        if not os.path.exists('static/face_recognition_model.pkl'):
            return jsonify({'message': 'Face recognition model not found'}), 400
        
        # Decode and process image
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({'message': 'Invalid image data'}), 400
            
        except Exception as decode_error:
            return jsonify({'message': f'Error decoding image: {str(decode_error)}'}), 400
        
        # Extract faces and identify
        faces = extract_faces(img)
        
        if len(faces) == 0:
            return jsonify({'message': 'No face detected in image'}), 400
        
        # Get the best face
        best_face = max(faces, key=lambda face: face[2] * face[3])
        x, y, w, h = best_face
        
        face_img = img[y:y+h, x:x+w]
        face_resized = cv2.resize(face_img, (50, 50))
        
        # Identify the face
        identified_person = identify_face(face_resized.reshape(1, -1))
        
        if identified_person is None:
            return jsonify({'message': 'Face not recognized'}), 400
        
        # Check if the identified person matches the current user
        expected_user_key = f"{user['name']}_{user['user_id']}"
        identified_user_key = identified_person[0]
        
        if identified_user_key != expected_user_key:
            return jsonify({'message': 'Face does not match user account'}), 400
        
        # Check if already marked attendance today
        today = date.today().strftime("%m_%d_%y")
        existing_attendance = db.get_user_attendance_for_date(current_user, today)
        
        if existing_attendance:
            return jsonify({'message': 'Attendance already marked for today'}), 400
        
        # Mark attendance
        if add_attendance(expected_user_key, user['type']):
            return jsonify({'message': 'Attendance marked successfully with face recognition'})
        else:
            return jsonify({'message': 'Failed to mark attendance'}), 500
    
    except Exception as e:
        return jsonify({'message': f'Error marking attendance: {str(e)}'}), 500

@app.route('/api/user/start-face-scan', methods=['POST'])
@jwt_required()
def start_face_scan():
    current_user = get_jwt_identity()
    
    try:
        # This endpoint can be used to initiate face scanning for attendance
        return jsonify({'message': 'Face scan initiated', 'user_id': current_user})
    except Exception as e:
        return jsonify({'message': f'Error starting face scan: {str(e)}'}), 500

@app.route('/api/user/analytics', methods=['GET'])
@jwt_required()
def get_user_analytics():
    current_user = get_jwt_identity()
    
    try:
        user_analytics = db.get_user_analytics(current_user)
        return jsonify(user_analytics)
    except Exception as e:
        return jsonify({'message': f'Error loading user analytics: {str(e)}'}), 500

@app.route('/api/analytics/attendance-trends', methods=['GET'])
@jwt_required()
def get_attendance_trends():
    try:
        trends = db.get_attendance_trends()
        return jsonify({'trends': trends})
    except Exception as e:
        return jsonify({'message': f'Error loading attendance trends: {str(e)}'}), 500

@app.route('/api/profile/<user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    try:
        user = db.get_user(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Get user's attendance statistics
        user_attendance = db.get_user_attendance(user_id)
        
        profile = {
            'id': user['user_id'],
            'name': user['name'],
            'type': user['type'],
            'class_section': user['class_section'],
            'registered_date': user['registered_date'],
            'attendance_stats': {
                'total_days': len(user_attendance),
                'attendance_rate': 85  # Calculate based on actual data
            }
        }
        
        return jsonify({'profile': profile})
    except Exception as e:
        return jsonify({'message': f'Error loading profile: {str(e)}'}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({'message': 'Unauthorized access'}), 401

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({'message': 'Access forbidden'}), 403

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('backups', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    
    # Initialize database tables (creates tables if they don't exist)
    try:
        db.init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        exit(1)
    
    # Run the app
    print("Starting Face Recognition Attendance System...")
    print("Frontend: http://localhost:3000")
    print("Backend API: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)