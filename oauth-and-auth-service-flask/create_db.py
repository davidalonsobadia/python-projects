from app import app, db

# Create the database and tables
with app.app_context():
    db.create_all()
    print("Database and tables created.")