from app.core.database import SessionLocal
from app.models.user import User
import time

db = SessionLocal()
count = db.query(User).count()
print(f"Users found: {count}")
db.close()
