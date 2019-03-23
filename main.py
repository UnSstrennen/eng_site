from flask import Flask, render_template, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from configparser import ConfigParser
from transliterate import translit
from flask_sqlalchemy import SQLAlchemy


def to_en(word):
    new_word = translit(word, 'ru', reversed=True)
    return new_word


def to_ru(word, capitalize=False):
    new_word = translit(word, 'ru')
    if capitalize:
        new_word = new_word.capitalize()
    return new_word


config = ConfigParser()
config.read('config.ini')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + config.get("connect", "DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.get("connect", "SECRET_KEY")
db = SQLAlchemy(app)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Teacher {} {} {}>'.format(
            self.id, self.username, self.full_name)


class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(30), unique=True, nullable=False)
    full_name = db.Column(db.String(80), unique=False, nullable=False)
    red_week = db.Column(db.String(30), unique=False, nullable=False)
    green_week = db.Column(db.String(30), unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Timetable object>'


db.create_all()


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], id='form_string_field')
    password = PasswordField('Пароль', validators=[DataRequired()], id='form_string_field')
    submit = SubmitField('Войти', id='button')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        """ teacher = Teacher(username=form.username.data,
                          full_name=form.full_name.data,
                          password=form.password.data
                          )
        db.session.add(teacher)
        db.session.commit() """
        query = Teacher.query.filter_by(username=form.username.data, password=form.password.data).first()
        if query is None:
            return render_template('login.html', form=form, error=True)
        else:
            session['username'] = query.username
            session['user_id'] = query.id
            return redirect('/index')
    return render_template('login.html', form=form, error=False)


@app.route('/idioms')
def idioms():
    return render_template('idioms.html')


@app.route('/advices')
def advices():
    return render_template('advices.html')


@app.route('/irregularverbs')
def irregularverbs():
    return render_template('irregularverbs.html')


@app.route('/motivation')
def motivation():
    return render_template('motivation.html')


@app.route('/popularwords')
def popularwords():
    return render_template('popularwords.html')


@app.route('/teachers')
def teachers():
    return render_template('teachers.html')


@app.route('/timetable')
def timetable():
    return render_template('timetable.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
