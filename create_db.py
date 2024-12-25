from myapi import app, db, UserModel

with app.app_context():
    db.create_all()
    
