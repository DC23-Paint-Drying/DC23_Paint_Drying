import datetime

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect

from .client_info import ClientInfo
from .database_context import DatabaseContext
from .forms import LoginForm, RegisterForm, OrderSubscriptionForm, EditProfileForm, EditSubscriptionForm
from .process_form import process_form
from .subscription_info import SubscriptionInfo
from .user_dto import UserDto

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

login_manager = LoginManager(app)

csrf = CSRFProtect(app)

db = DatabaseContext("db")


@login_manager.user_loader
def load_user(user_email):
    user = db.get_client_by_email(user_email)
    if user:
        return user.basic


@app.errorhandler(401)
def unauthorized_access(error):
    return render_template("unauthorized.html", the_title="Unauthorized - Paint Drying"), 401


@app.route("/")
def index():
    return render_template("index.html", the_title="Paint Drying")


@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return render_template("index.html", the_title="Paint Drying")


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_client_by_email(form.email.data)
        if not user:
            err_msg = "There is no account with the provided email. " \
                      "Please choose a different email to log in if you have an existing account."
            return render_template("login.html", form=form, err_msg=err_msg,
                                   the_title="Login - Paint Drying"), 409
        login_user(user.basic)
        return redirect(url_for('index'))
    return render_template("login.html", form=form, err_msg=None, the_title="Login - Paint Drying")


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.get_client_by_email(form.email.data)
        if user:
            err_msg = "An account with the provided email already exists. " \
                      "Please choose a different email or log in if you have an existing account."
            return render_template("register.html", form=form, err_msg=err_msg,
                                   the_title="Register - Paint Drying"), 409

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
        db.serialize(user)
        login_user(user.basic)
        return redirect(url_for('index'))
    return render_template("register.html", form=form, err_msg=None, the_title="Register - Paint Drying")


@app.route("/subscribe", methods=['POST', 'GET'])
@login_required
def order_subscription():
    form = OrderSubscriptionForm()
    if form.validate_on_submit():
        subscription = SubscriptionInfo(subscription_level=form.subscription_level.data,
                                        subscription_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user = db.get_client_by_email(form.email.data)
        user.subscription = subscription
        db.serialize(user)
        return redirect(url_for('index'))
    return render_template("order_subscription.html", form=form, the_title="Order Subscription - Paint Drying")


@app.route("/edit-profile", methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = db.get_client_by_email(current_user.email)
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
@login_required
def edit_subscription():
    form = EditSubscriptionForm()
    if form.validate_on_submit():
        user = db.get_client_by_email(current_user.email)
        if user:
            user.subscription = SubscriptionInfo(subscription_level=form.subscription_level.data,
                                                 subscription_timestamp=datetime.datetime.now().strftime(
                                                     "%Y-%m-%d %H:%M:%S"))
        db.serialize(user)
        return redirect(url_for('index'))
    return render_template("edit_subscription.html", form=form, the_title="Edit Subscription - Paint Drying")
