import inspect
from dataclasses import asdict

from flask import Flask, render_template, redirect, url_for
from flask_wtf import CSRFProtect

from .forms import LoginForm, RegisterForm, OrderSubscriptionForm, EditProfileForm, EditSubscriptionForm
from .process_form import process_form
from .csvDatabase import CSVDatabase
from .user_dto import UserDto

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

csrf = CSRFProtect(app)

db = CSVDatabase("db.csv", [param for param in inspect.signature(UserDto).parameters])

"""
Note: Currently we consider the most recently registered user as the one "signed in".
This is a temporary solution and will be updated once a sign-in form is implemented.
"""
current_user_email = None


@app.route("/")
def index():
	return render_template("index.html", the_title="Paint Drying")


@app.route("/login", methods=['POST', 'GET'])
def login():
	global current_user_email

	form = LoginForm()
	if form.validate_on_submit():
		users = db.get_clients(lambda client: client["email"] == form.email.data)
		if not users:
			raise Exception('User with given email does not exist')
		user = users[0]
		# user data is ready to further processing

		current_user_email = form.email.data

		return redirect(url_for('index'))
	return render_template("login.html", form=form, the_title="Login - Paint Drying")


@app.route("/register", methods=['POST', 'GET'])
def register():
	global current_user_email

	form = RegisterForm()
	if form.validate_on_submit():
		user = db.get_clients(lambda client: client["email"] == form.email.data)
		if user:
			raise Exception('User with given email already exists')

		user = UserDto(form.username.data,
					   form.name.data,
					   form.surname.data,
					   form.age.data,
					   form.email.data,
					   form.gender.data)
		current_user_email = form.email.data

		db.add_client(asdict(user))

		return redirect(url_for('index'))
	return render_template("register.html", form=form, the_title="Register - Paint Drying")


@app.route("/subscribe", methods=['POST', 'GET'])
def order_subscription():
	form = OrderSubscriptionForm()
	if form.validate_on_submit():
	# example how to get data from wtforms
		process_form(email=form.email.data,
					 subscription_level=form.subscription_level.data)
		return redirect(url_for('index'))
	return render_template("order_subscription.html", form=form, the_title="Order Subscription - Paint Drying")


@app.route("/edit-profile", methods=['POST', 'GET'])
def edit_profile():
	if not current_user_email:
		raise Exception('User needs to be logged in to edit profile')

	form = EditProfileForm()
	if form.validate_on_submit():
		users = db.get_clients(lambda client: client["email"] == current_user_email)
		if users:
			user = users[0]
			user['username'] = form.username.data
			user['name'] = form.name.data
			user['surname'] = form.surname.data
			user['age'] = form.age.data
			user['gender'] = form.gender.data

			db.update_client(user)

		return redirect(url_for('index'))
	return render_template("edit_profile.html", form=form, the_title="Edit Profile - Paint Drying")


@app.route("/edit-subscription", methods=['POST', 'GET'])
def edit_subscription():
	form = EditSubscriptionForm()
	if form.validate_on_submit():
	# place for change user subscription

		return redirect(url_for('index'))
	return render_template("edit_subscription.html", form=form, the_title="Edit Subscription - Paint Drying")
