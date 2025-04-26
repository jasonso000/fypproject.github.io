from app import app, db, User

def check_admin_and_teachers():
    with app.app_context():
        # Find admin users
        admin_users = User.query.filter_by(username='admin').all()
        print(f"Admin users found: {len(admin_users)}")
        for user in admin_users:
            print(f"Admin ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Timezone: {user.timezone}")
            print(f"City: {user.city}")
            print(f"Created at: {user.created_at}")
            print()
        
        # Find all teachers
        teachers = User.query.filter_by(role='teacher').all()
        print(f"Teachers found: {len(teachers)}")
        for teacher in teachers:
            print(f"Teacher ID: {teacher.id}")
            print(f"Username: {teacher.username}")
            print(f"Email: {teacher.email}")
            print(f"Role: {teacher.role}")
            print(f"Timezone: {teacher.timezone}")
            print(f"City: {teacher.city}")
            print(f"Created at: {teacher.created_at}")
            print()

if __name__ == '__main__':
    check_admin_and_teachers() 