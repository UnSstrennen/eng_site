from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from configparser import ConfigParser
from transliterate import translit


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
print(config.get('connect', 'pas'))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], id='form_string_field')
    password = PasswordField('Пароль', validators=[DataRequired()], id='form_string_field')
    submit = SubmitField('Войти', id='button')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


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
