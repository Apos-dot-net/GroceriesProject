from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import event

from shop import db, app
from shop.products import Product, Category


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False, default="profile.jpg")

    def __repr__(self):
        return '<User %r>' % self.username


class StockReplenishment(db.Model):
    __tablename__ = 'replenishments'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User, backref=db.backref('replenishments', lazy=True))

    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product = db.relationship(Product, backref=db.backref('replenishments', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    category = db.relationship(Category, backref=db.backref('replenishments', lazy=True))

    quantity = db.Column(db.Integer, nullable=False)
    replenishment_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<StockReplenishment %r>' % self.id


# Create an event listener for the StockReplenishment model
@event.listens_for(StockReplenishment, 'after_insert')
def update_stock_after_replenishment(mapper, connection, target):
    # Update the product stock quantity
    target.product.stock += target.quantity
    db.session.commit()


with app.app_context():
    db.create_all()
