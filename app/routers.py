from flask import render_template,redirect,url_for,flash,request
from . import app
from .forms import RegisterForm,LoginForm
from .models import User
from . import db
from flask_login import login_user

@app.route('/',methods=["GET","POST"])
def home():
    form = LoginForm()
    if form.is_submitted():
        usr = User.query.filter_by(username=form.username.data).first()
        if usr and usr.verify_password(entered_password = form.password.data):
            login_user(user=usr)
            flash(f'You are sucessfully loggined as {form.username.data}')
            return redirect(url_for('profile',name=form.username.data))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'there was an error in : {err}')
            return render_template('home.html',form=form,error=err)
    return render_template('home.html',form=form)

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
        return redirect(url_for('profile'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'there was an error in : {err}')
            return render_template('signup.html',form=form,error=err)
    return render_template('signup.html',form=form)

@app.route('/admin/',methods=["GET","POST"])
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
            flash(f'there was an error in : {err}')
            return render_template('signup.html',head="Admin Registion",form=form,error=err)
    return render_template('signup.html',head="Admin Registion",form=form)

@app.route('/admin/login/',methods=["GET","POST"])
def admin_login():
    form = LoginForm()
    if form.is_submitted():
        print("hi")
        usr = User.query.filter_by(username=form.username.data).first()
        if usr and usr.verify_password(entered_password = form.password.data) and usr.is_admin == True:
            login_user(user=usr)
            flash(f'You are sucessfully loggined as {form.username.data}')
            return redirect(url_for('admin_profile',name=form.username.data))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f'there was an error in : {err}')
            return render_template('login.html',form=form,error=err)
    return render_template('login.html',form=form)

@app.route('/profile/',methods=["GET","POST"])
def profile():
    name=request.args.get('name')
    return render_template('profile.html',name=name)

@app.route('/profile_admin/',methods=["GET","POST"])
def admin_profile():
    users = User.query.filter_by(is_admin=False)
    if request.args.get('name'):
        name=request.args.get('name')
        return render_template('adminprofile.html',name=name,datas=users)
    return render_template('adminprofile.html',datas=users)

@app.route('/user/',methods=["GET","POST"])
def user_delete():
    id=request.args.get('id')
    users = User.query.get(int(id))
    if users:
        db.session.delete(users)
        db.session.commit()
        return redirect(url_for('admin_profile'))
    return redirect(url_for('admin_profile'))

@app.route('/user/',methods=["GET","POST"])
def user_update():
    id=request.args.get('id')
    users = User.query.get(int(id))
    if users:
        db.session.delete(users)
        db.session.commit()
        name = request.form.get('username')
        email = request.form.get('email')
        is_admin = request.form.get('is_admin')
        user = User(id=id,username=name)
    print(users)
    return redirect(url_for('admin_profile'))
    # usr = User.query.get(id=id)
    # print(usr)