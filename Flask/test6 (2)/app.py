# -- coding: utf-8 --
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   render_template_string)  # render_template_string 쓰지마

from flask_wtf import FlaskForm
import pickle
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from datetime import datetime
from flask_moment import Moment

from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_googlemaps import GoogleMaps,Map

class MyForm(FlaskForm):
    text = StringField('text1', validators=[DataRequired()])
    password = PasswordField('password1')


class SearchFrom(FlaskForm):
    search = StringField('검색', validators=[DataRequired()])


app = Flask(__name__)
# 환경변수에 숨겨야한다. 안그러면 리스트로 다 보여진다.

app.config['DEBUG'] = True
app.config['SECURITY_REGISTERABLE'] = True  # 등록하게
app.config['SECRET_KEY'] = '문근영'  # 한글 한자 특수문자 해킹 덜 됨 # 암호화 키
app.config['SECURITY_PASSWORD_SALT'] = '문근영'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'  # 패스워드 해시
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = '/login.html'
app.config['GOOGLEMAPS_KEY']= 'AIzaSyA5pvygq6OIt2iPKryeqnV0i4RkLGtpCgc'


db = SQLAlchemy(app)  # flask <-> sql 연동
adbmin = Admin(app)  # 원래app에 admin을 확장 -? /admin 지원 (라우팅)
moment = Moment(app)
GoogleMaps(app)

# Define models
# 다대다 관계
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


class MyModelView(ModelView):
    pass


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

adbmin.add_view(ModelView(User, db.session))
adbmin.add_view(ModelView(Role, db.session))


# # Create a user to test with
# # 초기화
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='yjkwon9073@naver.com', password='password')
#     db.session.commit()
#

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # window //// mac ///
# app.config.update({'SECRET_KEY':'문근영'})
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 수정 변화를 추적


class TestModelView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.username

# crud create!!!!


@app.route('/map')
def map():
    import crime_data
    a, marker = crime_data.crimedata()

    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="moon",
        lat= a['GEO_LAT'],
        lng= a['GEO_LON'],
        language='ko',
        style=(
            "height:100%;"
            "width:100%;"
            "top:64;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
         markers = marker
    )
    dt = datetime(2018,7, 20)
    return render_template('map.html', sndmap=sndmap, dt=dt)

@app.route("/crimes")
def crimemapview():
    # creating a map in the view
    with open('crime.pickle', 'rb') as file:
        crimes = pickle.load(file)  # crimes 는 리스트

    crimemap = Map(
        identifier="jeung",
        lat=-104.949973,
        lng=39.726061,
        zoom=8,
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:500;"
        ),
        markers=crimes
    )
    return render_template('map.html', sndmap=crimemap)



@app.route('/add')
def add():
    user = User()
    user.email = 'yjkwon9073@naver.com'
    user.username = 'yjkwon'
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')


@app.route('/insert')
def insert():
    ue = request.args.get('ue')
    uu = request.args.get('uu')

    #from pandas_ import pandas_index
    #data = pandas_index()
    #data2 = data['name']

    # user = User()
    # user.email = ue
    # user.username =uu
    # db.session.add(user)
    # db.session.commit()
    # return render_template('index.html')

    # return render_template_string('index.html', data=data)



@app.route('/select')
def select():
    users = User.query.all()
    print(users)
    return render_template('index.html', users=users)


@app.route('/delete')
def delete():
    ue = request.args.get('ue')
    uu = request.args.get('uu')
    users = User()
    users.email = ue
    users.username = uu
    db.session.remove(users)
    db.session.commit()
    print(users)
    return render_template('index.html', users=users)


@app.route('/')
# @login_required # 로그인 해야지만 보임
# def hello_world():
#     users = User.query.all()
#     print(users)
#     return render_template('index.html', users =users)
def index():
    # a = [1,2,3,4,5,6,7,8]
    # b = list('abcdefg')
    # c = zip(a,b)
    # d = {'a': 1, 'b': 2, 'c': 3}
    # print(c)
    # return render_template('index.html', moon=d) # jinja2가 파이썬과 비슷해서 좋아

    # users = User.query.all()
    # return  render_template('index.html' ,moon= users)
    # return  render_template_string('{{a}}예쁘다', a='문근영')

    #dt = datetime(2018, 7, 20)dt=dt

    return render_template('index.html')


@app.route('/graph')
def graph():
    from data import plotdata

    script, div = plotdata()
    return render_template('graph.html', script=script, div=div)


@app.route('/<path>')
def path(path):
    return render_template('%s' % path)


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['serach']  # get -> args post -> form
    # search_term = request.get('serach')
    if search_term == '문근영':
        return render_template('index.html')
    return redirect('/form')


@app.route('/form', methods=['GET', 'POST'])  # default - > get
def form1():
    form = MyForm()
    if request.method == 'GET':
        if form.validate_on_submit():
            return render_template('index.html')
        return render_template('form.html', form2=form)
    else:
        if form.validate_on_submit():
            return render_template('index.html')
        return render_template('form.html', form2=form)
    return render_template('form.html')


@app.route('/a')
def hello():
    return "helloworld"


@app.route('/hello/')
def hello2():
    return 1
# 붙이는게 우아하다


# if __name__ == '__main__':
#     app.run()