from datetime import datetime

from sqlalchemy.dialects.mysql import INTEGER, FLOAT

from shop import db, app


class Product(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(FLOAT(unsigned=True), nullable=False)
    stock = db.Column(INTEGER(unsigned=True), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    brand_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('brand.id', ondelete="CASCADE"), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))
    category_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    category = db.relationship('Category', backref=db.backref('category', lazy=True))

    image_1 = db.Column(db.String(256), nullable=False, default='image1.jpg')

    def __repr__(self):
        return '<Product %r>' % self.name


class Brand(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    branded_products = db.relationship(Product, back_populates="brand", cascade="all, delete, delete-orphan")
    branded_purchases = db.relationship('Purchase', back_populates="brand", cascade="all, delete, delete-orphan")


class Category(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    categorical_products = db.relationship(Product, back_populates="category", cascade="all, delete, delete-orphan")
    categorical_purchases = db.relationship('Purchase', back_populates="category", cascade="all, delete, delete-orphan")


with app.app_context():
    db.create_all()
