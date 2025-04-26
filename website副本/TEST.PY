import pymysql
import sys

# MySQL Connection Info
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'jasonso000',  # User's MySQL password
    'database': 'demo01',  # This is the database we'll create if it doesn't exist
    'port': 3306,
    'charset': 'utf8mb4'
}

def test_connection():
    """Test the connection to MySQL and create the database if it doesn't exist."""
    try:
        # First connect without specifying a database
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port'],
            charset=db_config['charset']
        )
        
        with connection.cursor() as cursor:
            # Check if database exists, create it if it doesn't
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
            print(f"Database '{db_config['database']}' is ready.")
            
            # Use the database
            cursor.execute(f"USE {db_config['database']}")
            
            # Create users table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'student',
                    city VARCHAR(100),
                    timezone VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Users table is ready.")
            
            # Create events table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    event_date DATE NOT NULL,
                    start_time TIME,
                    end_time TIME,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            print("Events table is ready.")
            
        connection.commit()
        print("MySQL connection successful!")
        connection.close()
        return True
        
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    print("Testing MySQL connection...")
    success = test_connection()
    if success:
        print("MySQL setup completed successfully!")
    else:
        print("Failed to set up MySQL. Please check your connection settings.")
        sys.exit(1)
