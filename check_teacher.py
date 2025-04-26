from app import app, db, User

def check_teacher():
    with app.app_context():
        # Query the teacher
        teacher = User.query.filter_by(username='1234', role='teacher').first()
        
        if not teacher:
            print("Teacher with username 1234 not found")
            return
        
        # Print teacher details
        print(f"Teacher ID: {teacher.id}")
        print(f"Username: {teacher.username}")
        print(f"Email: {teacher.email}")
        print(f"Timezone: {teacher.timezone}")
        print(f"City: {teacher.city}")
        print(f"Created at: {teacher.created_at}")

if __name__ == '__main__':
    check_teacher() 