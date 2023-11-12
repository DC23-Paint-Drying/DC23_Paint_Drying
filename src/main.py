import datetime
import json
import os

from flask_wtf import CSRFProtect
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from . import manifest
from .bundle_info import BundleInfo
from .client_info import ClientInfo
from .database import Database
from .database_context import DatabaseContext
from .forms import LoginForm, RegisterForm, OrderSubscriptionForm, OrderPacketsForm, EditProfileForm, \
    EditSubscriptionForm
from .gdrive_manager import GdriveManager
from .invoice_generator import Invoice
from .mail import send_mail
from .subscription_info import SubscriptionInfo
from .text_generator import get_propose_mail_text, get_invoice_mail_text
from .user_dto import UserDto


app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

login_manager = LoginManager(app)

csrf = CSRFProtect(app)

db = DatabaseContext("db")

gdriveManager = GdriveManager() if "CONFIG_FILE_PATH" in os.environ else None


@login_manager.user_loader
def load_user(user_email):
    client = db.get_client_by_email(user_email)
    if client:
        return client.basic


@app.errorhandler(401)
def unauthorized_access(error):
    return render_template("unauthorized.html", the_title="Unauthorized - Paint Drying"), 401


@app.route("/")
def index():
    return render_template("index.html", the_title="Paint Drying")


@app.route("/user", methods=['GET'])
@login_required
def user():
    client = db.get_client_by_email(current_user.email)
    return render_template("user.html", data=json.loads(client.to_json()), the_title="Paint Drying")


