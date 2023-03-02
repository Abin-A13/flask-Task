from flask import render_template,redirect,url_for,flash,request
import requests
import json
from . import app
from .forms import RegisterForm,LoginForm
from .models import User
from . import db
from flask_login import login_user,logout_user,login_required,current_user
from . import app
from .utils import generate_token


@app.route('/signup/',methods=["GET","POST"])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password1.data
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    if form.errors != {}:
        for err in form.errors.values():
            return render_template('signup.html',form=form,error=err)
    return render_template('signup.html',form=form)

@app.route('/login/',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.is_submitted():
        usr = User.query.filter_by(username=form.username.data).first()
        if usr and usr.verify_password(entered_password = form.password.data):
            login_user(user=usr)
            flash(f'You are sucessfully loggined as {form.username.data}')
            return redirect(url_for('profile'))
        flash("wrong username or password")
    return render_template('login.html',form=form)

@app.route('/profile/',methods=["GET","POST"])
@login_required
def profile():
    headers = {'authorization': 'Bearer ' + generate_token(),
            'content-type': 'application/json'}
    res =requests.get(f'https://api.zoom.us/v2/users/me/meetings',headers=headers)
    data=res.json()
    return render_template('profile.html',data=data['meetings'])

@login_required
@app.route('/logout',methods=["GET","POST"])
def logout_page():
    logout_user()
    return redirect(url_for('home'))


@app.route('/user_add/',methods=["GET","POST"])
def user_add():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password1.data
                    )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin_profile'))
    if form.errors != {}:
        for err in form.errors.values():
            return render_template('adduser.html',form=form,error=err)
    return render_template('adduser.html',form=form)



@app.route('/user/delete',methods=["GET","POST"])
def user_delete():
    id=request.args.get('id')
    users = User.query.get(int(id))
    if users:
        db.session.delete(users)
        db.session.commit()
        return redirect(url_for('admin_profile'))
    return redirect(url_for('admin_profile'))

@app.route('/user/update',methods=["GET","POST"])
def user_update():
    id=request.args.get('id')
    users = User.query.get(int(id))
    form = RegisterForm()
    if users:
        name = request.form.get('username')
        email = request.form.get('email')
        is_admin = request.form.get('is_admin')
        user = User(id=id,username=name,email=email,is_admin=is_admin)
        return render_template('update.html',head="user",form=form)
    return redirect(url_for('admin_profile'))    
    