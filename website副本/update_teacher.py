from app import app, db, User

def update_teacher():
    with app.app_context():
        # Find teacher with username 123
        teacher = User.query.filter_by(username='123', role='teacher').first()
        
        if not teacher:
            print("Teacher with username 123 not found")
            return
        
        # Print current info
        print("Current teacher information:")
        print(f"ID: {teacher.id}")
        print(f"Username: {teacher.username}")
        print(f"Email: {teacher.email}")
        print(f"Timezone: {teacher.timezone}")
        print(f"City: {teacher.city}")
        
        # Update timezone and city
        teacher.timezone = 'Asia/Seoul'
        teacher.city = 'Seoul'
        
        # Save changes
        db.session.commit()
        
        print("\nTeacher updated successfully:")
        print(f"ID: {teacher.id}")
        print(f"Username: {teacher.username}")
        print(f"Email: {teacher.email}")
        print(f"Timezone: {teacher.timezone}")
        print(f"City: {teacher.city}")

if __name__ == '__main__':
    update_teacher() 