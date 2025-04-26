from app import app, User, db

with app.app_context():
    print('\nAll users in database:')
    users = User.query.all()
    if users:
        for user in users:
            print(f'id:{user.id} username:{user.username} role:{user.role}')
    else:
        print("No users found in the database.") 