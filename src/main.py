from flask import Flask, render_template, redirect, url_for
from forms import RegisterForm, OrderSubscriptionForm
from flask_wtf import CSRFProtect

from user_dto import UserDto, Gender
from forms import RegisterForm, OrderSubscriptionForm
from process_form import process_form

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

csrf = CSRFProtect(app)


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

