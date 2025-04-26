from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Prevents caching of static files

# Database Configuration - Using MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jasonso000@localhost/demo01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student' or 'teacher'
    city = db.Column(db.String(100))
    timezone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    events = db.relationship('Event', backref='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Dictionary to store username and password (only used as fallback if DB fails)
USER_CREDENTIALS = {
    'admin': '123'  # Username: 'admin', Password: '123'
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('123.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # First try database login
    try:
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            session['user_id'] = user.id
            session['role'] = user.role  # Store the user role in session
            return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback to hardcoded credentials
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['username'] = username
            session['role'] = 'student'  # Default role for hardcoded users
            return redirect(url_for('dashboard'))
    
    return render_template('123.html', error='Invalid username or password')

@app.route('/register', methods=['POST'])
def register():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    city = request.form.get('city')
    timezone = request.form.get('timezone')
    role = request.form.get('role', 'student')  # Default to student if not specified
    
    # Validate inputs
    if not username or not password or not email:
        return render_template('123.html', reg_error='All fields are required')
    
    # Check if username already exists
    try:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('123.html', reg_error='Username already exists')
            
        # Create new user with hashed password
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            role=role,
            city=city,
            timezone=timezone
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in
        session['username'] = username
        session['user_id'] = new_user.id
        session['role'] = role
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        print(f"Database error during registration: {e}")
        # Fallback to hardcoded method
        USER_CREDENTIALS[username] = password
        session['username'] = username
        session['role'] = role
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Get user-specific data if available
    user_events = []
    if 'user_id' in session:
        try:
            user_events = Event.query.filter_by(user_id=session['user_id']).all()
        except Exception as e:
            print(f"Error fetching events: {e}")
    
    # Direct to appropriate dashboard based on role
    role = session.get('role', 'student')
    if role == 'teacher':
        return render_template('teacher_dashboard.html', username=session['username'], events=user_events)
    else:
        return render_template('student_dashboard.html', username=session['username'], events=user_events)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/api/teacher-availability/<username>')
def teacher_availability(username):
    # Check if the teacher exists in the database
    teacher = User.query.filter_by(username=username, role='teacher').first()
    
    if not teacher:
        return {'error': 'Teacher not found'}, 404
    
    # Fetch teacher's availability events from the database
    availability_events = Event.query.filter_by(
        user_id=teacher.id, 
        title='Free Time'
    ).all()
    
    # Format the availability data
    availability_data = []
    for event in availability_events:
        availability_data.append({
            'date': event.event_date.strftime('%Y-%m-%d'),
            'time': event.start_time.strftime('%H:%M'),
            'endTime': event.end_time.strftime('%H:%M'),
            'type': 'free-time'
        })
    
    return {'availability': availability_data}

@app.route('/api/save-availability', methods=['POST'])
def save_availability():
    if 'user_id' not in session:
        return {'error': 'Not logged in'}, 401
        
    if session.get('role') != 'teacher':
        return {'error': 'Only teachers can set availability'}, 403
    
    # Get the availability data from the request
    availability_data = request.json.get('availability', [])
    user_id = session['user_id']
    
    try:
        # Clear previous free time slots for this teacher
        Event.query.filter_by(user_id=user_id, title='Free Time').delete()
        
        # Add new availability slots
        for slot in availability_data:
            # Parse date and times
            event_date = datetime.datetime.strptime(slot['date'], '%Y-%m-%d').date()
            start_time = datetime.datetime.strptime(slot['time'], '%H:%M').time()
            end_time = datetime.datetime.strptime(slot['endTime'], '%H:%M').time()
            
            # Create new event
            new_event = Event(
                user_id=user_id,
                title='Free Time',
                description='Available for booking',
                event_date=event_date,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(new_event)
        
        db.session.commit()
        return {'success': True, 'message': 'Availability saved successfully'}
        
    except Exception as e:
        db.session.rollback()
        print(f"Error saving availability: {e}")
        return {'error': f'Failed to save availability: {str(e)}'}, 500

if __name__ == '__main__':
    app.run(debug=True)
