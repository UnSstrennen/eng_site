from flask import Flask, render_template, session, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from configparser import ConfigParser
from transliterate import translit
from flask_sqlalchemy import SQLAlchemy


WEEK_DAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']


def to_en(word):
    new_word = translit(word, 'ru', reversed=True)
    return new_word


def to_ru(word, capitalize=False):
    new_word = translit(word, 'ru')
    if capitalize:
        new_word = new_word.capitalize()
    return new_word


def make_empty_timetable(user):
    """ creates an empty timetable for teacher """
    # check for existing
    query = Timetable.query.filter_by(user_id=user.id).first()
    if query is not None:
        return
    # if not exists
    for day in WEEK_DAYS:
        for number in range(1, 5):
            row = Timetable(day=day,
                            number=number,
                            full_name=user.full_name,
                            red_week='',
                            green_week='',
                            user_id=user.id)
            db.session.add(row)
    db.session.commit()
    return


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
    accepted = db.Column(db.Boolean, unique=False)

    def __repr__(self):
        return '<Teacher {} {} {}>'.format(
            self.id, self.username, self.full_name)


class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(30), unique=False, nullable=False)
    number = db.Column(db.Integer, unique=False, nullable=False)
    full_name = db.Column(db.String(80), unique=False, nullable=False)
    red_week = db.Column(db.String(30), unique=False, nullable=False)
    green_week = db.Column(db.String(30), unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Timetable {}/{} {}(id={}) {}/{}>'.format(
            self.day, self.number, self.full_name, self.user_id, self.red_week, self.green_week)


db.create_all()


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], id='form_string_field')
    password = PasswordField('Пароль', validators=[DataRequired()], id='form_string_field')
    submit = SubmitField('Войти', id='button')


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], id='form_string_field')
    password = PasswordField('Пароль', validators=[DataRequired()], id='form_string_field')
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()], id='form_string_field')
    full_name = StringField('ФИО (полностью)', validators=[DataRequired()], id='form_string_field')
    submit = SubmitField('Зарегестрироваться', id='button')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', session=session)


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
    return render_template('login.html', form=form, error=False, session=session)


@app.route('/idioms')
def idioms():
    return render_template('idioms.html', session=session)


@app.route('/advices')
def advices():
    return render_template('advices.html', session=session)


@app.route('/irregularverbs')
def irregularverbs():
    return render_template('irregularverbs.html', session=session)


@app.route('/motivation')
def motivation():
    return render_template('motivation.html', session=session)


@app.route('/popularwords')
def popularwords():
    return render_template('popularwords.html', session=session)


@app.route('/teachers')
def teachers():
    return render_template('teachers.html', session=session)


@app.route('/timetable')
def timetable():
    return render_template('timetable.html', session=session)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', session=session, form=form, error=True)
        teacher = Teacher(username=form.username.data,
                          full_name=form.full_name.data,
                          password=form.password.data,
                          accepted=False
                          )
        db.session.add(teacher)
        db.session.commit()
        return redirect('login')
    return render_template('register.html', session=session, form=form, error=False)


@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/index')
    if session['username'] == 'admin':
        return redirect('/admin')
    query = Teacher.query.filter_by(username=session['username']).first()
    full_name = query.full_name
    # prepare dict
    teacher_dict = dict()
    for day in WEEK_DAYS:
        teacher_dict[day] = dict
    # add data to dict
    for day in WEEK_DAYS:
        day_dict = dict()
        for number in range(1, 5):
            query = Timetable.query.filter_by(day=day, number=number, full_name=full_name).first()
            day_dict[number] = {'red_week': query.red_week, 'green_week': query.green_week}
        teacher_dict[day] = day_dict
    print(teacher_dict['Понедельник'][1])
    return render_template('profile.html', session=session, full_name=full_name,
                           week_days=WEEK_DAYS, data=teacher_dict)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/index')


@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect('/index')
    if session['username'] != 'admin':
        return redirect('/index')
    return render_template('admin.html', session=session, users=Teacher.query.all())


@app.route('/accept/<int:user_id>')
def accept(user_id):
    if 'username' not in session:
        return redirect('/index')
    if session['username'] != 'admin':
        return redirect('/index')
    query = Teacher.query.filter_by(id=user_id).first()
    query.accepted = not query.accepted
    if query.accepted:
        make_empty_timetable(query)
    db.session.commit()
    return redirect('/admin')


@app.route('/aaa', methods=['GET', 'POST'])
def aaa():
    if request.method == 'POST':
        print(request.args.get('name'))
    else:
        return '''<input type="text" name="name" size="40"><input type="submit" value="Отправить" 
            onclick="location.replace('http://ya.ru')">'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
