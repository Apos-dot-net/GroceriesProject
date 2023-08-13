from flask import redirect, render_template, session, url_for, flash, request
from flask_login import login_required, current_user

from shop import app, db
from shop.checkout import Purchase
from shop.products.models import Product
from shop.products.routes import get_entities_with_products


def merge_dict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/add-cart', methods=["POST"])
def add_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if request.method == "POST" and product_id and quantity:
            dict_items = {product_id: {"name": product.name, "category": int(product.category.id),
                                       'price': int(product.price), 'quantity': int(quantity),
                                       'image': product.image_1, 'stock': int(product.stock),
                                       'brand': product.brand_id}}
            if 'shop_cart' in session:
                if product_id in session['shop_cart']:
                    for key, item in session['shop_cart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['shop_cart'] = merge_dict(session['shop_cart'], dict_items)
            else:
                session['shop_cart'] = dict_items
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/cart')
def get_cart():
    if 'shop_cart' not in session:
        return redirect(request.referrer)
    total_without_tax = 0
    for key, product in session['shop_cart'].items():
        total_without_tax += product['price'] * int(product['quantity'])
    session['total_without_tax'] = total_without_tax
    return render_template('Checkout/cart.html', title="Your Cart",
                           total_without_tax=total_without_tax,
                           brands=get_entities_with_products('brand'),
                           categories=get_entities_with_products('category'))


@app.route('/empty')
@login_required
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)


@app.route('/update-cart/<int:code>', methods=["POST"])
@login_required
def update_cart(code):
    if 'shop_cart' not in session and len(session['shop_cart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['shop_cart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item Updated', 'success')
                    return redirect(url_for('get_cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('get_cart'))


@app.route('/delete-item/<int:item_id>')
@login_required
def delete_item(item_id):
    if 'shop_cart' not in session or len(session['shop_cart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['shop_cart'].items():
            if int(key) == item_id:
                session['shop_cart'].pop(key, None)
                return redirect(url_for('get_cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('get_cart'))


@app.route('/clear-cart')
@login_required
def clear_cart():
    try:
        session.pop('shop_cart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)


@app.route('/checkout', methods=["POST"])
@login_required
def checkout():
    if 'shop_cart' not in session:
        return redirect(request.referrer)
    if request.method == "POST":
        for key, product in session['shop_cart'].items():
            purchase = Purchase(
                user_id=current_user.id,
                product_id=key,
                quantity=product['quantity'],
                category_id=product['category'],
                brand_id=product['brand']
            )
            db.session.add(purchase)

        db.session.commit()
    else:
        flash("An unexpected Error occurred", "error")

    flash("Your order Has been placed", "success")
    clear_cart()
    return redirect("/")


@app.route('/confirm_checkout', methods=['GET', 'POST'])
@login_required
def confirm_checkout():
    total_without_tax = 0  # Calculate the total without tax (you can retrieve this value from your existing logic)

    return render_template('Checkout/confirm_checkout.html', current_user=current_user,
                           total_without_tax=total_without_tax)
