from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Length,Email,DataRequired,ValidationError,Optional
from .models import User

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        usr =  User.query.filter_by(username=username_to_check.data).first()
        if usr:
            raise ValidationError('Username is already exists!')
    def validate_email(self,email_to_check):
        usr =  User.query.filter_by(email=email_to_check.data).first()
        if usr:
            raise ValidationError('email Address is already exists!')
    def validate_password2(self,pass_to_check):
        print(self.password1.data,pass_to_check.data)
        if self.password1.data != pass_to_check.data:
            raise ValidationError('password is not match')
       
       
    username = StringField(label="Username",validators=[Length(min=2,max=30),DataRequired()])
    email = StringField(label="Email Address",validators=[Email(),DataRequired()])
    password1 = PasswordField(label="Password",validators=[Length(min=5),DataRequired()])
    password2 = PasswordField(label="Confirm_Password",validators=[DataRequired()])
    submit = SubmitField(label="Signup")

class LoginForm(FlaskForm):
    # def validate_username(self,username_to_check):
    #     usr =  User.query.filter_by(username=username_to_check.data).first()
    #     if usr:
    #         raise ValidationError('Username is already exists!')
    # def validate_email(self,email_to_check):
    #     usr =  User.query.filter_by(email=email_to_check.data).first()
    #     if usr:
    #         raise ValidationError('email Address is already exists!')
    # def validate_password2(self,pass_to_check):
    #     print(self.password1.data,pass_to_check.data)
    #     if self.password1.data != pass_to_check.data:
    #         raise ValidationError('password is not match')
       
       
    username = StringField(label="Username",validators=[DataRequired()])
    password = PasswordField(label="Password",validators=[DataRequired()])
    is_admin = BooleanField(label="is_admin",validators=[Optional])
    submit = SubmitField(label="Signin")
