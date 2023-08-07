from datetime import datetime

from shop import db, app


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id', ondelete="CASCADE"), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="CASCADE"), nullable=False)
    category = db.relationship('Category', backref=db.backref('category', lazy=True))

    image_1 = db.Column(db.String(256), nullable=False, default='image1.jpg')

    def __repr__(self):
        return '<Product %r>' % self.name


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)


with app.app_context():
    db.create_all()
