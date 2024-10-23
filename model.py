from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Specify table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)  # Field for the hashed password

    # Method to set the password and hash it
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Product(db.Model):

    __tablename__ = 'product'  # Specify table name

    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f"<Product {self.name}>"

    def update_price(self, new_price):
        """Update the product price if it's valid."""
        if new_price >= 0:
            self.price = new_price
        else:
            raise ValueError("Price cannot be negative.")