# Создать страницу, на которой будет форма для ввода имени и электронной почты, 
# при отправке которой будет создан cookie-файл
# с данными пользователя, а также будет произведено перенаправление на страницу 
# приветствия, где будет отображаться имя пользователя.


# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую 
# будет удалён cookie-файл с данными пользователя и произведено перенаправление 
# на страницу ввода имени и электронной почты.

from flask import Flask, make_response, request, url_for, render_template, redirect, session


app = Flask(__name__)


@app.route("/submit", methods = ["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        response = make_response(redirect(url_for('hello', name = name)))
        response.set_cookie('user', f'{name}:{email}')
        return response
    return render_template("form.html")     

@app.route('/hello/<name>')
def hello(name):
    # return f'Привет, {name}!'
    return render_template("hello.html", name)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('/submit')))
    response.set_cookie('user', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)

