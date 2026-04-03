from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.record import FinancialRecord
from app.core.auth import get_password_hash
from datetime import datetime

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data
db.query(FinancialRecord).delete()
db.query(User).delete()
db.commit()

# Create users
users = [
    User(full_name="Admin User", email="admin@zorvyn.com", hashed_password=get_password_hash("admin123"), role="admin", is_active=True),
    User(full_name="Analyst User", email="analyst@zorvyn.com", hashed_password=get_password_hash("analyst123"), role="analyst", is_active=True),
    User(full_name="Viewer User", email="viewer@zorvyn.com", hashed_password=get_password_hash("viewer123"), role="viewer", is_active=True),
]

for user in users:
    db.add(user)
db.commit()

admin = db.query(User).filter(User.email == "admin@zorvyn.com").first()

# Create financial records
records = [
    FinancialRecord(amount=50000, type="income", category="salary", date=datetime(2026, 4, 1), notes="Monthly salary", created_by=admin.id),
    FinancialRecord(amount=25000, type="income", category="freelance", date=datetime(2026, 3, 15), notes="Freelance project payment", created_by=admin.id),
    FinancialRecord(amount=10000, type="income", category="freelance", date=datetime(2026, 2, 20), notes="Web development project", created_by=admin.id),
    FinancialRecord(amount=45000, type="income", category="salary", date=datetime(2026, 3, 1), notes="Monthly salary", created_by=admin.id),
    FinancialRecord(amount=15000, type="expense", category="rent", date=datetime(2026, 4, 1), notes="Monthly rent", created_by=admin.id),
    FinancialRecord(amount=5000, type="expense", category="utilities", date=datetime(2026, 3, 10), notes="Electricity and internet", created_by=admin.id),
    FinancialRecord(amount=8000, type="expense", category="food", date=datetime(2026, 3, 20), notes="Monthly groceries", created_by=admin.id),
    FinancialRecord(amount=3000, type="expense", category="transport", date=datetime(2026, 2, 15), notes="Fuel and cab expenses", created_by=admin.id),
    FinancialRecord(amount=12000, type="expense", category="rent", date=datetime(2026, 2, 1), notes="Monthly rent", created_by=admin.id),
    FinancialRecord(amount=2000, type="expense", category="entertainment", date=datetime(2026, 3, 25), notes="Movies and dining out", created_by=admin.id),
]

for record in records:
    db.add(record)
db.commit()

db.close()

print("Seed data created successfully.")
print("Admin:    admin@zorvyn.com    / admin123")
print("Analyst:  analyst@zorvyn.com  / analyst123")
print("Viewer:   viewer@zorvyn.com   / viewer123")