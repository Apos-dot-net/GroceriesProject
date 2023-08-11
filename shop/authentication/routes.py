from flask import redirect, url_for, request, flash, render_template, session
from flask_login import logout_user, login_user, current_user

from shop import bcrypt
from shop import db, app
from ..admin.forms import RegistrationForm, LoginForm
from ..admin.models import User
from ..customers.forms import CustomerRegistrationForm, CustomerLoginForm
from ..customers.models import RegisterModel


@app.route('/register/<string:user_type>', methods=["POST", "GET"])
def register(user_type):
    session["user_type"] = user_type
    if user_type == 'customer':
        form = CustomerRegistrationForm()
    elif user_type == 'admin':
        form = RegistrationForm(request.form)
    else:
        return "Invalid user type"

    print(form.data, form.validate_on_submit())

    if request.method == "POST" and form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        if user_type == 'customer':
            register_user = RegisterModel(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=hash_password,
                country=form.country.data,
                state=form.state.data,
                city=form.city.data,
                address=form.address.data,
                contact=form.contact.data
            )
            db.session.add(register_user)
        elif user_type == 'admin':
            user = User(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=hash_password
            )
            print(user)
            db.session.add(user)

        db.session.commit()
        flash(f"Welcome {form.name.data}, Thank You for registering", "success")
        return redirect(url_for("login", user_type=user_type))

    template = "customers/register.html" if user_type == 'customer' else "admin/register.html"
    title = "Register" if user_type == 'customer' else "Admin Registration"
    return render_template(template, form=form, title=title)


@app.route('/login/<string:user_type>', methods=['GET', 'POST'])
def login(user_type):
    session["user_type"] = user_type
    if user_type == 'customer':
        form = CustomerLoginForm()
        login_template = 'customers/login.html'
        success_redirect = 'home'
    elif user_type == 'admin':
        form = LoginForm(request.form)
        login_template = 'admin/login.html'
        success_redirect = 'admin'
    else:
        return "Invalid user type"

    print(form.data, form.validate_on_submit())
    if form.validate_on_submit():
        user = None
        if user_type == 'customer':
            user = RegisterModel.query.filter_by(email=form.email.data).first()
        elif user_type == 'admin':
            user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Successfully Logged in", 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for(success_redirect))
        flash("Incorrect email or password", 'error')
        return redirect(url_for('login', user_type=user_type))

    if not current_user.is_authenticated:
        return render_template(login_template, form=form, title="Log In")

    return redirect(url_for('login', user_type=user_type))


@app.route('/logout/<string:user_type>')
def logout(user_type):
    print("Logged out")
    logout_user()
    if user_type == 'customer' or user_type == 'admin':
        return redirect(url_for('login', user_type=user_type))
    else:
        return "Invalid user type"


@app.route('/choose_user_type', methods=['GET'])
def choose_user_type():
    return render_template('choose_user_type.html')
