# -*- coding: utf-8 -*-
from flask import abort
from flask import Flask
from flask import escape
from flask import redirect
from flask import request
from flask import render_template
from flask import render_template_string
from flask import session
from flask import send_file
from flask import send_from_directory
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

import datetime
import os

db_path = os.path.abspath(os.getcwd())+"/data"

# damn vulnerable flask application
# use only for CTF
app = Flask(__name__)

app.permanent_session_lifetime = datetime.timedelta(days=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + db_path
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'HITS{l0v3ly_t3mpl4t35}'

db = SQLAlchemy(app)

import models

from authorization import *


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.route('/')
@app.route('/index')
def index():
    projects = models.Projects.query.filter().all()

    html = ""
    projects = projects[::-1]
    for project in projects[:5]:
        user = models.User.query.filter(models.User.id == project.author_id).first()

        if not user:
            return "Author of project doesn't exist in DB"

        name = user.name2 + " " + user.name + " " + user.name3
        html += render_template('single_project_inner.html', name = project.name,
                                direction = project.direction,
                                date = project.date,
                                description = project.description,
                                image_link = user.image_link,
                                author_link = "/user/" + str(user.id),
                                project_link = "/projects/" + str(project.id),
                                author_name = name)

    header = "ПОСЛЕДНИЕ ОПУБЛИКОВАННЫЕ ПРОЕКТЫ"
    html = render_template('projects_inner.html',
                            header = header.decode('utf-8'),
                            projects = html)
    return render_template('main.html',
                            inner_html = html,
                            view = auth_check(session))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        return registration_by_request(request, db)
    else:
        # render page
        html = open('templates/registration_inner.html', 'r').read().decode('utf-8')
        return render_template('main.html', inner_html = html)


@app.route('/archive', methods=['GET'])
def archive():
    return render_template('main.html',
                            inner_html = '<h1>РЕАЛИЗОВАННЫЕ ИДЕИ<h1>'.decode('utf-8'),
                            view = auth_check(session))


@app.route('/projects/ideas')
def projects_ideas():
    projects = models.Projects.query.filter(models.Projects.flag == models.IDEA_FLAG).all()

    html = ""
    projects = projects[::-1]
    for project in projects:
        user = models.User.query.filter(models.User.id == project.author_id).first()

        if not user:
            return "Author of project doesn't exist in DB"

        name = user.name2 + " " + user.name + " " + user.name3
        html += render_template('single_project_inner.html', name = project.name,
                                direction = project.direction,
                                date = project.date,
                                description = project.description,
                                image_link = user.image_link,
                                author_link = "/user/" + str(user.id),
                                project_link = "/projects/" + str(project.id),
                                author_name = name)

    header = "ИДЕИ ДЛЯ ТАСКОВ"
    html = render_template('projects_inner.html',
                            header = header.decode('utf-8'),
                            projects = html)
    return render_template('main.html',
                            inner_html = html,
                            view = auth_check(session))


@app.route('/projects/active')
def projects_active():
    projects = models.Projects.query.filter(models.Projects.flag == models.ACTIVE_FLAG).all()

    html = ""
    projects = projects[::-1]
    for project in projects:
        user = models.User.query.filter(models.User.id == project.author_id).first()

        if not user:
            return "Author of project doesn't exist in DB"

        name = user.name2 + " " + user.name + " " + user.name3
        html += render_template('single_project_inner.html', name = project.name,
                                direction = project.direction,
                                date = project.date,
                                description = project.description,
                                image_link = user.image_link,
                                author_link = "/user/" + str(user.id),
                                project_link = "/projects/" + str(project.id),
                                author_name = name)

    header = "ТАСКИ В РАЗРАБОТКЕ"
    html = render_template('projects_inner.html',
                            header = header.decode('utf-8'),
                            projects = html)
    return render_template('main.html',
                            inner_html = html,
                            view = auth_check(session))


@app.route('/projects/<int:id>')
def project_by_id(id):
    project = models.Projects.query.filter(models.Projects.id == id).first()
    # if not found
    if not project:
        abort(404)

    id = project.author_id
    user = models.User.query.filter(models.User.id == id).first()
    # if not found again
    if not user:
        return "Project author doesn't exist"

    information = ""
    if 'username' in session:
        if session['username'] == user.username:
            information = project.information.replace('<', '&lt;').replace('>', '&gt;')

    name = user.name2 + " " + user.name + " " + user.name3

    comments = models.Comments.query.filter(models.Comments.project_id == project.id).all()
    comments_html = ""
    for comment in comments:
        comments_html += render_template('project_comment_inner.html',
                                        text = comment.text,
                                        author = comment.author,
                                        image = comment.image_link)

    edit_project = ""
    if 'username' in session:
        user = models.User.query.filter(models.User.username == session['username']).first()
        if user.id == project.author_id:
            edit_project = render_template('edit_project_link.html',
                                            link = "/projects/" + str(id) + "/edit")

    # very unsafe code
    vulnerable_template = open('templates/project_info_inner.html', 'r').read().decode('utf-8') % information
    html = render_template_string(vulnerable_template,
                            name = name, project = project.name,
                            direction = project.direction, date = project.date,
                            description = project.description,
                            comments = comments_html, project_id = project.id,
                            document_link = "/projects/" + str(id) + "/download",
                            edit_project = edit_project,
                            information = information)

    return render_template('main.html',
                            inner_html = html,
                            view = auth_check(session))


@app.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    if not 'username' in session:
        abort(401)
    username = session['username']
    user = models.User.query.filter(models.User.username == username).first()

    if request.method == 'POST':
        direction = request.form.get('direction')
        description = request.form.get('description')
        name = request.form.get('name')
        information = request.form.get('information')

        if not name:
            return "Name can't be empty"
        if not description:
            return "You need to provide a description"
        if not direction:
            return "You need to choose the direction"

        project = models.Projects.query.filter(models.Projects.id == id).first()
        if not project:
            return "Project not found"

        project.name = name
        project.description = description
        project.direction = direction
        project.information = information

        db.session.commit()
        return redirect('/user')
    else:
        # render edit page
        project = models.Projects.query.filter(models.Projects.id == id).first()
        user = models.User.query.filter(models.User.id == project.author_id).first()
        if not project:
            return "Project doesn't exist"
        if not user:
            return "Author doesn't exist"
        if user.id != project.author_id:
            abort(403)

        directions = models.Directions.query.filter().all()
        options = ""
        for direction in directions:
            options += "<option>" + direction.direction + "</option>" + "\n"

        html = render_template('edit_project_inner.html',
                                options = options,
                                description = project.description,
                                name = project.name,
                                information = project.information)
        return render_template('main.html',
                                inner_html = html,
                                view = auth_check(session))


@app.route('/projects/<int:id>/delete', methods=['POST'])
def delete_project(id):
    if not 'username' in session:
        abort(401)
    project = models.Projects.query.filter(models.Projects.id == id).first()
    user = models.User.query.filter(models.User.username == session['username']).first()

    if project.author_id != user.id:
        abort(403)

    # delete comments
    comments = models.Comments.query.filter(models.Comments.project_id == id).all()
    for comment in comments:
        models.Comments.delete_rec(comment)

    # delete project
    models.Projects.delete_rec(project)
    return redirect('/user')


@app.route('/post_comment', methods=['POST'])
def post_comment():
    if not 'username' in session:
        abort(401)
    else:
        username = session['username']

    text = request.form.get('comment')
    project_id = request.form.get('project_id')

    user = models.User.query.filter(models.User.username == username).first()
    name = user.name2 + " " + user.name + " " + user.name3

    if not text:
        return "Comment form can't be empty"
    if not project_id:
        return "Project id is required"
    if not user:
        return "User doesn't exist"

    c = models.Comments(project_id = project_id, author = name,
                        text = text, image_link = user.image_link)

    db.session.add(c)
    db.session.commit()

    return redirect('/projects/' + str(project_id))


@app.route('/directions')
def directions_info():
    directions = models.Directions.query.filter().all()
    html = ""
    for direction in directions:
        html += render_template('simple_direction_inner.html',
        direction = direction.direction, link = direction.link)
    html = render_template('research_directions_inner.html',
                            directions = html)
    return render_template('main.html',
                            inner_html = html,
                            view = auth_check(session))


@app.route('/info')
def info():
    html = render_template('information_inner.html').encode('utf-8')
    return render_template('main.html',
                            inner_html = html.decode('utf-8'),
                            view = auth_check(session))


@app.route('/user')
def profile():
    if 'username' in session:
        username = session.get('username')
        user = models.User.query.filter(models.User.username == username).first()
        return redirect('/user/' + str(user.id))
    else:
        abort(401)


@app.route('/user/<int:id>')
def profile_by_id(id):
    user = models.User.query.filter(models.User.id == id).first()
    # if not found
    if not user:
        abort(404)

    actions = ""
    if 'username' in session:
        username = session['username']
        if username == user.username:
            actions = open('templates/actions_inner.html').read().decode('utf-8')

    name = user.name2 + " " + user.name + " " + user.name3
    email = user.email

    projects = models.Projects.query.filter(models.Projects.author_id == user.id).all()

    html = ""
    for project in projects:
        html += render_template('projects_list_inner.html', name = project.name,
                                date = project.date, direction = project.direction,
                                link = '/projects/' + str(project.id))

    html = render_template('profile_inner.html', projects = html,
                            image = user.image_link, email = email,
                            name = name, actions = actions)
    return render_template('main.html',
                            inner_html = html,
                            view = auth_check(session))


@app.route('/settings')
def user_settings():
    return "Not available"


@app.route('/edit_profile', methods = ['POST'])
def edit_profile():
    return edit_profile_by_request(request, session, db)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if not 'username' in session:
            abort(401)

        name = request.form.get('name')
        description = request.form.get('description')
        direction = request.form.get('direction')
        status = request.form.get('status')
        information = request.form.get('information')
        username = session.get('username')

        user = models.User.query.filter(models.User.username == username).first()
        if not user:
            return "User doesn't exist"

        if not name:
            return "You need to provide a name"
        if not description:
            return "You need to provide a description"
        if not direction:
            return "Direction is undefined"
        if not status:
            return "Undefined status"

        if status == "idea":
            flag = models.IDEA_FLAG
        else:
            flag = models.ACTIVE_FLAG

        # current day
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        project = models.Projects(author_id = user.id, name = name,
                                description = description, direction = direction,
                                date = date, flag = flag, information = information)
        db.session.add(project)
        db.session.commit()

        return redirect('/index')
    else:
        directions = models.Directions.query.filter().all()
        options = ""
        for direction in directions:
            options += "<option>" + direction.direction + "</option>" + "\n"
        html = render_template('upload_inner.html',
                                options = options)
        return render_template('main.html',
                                inner_html=html,
                                view = auth_check(session))


@app.route('/auth', methods=['POST'])
def auth():
    return authorize_by_request(request)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    if not 'username' in session:
        abort(401)
    username = session['username']
    user = models.User.query.filter(models.User.username == username).first()

    # delete user projects
    projects = models.Projects.query.filter(models.Projects.author_id == user.id).all()
    for project in projects:
        models.Projects.delete_rec(project)

    # delete user
    models.User.delete_rec(user)
    logout()

    return "User " + username + " deleted successfully"


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
