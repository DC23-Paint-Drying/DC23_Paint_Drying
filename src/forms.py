from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from . import manifest

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Login')


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=64)])
    name = StringField(label='Name', validators=[DataRequired(), Length(min=3, max=64)])
    surname = StringField(label='Surname', validators=[DataRequired(), Length(min=3, max=64)])
    age = IntegerField(label="Age", validators=[DataRequired(), NumberRange(min=1, max=150)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    gender = RadioField(label='Gender', choices=[('female', 'Female'),
                                                 ('male', 'Male'),
                                                 ('other', 'Other')])
    submit = SubmitField(label='Register')


class OrderSubscriptionForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    subscription_level = RadioField(label='Subscription', choices=[(name, manifest.SUBSCRIPTIONS[name]["name"]) for name in manifest.SUBSCRIPTIONS])
    submit = SubmitField(label='Order Subscription')


class EditProfileForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=64)])
    name = StringField(label='Name', validators=[DataRequired(), Length(min=3, max=64)])
    surname = StringField(label='Surname', validators=[DataRequired(), Length(min=3, max=64)])
    age = IntegerField(label="Age", validators=[DataRequired(), NumberRange(min=1, max=150)])
    gender = RadioField(label='Gender', choices=[('female', 'Female'),
                                                 ('male', 'Male'),
                                                 ('other', 'Other')])
    submit = SubmitField(label='Edit Profile')


class EditSubscriptionForm(FlaskForm):
    subscription_level = RadioField(label='Subscription', choices=[(name, manifest.SUBSCRIPTIONS[name]["name"]) for name in manifest.SUBSCRIPTIONS])
    submit = SubmitField(label='Order Subscription')
