from datetime import datetime

from sqlalchemy import event
from sqlalchemy.dialects.mysql import INTEGER

from shop import db, app
from shop.customers import RegisterModel
from shop.products import Product


class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(INTEGER(unsigned=True), primary_key=True)

    user_id = db.Column(INTEGER(unsigned=True), db.ForeignKey(RegisterModel.id, ondelete="CASCADE"), nullable=False)
    user = db.relationship(RegisterModel, backref=db.backref('purchases', lazy=True))

    product_id = db.Column(INTEGER(unsigned=True), db.ForeignKey(Product.id, ondelete="CASCADE"), nullable=False)
    product = db.relationship(Product, backref=db.backref('purchases', lazy=True))

    quantity = db.Column(INTEGER(unsigned=True), nullable=False, default=1)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    category_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    category = db.relationship('Category', backref=db.backref('purchases', lazy=True))

    brand_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('brand.id', ondelete="CASCADE"), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('purchases', lazy=True))

    def __repr__(self):
        return '<Purchase %r>' % self.id


@event.listens_for(Purchase, 'before_insert')
def update_stock_after_purchase(mapper, connection, target):
    # Check if the purchased quantity exceeds the available stock
    avail_stock = int(db.session.query(Product).filter_by(id=target.product_id).first().stock)
    if int(target.quantity) > avail_stock:
        raise ValueError("Not enough stock available for purchase.")
    elif int(target.quantity) < 0:
        raise ValueError("Value cannot be negative")

    # Subtract the purchased quantity from the stock
    db.session.query(Product).filter_by(id=target.product_id).update({'stock': avail_stock - int(target.quantity)})


with app.app_context():
    db.create_all()
