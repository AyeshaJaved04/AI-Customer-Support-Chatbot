import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from app.db.session import SessionLocal
from app.db.models import User, Purchase, Base
from app.core.security import hash_password
from datetime import datetime, timedelta
import random

db = SessionLocal()

PRODUCTS = [
    ("PRD001", "Wireless Headphones", "Electronics", 129.99),
    ("PRD002", "Smart Watch", "Electronics", 249.99),
    ("PRD003", "Yoga Mat", "Sports", 39.99),
    ("PRD004", "Coffee Maker", "Kitchen", 89.99),
    ("PRD005", "Running Shoes", "Sports", 119.99),
    ("PRD006", "Laptop Stand", "Electronics", 49.99),
    ("PRD007", "Water Bottle", "Sports", 24.99),
]
STATUSES = ["delivered", "shipped", "processing", "cancelled"]

users_created = 0
for i in range(1, 6):
    email = f"testuser{i}@example.com"
    if not db.query(User).filter(User.email == email).first():
        user = User(
            email=email,
            name=f"Test User {i}",
            hashed_password=hash_password("testpass123")
        )
        db.add(user)
        db.flush()
        for _ in range(random.randint(2, 5)):
            pid, pname, cat, price = random.choice(PRODUCTS)
            db.add(Purchase(
                user_id=user.id,
                product_id=pid,
                product_name=pname,
                category=cat,
                price=price,
                status=random.choice(STATUSES),
                purchase_date=datetime.utcnow() - timedelta(days=random.randint(1, 60))
            ))
        users_created += 1

db.commit()
db.close()
print(f"Created {users_created} test users with purchase history")
print("Login: testuser1@example.com / testpass123")