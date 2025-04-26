from app import db, User, app
from werkzeug.security import generate_password_hash

# Create all tables
with app.app_context():
    # Make sure all tables exist
    db.create_all()
    print("Database tables created!")
    
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # Create admin user
        admin = User(
            username='admin',
            password=generate_password_hash('123'), # Password: 123
            email='admin@example.com',
            role='teacher'  # Set admin as a teacher
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists!")
    
    print("Database setup complete!") 