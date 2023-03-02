from flask import render_template,redirect,url_for,flash,request
from . import app
from .forms import RegisterForm,LoginForm
from .models import User
from . import db
from flask_login import login_user,logout_user,login_required

@app.route('/',methods=["GET","POST"])
def home():
    return render_template('home.html')

@app.route('/admin/register/',methods=["GET","POST"])
def admin_register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password1.data,
                    is_admin=True
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin_login'))
    if form.errors != {}:
        for err in form.errors.values():
            return render_template('admin_signUp.html',form=form,error=err)
    return render_template('admin_signUp.html',form=form)



@app.route('/admin/',methods=["GET","POST"])
def admin_login():
    form = LoginForm()
    if form.is_submitted():
        usr = User.query.filter_by(username=form.username.data).first()
        if usr and usr.verify_password(entered_password = form.password.data) and usr.is_admin == True:
            login_user(user=usr)
            flash(f'You are sucessfully loggined as {form.username.data}')
            return redirect(url_for('admin_profile',name=form.username.data))
        flash('wrong username or password')
    return render_template('admin_login.html',form=form)



@app.route('/admin_profile/',methods=["GET","POST"])
@login_required
def admin_profile():
    users = User.query.filter_by(is_admin=False)
    if request.args.get('name'):
        name=request.args.get('name')
        return render_template('adminprofile.html',name=name,datas=users)
    return render_template('adminprofile.html',datas=users)

from .extra import *
from .auth import *