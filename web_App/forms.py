from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from web_App.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    token=StringField('Token No.(Only for librarians)')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exist. Choose different one')
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken. Choose different one')


class SelectionForm(FlaskForm):
    category = SelectField('Category',
                        choices=['Genre', 'Author','Rating', 'Publisher','Book Name'  ])
    input_ = StringField('Category')
    #password = PasswordField('Password', validators=[DataRequired()])
    

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Book_regForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    #email = StringField('Email',
    #                    validators=[DataRequired(), Email()])
    book_name = StringField('Book Name',
                           validators=[DataRequired(), Length(min=2, max=40)])
    book_entry_id = IntegerField('Book Id', validators=[DataRequired()])
    duration = IntegerField('Define in number of days', validators=[DataRequired()])
    submit = SubmitField('Submit Request')

class LibLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    token = StringField('Token No.',
                        validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ManageBookForm(FlaskForm):
    name = StringField('Book Name',validators=[DataRequired(), Length(min=2, max=40)])
    writen_by = StringField('Author',validators=[DataRequired()])
    publisher = StringField('Publisher')
    summary = TextAreaField('Summary')
    genre=StringField('Genre of Book')
    availability = IntegerField('Status')
    picture = FileField('Update Picture', validators=[FileAllowed(['jpg','jpeg', 'png'])])
    submit = SubmitField('Update')

    #def validate_username(self, username):
    #    if username.data != current_user.username:
    #        user = User.query.filter_by(username=username.data).first()
    #        if user:
    #            raise ValidationError('That username is taken. Please choose a different one.')

    #def validate_email(self, email):
    #    if email.data != current_user.email:
    #        user = User.query.filter_by(email=email.data).first()
    #        if user:
    #            raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    rating =IntegerField('Rate the Book on Scale of 5',
                        validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    content = TextAreaField('Write Content')
    submit = SubmitField('Post')