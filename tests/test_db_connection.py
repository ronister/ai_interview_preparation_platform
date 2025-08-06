import os
import django
import sys

# Add the parent directory to Python path to import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

from django.contrib.auth.models import User

def test_db_connection():
    try:
        # Try to get all users
        users = User.objects.all()
        
        print("Database connection successful!")
        print("\nList of users in the database:")
        print("-" * 50)
        
        if users.exists():
            for user in users:
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
                print(f"Date joined: {user.date_joined}")
                print("-" * 50)
        else:
            print("No users found in the database.")
            
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")

if __name__ == "__main__":
    test_db_connection()
