from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=64)])
    name = StringField(label='Name', validators=[DataRequired(), Length(min=3, max=64)])
    surname = StringField(label='Surname', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    gender = RadioField(label='Gender', choices=[('female', 'Female'),
                                                 ('male', 'Male'),
                                                 ('other', 'Other')])
    submit = SubmitField(label='Register')


class OrderSubscriptionForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    subscription_level = RadioField(label='Subscription', choices=[('bronze', 'Bronze'),
                                                             ('silver', 'Silver'),
                                                             ('gold', 'Gold')])
    submit = SubmitField(label='Order Subscription')
