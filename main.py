from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')
print(config.get('connect', 'pas'))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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