@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return render_template("index.html", the_title="Paint Drying")


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        client = db.get_client_by_email(form.email.data)
        if not client:
            err_msg = "There is no account with the provided email. " \
                      "Please choose a different email to log in if you have an existing account."
            return render_template("login.html", form=form, err_msg=err_msg,
                                   the_title="Login - Paint Drying"), 409
        login_user(client.basic)
        return redirect(url_for('index'))
    return render_template("login.html", form=form, err_msg=None, the_title="Login - Paint Drying")


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        client = db.get_client_by_email(form.email.data)
        if client:
            err_msg = "An account with the provided email already exists. " \
                      "Please choose a different email or log in if you have an existing account."
            return render_template("register.html", form=form, err_msg=err_msg,
                                   the_title="Register - Paint Drying"), 409

        client = ClientInfo(
            UserDto(form.username.data,
                    form.name.data,
                    form.surname.data,
                    form.age.data,
                    form.email.data,
                    form.gender.data,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            SubscriptionInfo(subscription_level='basic',
                             subscription_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            [])

        db.serialize(client)
        login_user(client.basic)
        return redirect(url_for('index'))
    return render_template("register.html", form=form, err_msg=None, the_title="Register - Paint Drying")


@app.route("/subscribe", methods=['POST', 'GET'])
@login_required
def order_subscription():  # unused
    form = OrderSubscriptionForm()
    if form.validate_on_submit():
        subscription = SubscriptionInfo(subscription_level=form.subscription_level.data,
                                        subscription_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        client = db.get_client_by_email(form.email.data)
        client.subscription = subscription
        db.serialize(client)
        return redirect(url_for('index'))
    return render_template("order_subscription.html", form=form, the_title="Order Subscription - Paint Drying")


@app.route("/order-packets", methods=['POST', 'GET'])
@login_required
def order_packets():
    form = OrderPacketsForm()
    if current_user.user_type == manifest.USER_TYPES.ADMIN:
        form.email.choices = [(email, email) for email in db.get_all_emails()]
    descriptions = [(manifest.PACKETS[name]["name"], manifest.PACKETS[name]["description"]) for name in
                    manifest.PACKETS]
    descriptions = dict(descriptions)

    if form.validate_on_submit():
        client = db.get_client_by_email(form.email.data if form.email.data != "current_user" else current_user.email)
        client.bundles.append(
            BundleInfo(email=client.basic.email,
                       name=form.packets.data,
                       date_from=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       date_to=(datetime.datetime.now() + datetime.timedelta(days=manifest.PACKETS[form.packets.data]['duration'])).strftime("%Y-%m-%d %H:%M:%S")))
        db.serialize(client)

        return redirect(url_for('index'))
    return render_template("order_packets.html", form=form, descriptions=descriptions,
                           the_title="Order Packets - Paint Drying")


@app.route("/edit-profile", methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if current_user.user_type == manifest.USER_TYPES.ADMIN:
        form.email.choices = [(email, email) for email in db.get_all_emails()]
    if form.validate_on_submit():
        client = db.get_client_by_email(form.email.data if form.email.data != "current_user" else current_user.email)
        if client:
            client.basic.username = form.username.data
            client.basic.name = form.name.data
            client.basic.surname = form.surname.data
            client.basic.age = form.age.data
            client.basic.gender = form.gender.data
        db.serialize(client)
        return redirect(url_for('index'))
    return render_template("edit_profile.html", form=form, the_title="Edit Profile - Paint Drying")


@app.route("/edit-subscription", methods=['POST', 'GET'])
@login_required
def edit_subscription():
    form = EditSubscriptionForm()
    if current_user.user_type == manifest.USER_TYPES.ADMIN:
        form.email.choices = [(email, email) for email in db.get_all_emails()]
    if form.validate_on_submit():
        client = db.get_client_by_email(form.email.data if form.email.data != "current_user" else current_user.email)
        if client:
            client.subscription = SubscriptionInfo(subscription_level=form.subscription_level.data,
                                                   subscription_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.serialize(client)
        return redirect(url_for('index'))
    return render_template("edit_subscription.html", form=form, the_title="Edit Subscription - Paint Drying")


@app.route("/admin_panel", methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'GET':
        if request.args.get('suggest-services') == 'suggest':
            clients = db.basic_db.get_clients()
            print(clients)
            for client in clients:
                mail_text = get_propose_mail_text(client['id'], Database(db))
                send_mail(client['email'],
                          'Suggestion',
                          mail_text.__str__(),
                          [])
            return render_template("admin_panel.html", the_title="Paint Drying", notification="Mails sent")
        if request.args.get('send-invoice') == 'send':
            clients = db.basic_db.get_clients()
            directory_name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for i in range(0, len(clients)):
                client = db.get_client_by_email(clients[i]['email'])
                file_name = f'invoice_{client.basic.id}'
                invoice = Invoice(client)
                invoice.save_pdf(f"{file_name}.pdf")
                mail_text = get_invoice_mail_text(client.basic.id, invoice, Database(db))
                send_mail(client.basic.email,
                          'Invoice',
                          mail_text.__str__(),
                          [f"{file_name}.pdf"])
                os.remove(f"{file_name}.pdf")

                if gdriveManager is not None:
                    invoice.save_xml(f"{file_name}.xml")
                    gdriveManager.upload_file(filename=f"{file_name}.xml",
                                              directory_name=directory_name)
                    os.remove(f"{file_name}.xml")
            return render_template("admin_panel.html", the_title="Paint Drying", notification="Invoices sent")
        if request.args.get('generate-report') == 'generate':
            return render_template("admin_panel.html", the_title="Paint Drying", notification="Report generated")

    return render_template("admin_panel.html", the_title="Paint Drying/Admin Panel", notification="")


@app.route("/list_gdrive_files", methods=['GET', 'POST'])
def list_gdrive_files():
    data = {}
    gdrive_available = False
    if request.method == 'GET':
        if gdriveManager is not None:
            gdrive_available = True
            headers = gdriveManager.list_files()
            for h in headers:
                files = gdriveManager.list_files(directory_name=h)
                data[h] = files
    return render_template("list_gdrive_files.html",
                           the_title="Paint Drying/Google Drive Files",
                           data=data,
                           gdrive_available=gdrive_available)
