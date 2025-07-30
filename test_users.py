from app import app
from backend.models import User
from werkzeug.security import check_password_hash

with app.app_context():
    # Check if admin user exists
    admin_user = User.query.filter_by(user_mail='admin@quiz.com').first()
    if admin_user:
        print(f"Admin user found: {admin_user.user_name}")
        print(f"Admin roles: {[role.name for role in admin_user.roles]}")
        
        # Test password verification
        test_password = 'admin'
        if check_password_hash(admin_user.user_pass, test_password):
            print("✅ Admin password verification works!")
        else:
            print("❌ Admin password verification failed!")
            print(f"Stored hash: {admin_user.user_pass}")
    else:
        print("❌ Admin user not found!")
    
    # Check if regular user exists
    user0 = User.query.filter_by(user_mail='user0@quiz.com').first()
    if user0:
        print(f"User found: {user0.user_name}")
        print(f"User roles: {[role.name for role in user0.roles]}")
        
        # Test password verification
        test_password = 'user'
        if check_password_hash(user0.user_pass, test_password):
            print("✅ User password verification works!")
        else:
            print("❌ User password verification failed!")
            print(f"Stored hash: {user0.user_pass}")
    else:
        print("❌ User not found!")
    
    # List all users
    all_users = User.query.all()
    print(f"\nTotal users in database: {len(all_users)}")
    for user in all_users:
        print(f"- {user.user_mail} ({user.user_name}) - Roles: {[role.name for role in user.roles]}") 