import os
import secrets

from flask import redirect, url_for, request, flash, render_template, current_app
from flask_login import login_required

from shop import db, app, photos
from .forms import AddProducts
from .models import Brand, Category, Product


def get_entities_with_products(entity_type):
    if entity_type == 'brand':
        entities = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    elif entity_type == 'category':
        entities = Category.query.join(Product, (Category.id == Product.category_id)).all()
    else:
        raise ValueError("Invalid entity_type. It should be 'brand' or 'category'.")

    return entities


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.stock > 0).paginate(page=page, per_page=16)
    return render_template('products/index.html', title="Store Home", products=products,
                           brands=get_entities_with_products('brand'),
                           categories=get_entities_with_products('category'))
@app.route('/welcome_page')
def welcome():
    return render_template('welcome.html', title="Store Home", products="hello",
                           brands=get_entities_with_products('brand'),
                           categories=get_entities_with_products('category'))

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/product_details.html', product=product, title=product.name, brands=brands,
                           categories=get_entities_with_products('category'))


@app.route('/entity/<string:entity>/<int:entity_id>')
def get_entity(entity, entity_id):
    page = request.args.get('page', 1, type=int)

    if entity == 'brand':
        get_entity_obj = Brand.query.filter_by(id=entity_id).first_or_404()
        entity_name = Brand.query.get(entity_id).name
        entity_products = Product.query.filter_by(brand=get_entity_obj).paginate(page=page, per_page=16)
        entity_var = 'brand'
    elif entity == 'category':
        get_entity_obj = Category.query.filter_by(id=entity_id).first_or_404()
        entity_name = Category.query.get(entity_id).name
        entity_products = Product.query.filter_by(category=get_entity_obj).paginate(page=page, per_page=16)
        entity_var = 'category'
    elif entity == 'search':
        search_word = str(request.args.get('search_query'))
        page = request.args.get('page', 1, type=int)
        products = Product.query.filter(
            db.and_(Product.stock > 0, Product.name.like("%{}%".format(search_word)))).paginate(page=page, per_page=16)
        return render_template('products/index.html', title="Store Home", products=products,
                               brands=get_entities_with_products('brand'),
                               categories=get_entities_with_products('category'))
    else:
        flash('Invalid entity', 'warning')
        return redirect(url_for('admin'))

    return render_template('products/index.html', **{
        entity_var: entity_products,
        'title': entity_name,
        'brands': get_entities_with_products('brand'),
        'categories': get_entities_with_products('category'),
        'get_brand': get_entity_obj if entity == 'brand' else None,
        'get_cat': get_entity_obj if entity == 'category' else None,
    })


@app.route('/add/<string:entity>', methods=["GET", "POST"])
@login_required
def add_entity(entity):
    if request.method == "POST":
        entity_name = request.form.get('name')
        if entity == 'brand':
            entity_obj = Brand(name=entity_name)
        elif entity == 'category':
            entity_obj = Category(name=entity_name)
        else:
            flash('Invalid entity', 'warning')
            return redirect(url_for('add_entity', entity=entity))

        db.session.add(entity_obj)
        db.session.commit()

        flash(f'The {entity.capitalize()} {entity_name} was added to the database.', 'success')
        return redirect(url_for('add_entity', entity=entity))

    return render_template('products/add_brand.html', title=f'Add {entity.capitalize()}', entity=entity)


@app.route('/add/product', methods=["GET", "POST"])
@login_required
def add_product():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        desc = form.desc.data
        brand_id = request.form.get('brand')
        category_id = request.form.get('category')
        image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + '.')

        product = Product(name=name, price=price, stock=stock, desc=desc, brand_id=brand_id,
                          category_id=category_id, image_1=image_1)
        db.session.add(product)
        db.session.commit()

        flash(f"{name} has been added to database.", 'success')
        return redirect(url_for('admin'))

    return render_template('products/add_product.html', title='Add Product', form=form, brands=brands,
                           categories=categories)


@app.route('/update/<string:entity>/<int:entity_id>', methods=["GET", "POST"])
@login_required
def update_entity(entity, entity_id):
    if entity == 'brand':
        entity_query = Brand.query.get_or_404(entity_id)
    elif entity == 'category':
        entity_query = Category.query.get_or_404(entity_id)
    else:
        flash('Invalid entity', 'warning')
        return redirect(url_for('admin'))

    if request.method == "POST":
        entity_name = request.form.get('newVal')
        entity_query.name = entity_name
        db.session.commit()
        flash(f'Your {entity} has been updated', 'success')
    if entity == 'brand':
        brand_types = Brand.query.order_by(Brand.id.desc()).all()
        return render_template('admin/categories.html', title="Categories Page", categories=brand_types)
    elif entity == 'category':
        category_types = Category.query.order_by(Category.id.desc()).all()
        return render_template('admin/categories.html', title="Categories Page", categories=category_types)
    else:
        flash('Invalid entity', 'warning')
        return redirect(url_for('admin'))


@app.route('/update/product/<int:product_id>', methods=["GET", "POST"])
@login_required
def update_product(product_id):
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')

    product = Product.query.get_or_404(product_id)
    form = AddProducts(request.form)

    if request.method == "POST":

        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.desc = form.desc.data
        product.brand_id = brand
        product.category_id = category

        if request.files.get('image_1'):
            img_path = os.path.join(current_app.root_path, 'static/images/' + product.image_1)
            if os.path.exists(img_path):
                os.unlink(img_path)
            product.image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Product Updated', 'success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.stock.data = product.stock
    form.desc.data = product.desc

    return render_template('products/update_product.html', title="Update Product", form=form, brands=brands,
                           categories=categories, product=product)


@app.route('/delete/<string:entity>/<int:entity_id>', methods=["POST"])
@login_required
def delete_entity(entity, entity_id):
    if entity == 'brand':
        entity_obj = Brand.query.get_or_404(entity_id)
    elif entity == 'category':
        entity_obj = Category.query.get_or_404(entity_id)
    elif entity == 'product':
        entity_obj = Product.query.get_or_404(entity_id)
    else:
        flash('Invalid entity', 'warning')
        return redirect(url_for('admin'))

    if request.method == "POST":
        if entity == 'product' and request.files.get('image_1'):
            img_path = os.path.join(current_app.root_path, 'static/images/' + entity_obj.image_1)
            if os.path.exists(img_path):
                os.unlink(img_path)

        db.session.delete(entity_obj)
        db.session.commit()
        flash(f'{entity.capitalize()}: {entity_obj.name} Deleted', 'success')
        return redirect(url_for('admin'))

    flash(f'Cant delete {entity.capitalize()}: {entity_obj.name}', 'warning')
    return redirect(url_for('admin'))
