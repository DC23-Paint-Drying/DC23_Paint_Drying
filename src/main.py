from flask import Flask, render_template, redirect, url_for
from flask_wtf import CSRFProtect

from forms import RegisterForm, OrderSubscriptionForm
from gdrive_manager import GdriveManager
from process_form import process_form
from user_dto import UserDto, Gender

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

csrf = CSRFProtect(app)

gdrive = GdriveManager()


@app.route("/")
def index():
    return render_template("index.html", the_title="Paint Drying")


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        user = UserDto(form.username.data,
                       form.name.data,
                       form.surname.data,
                       form.email.data,
                       Gender(form.gender.data))

        return redirect(url_for('index'))
    return render_template("register.html", form=form, the_title="Register - Paint Drying")


@app.route("/order_subscription", methods=['POST', 'GET'])
def order_subscription():
    form = OrderSubscriptionForm()
    if form.validate_on_submit():
        # example how to get data from wtforms
        process_form(email=form.email.data,
                     subscription_level=form.subscription_level.data)
        return redirect(url_for('index'))
    return render_template("order_subscription.html", form=form, the_title="Order Subscription - Paint Drying")

