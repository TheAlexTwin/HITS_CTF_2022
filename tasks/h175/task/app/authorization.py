from flask import session
from flask import redirect
from flask import url_for
from flask import render_template
from werkzeug.utils import secure_filename
import hashlib
import models
import re
import os

SALT = "Strong String"

def auth_check(session):
    if 'username' in session:
        username = session.get('username')
        user = models.User.query.filter(models.User.username == username).first()

        if not user:
            session.pop('username', None)
            return open('templates/authorization_inner_view.html', 'r').read().decode('utf-8')

        name = user.name2 + " " + user.name + " " + user.name3
        return render_template('profile_inner_view.html', name = name,
                                image = user.image_link)
    else:
        return open('templates/authorization_inner_view.html', 'r').read().decode('utf-8')


def authorize_by_request(request):
    username = request.form.get('username')
    password = request.form.get('password')

    m = hashlib.md5()
    m.update((password + SALT).encode())
    password = m.hexdigest()

    user = models.User.query.filter(models.User.username == username).first()

    if not user:
        return "No such user"
    elif password != user.password:
        return "Wrong password"
    else:
        session['username'] = username
        return redirect(url_for('index'), 302)


def registration_by_request(request, db):
    user = request.form.get('username')
    pasw = request.form.get('password')
    cpasw = request.form.get('cpassword')
    mail = request.form.get('email')
    name = request.form.get('name')
    name2 = request.form.get('name2')
    name3 = request.form.get('name3')

    link = models.DEFAULT_IMAGE_PATH

    profile = models.User.query.filter(models.User.username == user).first()
    if profile:
        return "User with such username already exist"
    profile = models.User.query.filter(models.User.email == mail).first()
    if profile:
        return "User with such email already exist"

    valid_email_pattern = "\S*@[A-Za-z0-9-\.]{,61}\.[A-Za-z]{2,4}"

    if pasw != cpasw:
        return "Passwords do not match"
    elif len(pasw) <= 6:
        return "Password is too short"
    elif len(user) <= 3:
        return "Username lenght can not be shorter than 3"
    elif not re.match(valid_email_pattern, mail):
        return "Invalid email"
    elif len(name) == 0 or len(name2) == 0 or len(name3) == 0:
        return "Invalid credentials"

    m = hashlib.md5()
    m.update((pasw + SALT).encode())
    pasw = m.hexdigest()

    u = models.User(name=name, name2=name2, name3=name3,
                    username=user, password=pasw,
                    email = mail, role=models.ROLE_USER)
    db.session.add(u)
    db.session.commit()

    return redirect(url_for('index'), code=302)


def edit_profile_by_request(request, session, db):
    if not 'username' in session:
        abort(401)
    username = session['username']

    user = models.User.query.filter(models.User.username == username).first()
    if not user:
        return "No such user"

    new_username = request.form.get('new_username')
    new_email = request.form.get('new_email')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    cnew_password = request.form.get('cnew_password')

    if new_email:
        another_user = models.User.query.filter(models.User.email == new_email).all()
        if another_user:
            return "E-mail already in use"
        else:
            user.email = new_email
    if new_username:
        another_user = models.User.query.filter(models.User.username == new_username).all()
        if another_user:
            return "Username already in use"
        else:
            user.username = new_username
    if new_password:
        if not old_password:
            return "Old password required"
        if not cnew_password:
            return "Repeat new password"

        m = hashlib.md5()
        m.update((old_password + SALT).encode())
        old_password = m.hexdigest()
        m = hashlib.md5()
        m.update((new_password + SALT).encode())
        new_password = m.hexdigest()
        m = hashlib.md5()
        m.update((cnew_password + SALT).encode())
        cnew_password = m.hexdigest()

        if old_password != user.password:
            return "Wrong password"
        elif new_password != cnew_password:
            return "Passwords do not match"
        else:
            user.password = new_password

    f = request.files['file']
    if 'file' in request.files:
        # check extension
        if not f.content_type == "image/jpeg":
            if not f.content_type == "image/png":
                if not f.content_type == "image/pjpeg":
                    return "File must be in .jpg/.jpeg/.png extension"

        link = 'static/resources/user_images/'
        link += str(user)
        if not os.path.exists(link):
            os.makedirs(link)
        link += '/' + secure_filename(f.filename)
        f.save(link)
        link = "/" + link
        user.image_link = link

    # apply changes
    db.session.commit()

    session.pop('username', None)
    return redirect('/index')
