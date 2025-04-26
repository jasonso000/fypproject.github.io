from app import app, db, User

def update_student():
    with app.app_context():
        # Find student with username 12
        student = User.query.filter_by(username='12', role='student').first()
        
        if not student:
            # If student not found, check if there's a user with ID 12
            student = User.query.filter_by(id=12).first()
            if not student:
                print("Student with username/ID 12 not found")
                return
        
        # Print current info
        print("Current student information:")
        print(f"ID: {student.id}")
        print(f"Username: {student.username}")
        print(f"Email: {student.email}")
        print(f"Timezone: {student.timezone}")
        print(f"City: {student.city}")
        
        # Update timezone and city
        student.timezone = 'Europe/Madrid'
        student.city = 'Barcelona'
        
        # Save changes
        db.session.commit()
        
        print("\nStudent updated successfully:")
        print(f"ID: {student.id}")
        print(f"Username: {student.username}")
        print(f"Email: {student.email}")
        print(f"Timezone: {student.timezone}")
        print(f"City: {student.city}")

if __name__ == '__main__':
    update_student() 