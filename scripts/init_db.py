import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.db.models import Base

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
print("Tables:", list(Base.metadata.tables.keys()))