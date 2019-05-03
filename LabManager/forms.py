from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from LabManager.dbModels import User


class RegistrationForm(FlaskForm):
    # The first StringField argument is the field name,
    # which is also the HTML label.
    username = StringField("Username",
        validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField("Email",
        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
        validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
        validators=[DataRequired(), EqualTo("password")])
    submit_signUp = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken. Please try another one.")
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("This email is already registered. Please choose another one.")


class LoginForm(FlaskForm):
    email = StringField("Email",
        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
        validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit_signIn = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
        validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField("Email",
        validators=[DataRequired(), Email()])
    picture = FileField("Profile Picture",
        validators=[FileAllowed(["jpg", "png"], message="The file you selected had an unsupported extension. Please upload a JPG or PNG file instead.")])
    submit = SubmitField("Update Account")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is taken. Please try another one.")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("This email is already registered. Please choose another one.")
