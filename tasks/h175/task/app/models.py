from main import db

ROLE_USER = 0
ROLE_ADMIN = 1

ACTIVE_FLAG = 0
IDEA_FLAG = 1

DEFAULT_IMAGE_PATH = "/static/resources/user_icon.jpg"

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), index = True, unique = False)
    name2 = db.Column(db.String(80), index = True, unique = False)
    name3 = db.Column(db.String(80), index = True, unique = False)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(100), index = True, unique = False)
    email = db.Column(db.String(120), index = True, unique = True)
    image_link = db.Column(db.String(120), index = True, unique = False,
                            default = DEFAULT_IMAGE_PATH)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.username)

    @staticmethod
    def delete_rec(data_rec):
        db.session.delete(data_rec)
        db.session.commit()


class Projects(db.Model):
    __tablename__ = "projects"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, index = True, unique = False)
    name = db.Column(db.String(100), index = True, unique = False)
    description = db.Column(db.String(200), index = True, unique = False)
    information = db.Column(db.String(140), index = True, unique = False)
    direction = db.Column(db.String(60), index = True, unique = False)
    date = db.Column(db.String(20), index = True, unique = False)
    flag = db.Column(db.SmallInteger, default = ACTIVE_FLAG)

    def __repr__(self):
        return '<Project: %r %r %r>' % (self.name, self.link)

    @staticmethod
    def delete_rec(data_rec):
        db.session.delete(data_rec) 
        db.session.commit()


class Comments(db.Model):
    __tablename__ = "comments"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key = True)
    project_id = db.Column(db.Integer, index = True, unique = False)
    author = db.Column(db.String(240), index = True, unique = False)
    image_link = db.Column(db.String(120), index = True, unique = False,
                            default = DEFAULT_IMAGE_PATH)
    text = db.Column(db.String(600), index = True, unique = False)

    def __repr__(self):
        return '<Comment by %r: %r>' % (self.author, self.text)

    @staticmethod
    def delete_rec(data_rec):
        db.session.delete(data_rec)
        db.session.commit()


class Directions(db.Model):
    __tablename__ = "directions"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key = True)
    direction = db.Column(db.String(60), index = True, unique = True)
    link = db.Column(db.String(100), index = True, unique = False)

    def __repr__(self):
        return '<Direction %r: %r>' % (self.direction, self.link)

    @staticmethod
    def delete_rec(data_rec):
        db.session.delete(data_rec)
        db.session.commit()


db.create_all()
