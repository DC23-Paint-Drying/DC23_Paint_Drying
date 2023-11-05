import datetime

from flask import Flask, render_template, redirect, url_for
from flask_wtf import CSRFProtect

from .client_info import ClientInfo
from .database_context import DatabaseContext
from .forms import LoginForm, RegisterForm, OrderSubscriptionForm, EditProfileForm, EditSubscriptionForm
from .process_form import process_form
from .subscription_info import SubscriptionInfo
from .user_dto import UserDto

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

csrf = CSRFProtect(app)

db = DatabaseContext("db")

"""
Note: Currently we consider the most recently registered user as the one "signed in".
This is a temporary solution and will be updated once a sign-in form is implemented.
"""
current_user_email = None


@app.route("/")
def index():
    return render_template("index.html", the_title="Paint Drying")


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    global current_user_email
    current_user_email = None

    return render_template("index.html", the_title="Paint Drying")


@app.route("/login", methods=['POST', 'GET'])
def login():
    global current_user_email

    form = LoginForm()
    if form.validate_on_submit():
        users = db.get_clients(lambda client: client["email"] == form.email.data)
        if not users:
            err_msg = "Invalid Email address. Please check it and try again."
            return render_template("login.html", form=form, err_msg=err_msg, the_title="Login - Paint Drying"), 401
        user = users[0]
        # user data is ready to further processing

        current_user_email = form.email.data

        return redirect(url_for('index'))
    return render_template("login.html", form=form, err_msg=None, the_title="Login - Paint Drying")


@app.route("/register", methods=['POST', 'GET'])
def register():
    global current_user_email

    form = RegisterForm()
    if form.validate_on_submit():
        user = db.get_client_by_email(form.email.data)
        if user:
            err_msg = "An account with the provided email already exists. " \
                      "Please choose a different email or log in if you have an existing account."
            return render_template("register.html", form=form, err_msg=err_msg, the_title="Register - Paint Drying"), 409

        user = ClientInfo(UserDto(form.username.data,
                                  form.name.data,
                                  form.surname.data,
                                  form.age.data,
                                  form.email.data,
                                  form.gender.data,
                                  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                          SubscriptionInfo(subscription_level='basic',
                                           subscription_timestamp=datetime.datetime.now().strftime(
                                               "%Y-%m-%d %H:%M:%S")),
                          [])
        current_user_email = form.email.data
        db.serialize(user)

        return redirect(url_for('index'))
    return render_template("register.html", form=form, err_msg=None, the_title="Register - Paint Drying")


@app.route("/subscribe", methods=['POST', 'GET'])
def order_subscription():
    form = OrderSubscriptionForm()
    if not current_user_email:
        return render_template("unauthorized.html", the_title="Unauthorized - Paint Drying"), 401

    if form.validate_on_submit():
        subscription = SubscriptionInfo(subscription_level=form.subscription_level.data,
                                        subscription_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user = db.get_client_by_email(form.email.data)
        user.subscription = subscription
        db.serialize(user)
        return redirect(url_for('index'))
    return render_template("order_subscription.html", form=form, the_title="Order Subscription - Paint Drying")


@app.route("/edit-profile", methods=['POST', 'GET'])
def edit_profile():
    form = EditProfileForm()
    if not current_user_email:
        return render_template("unauthorized.html", the_title="Unauthorized - Paint Drying"), 401

    if form.validate_on_submit():
        user = db.get_client_by_email(current_user_email)
        if user:
            user.basic.username = form.username.data
            user.basic.name = form.name.data
            user.basic.surname = form.surname.data
            user.basic.age = form.age.data
            user.basic.gender = form.gender.data
        db.serialize(user)
        return redirect(url_for('index'))
    return render_template("edit_profile.html", form=form, the_title="Edit Profile - Paint Drying")


@app.route("/edit-subscription", methods=['POST', 'GET'])
def edit_subscription():
    global current_user_email

    form = EditSubscriptionForm()
    if not current_user_email:
        return render_template("unauthorized.html", the_title="Unauthorized - Paint Drying"), 401

    if form.validate_on_submit():
        user = db.get_client_by_email(current_user_email)
        if user:
            user.subscription = SubscriptionInfo(subscription_level=form.subscription_level.data,
                                                 subscription_timestamp=datetime.datetime.now().strftime(
                                                     "%Y-%m-%d %H:%M:%S"))
        db.serialize(user)
        return redirect(url_for('index'))
    return render_template("edit_subscription.html", form=form, the_title="Edit Subscription - Paint Drying")
