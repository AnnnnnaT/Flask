# Создать форму для регистрации пользователей на сайте. 
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль"
# и кнопку "Зарегистрироваться". 
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

from flask import Flask, render_template, request, url_for
from form import RegistrationForm
from models import db, User
from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)


db.init_app(app)

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route("/submit/", methods = ["GET", "POST"])
def registration():
    form = RegistrationForm()
    if request.method == "POST" and form.validate():
        first_name = form.first_name.data
        second_name = form.second_name.data
        email = form.email.data
        password = form.password.data
        user = User(first_name = first_name, second_name = second_name,
                     email = email, password=password)
        db.session.add(user)
        db.session.commit()
        print('user added in DB!')
    return render_template('form.html', form=form)