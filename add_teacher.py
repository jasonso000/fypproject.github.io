from app import app, db, User
from werkzeug.security import generate_password_hash

def add_teacher():
    with app.app_context():
        # Check if teacher already exists
        existing_teacher = User.query.filter_by(username='1234', role='teacher').first()
        
        if existing_teacher:
            print('Teacher with username 1234 already exists')
            return
        
        # Create new teacher
        teacher = User(
            username='1234',
            password=generate_password_hash('1234'),
            email='teacher1234@example.com',
            role='teacher'
        )
        
        # Add to database
        db.session.add(teacher)
        db.session.commit()
        print('Teacher with username 1234 added successfully')

if __name__ == '__main__':
    add_teacher() 