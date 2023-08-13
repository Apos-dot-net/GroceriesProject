from flask import render_template, redirect, url_for, abort
from flask_login import (
    login_required, current_user
)

from shop import app, db
from shop.admin import ReplenishStockForm, User, StockReplenishment
from shop.products.models import Product, Brand, Category


@app.route("/admin")
@login_required
def admin():
    products = Product.query.all()
    return render_template("admin/index.html", title="Admin Page", products=products)


@app.route('/brands')
@login_required
def brands():
    brand_names = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title="Brands Page", brands=brand_names)


@app.route('/categories')
@login_required
def categories():
    category_types = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/categories.html', title="Categories Page", categories=category_types)


@app.route('/replenish_stock', methods=['GET', 'POST'])
@login_required
def replenish_stock():
    form = ReplenishStockForm()

    form.product.choices = [(product.id, product.name) for product in Product.query.all()]
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        # Get the selected product ID and quantity from the form
        product_id = form.product.data
        quantity = form.quantity.data
        category_id = form.category.data

        # Check if the current user is from the User model (not RegisterModel)
        if not isinstance(current_user, User):
            abort(403)

        # Create a new StockReplenishment entry
        replenishment = StockReplenishment(user_id=current_user.id, product_id=product_id, quantity=quantity,
                                           category_id=category_id)
        db.session.add(replenishment)

        # Update the product stock quantity
        product = Product.query.get(product_id)
        product.stock += quantity

        db.session.commit()

        return redirect(url_for('replenish_stock'))

    return render_template('admin/replenish_stock.html', form=form)
