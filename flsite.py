
from flask import Flask, render_template, url_for, request, flash, g, send_file, abort, redirect, make_response, session
import sqlite3
import os
import io
from dotenv import load_dotenv
from source.db_manager import *

# 1. Дані авторизації
load_dotenv()

# Конфігурація
DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config.from_object(__name__)
# app.config['SECRET_KEY'] = 'c68310e032c7aa6aec8f5b01e475bb9b'
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

menu = [{'name': 'Жіночий', 'url': 'women'},
        {'name': 'Чоловічий', 'url': 'men'},
        {'name': 'Про нас', 'url': 'about'},
        {'name': "Зворотній зв'язок", 'url': 'contact'}
        ]


@app.route('/about')
def about():
    print(url_for('about'))
    print(dict(app.config)['SECRET_KEY'])
    return render_template('about.html', menu=menu)

    # res = make_response(content)
    # res.headers['Content-Type'] = 'text/plain'
    # res.headers['Server'] = 'flasksite'
    # return res


@app.route('/profile/<username>')
def profile(username):
    print(url_for('profile', username=username))

    return f"User: {username}"


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) < 2:
            flash("Ім'я повинно мати більше одного символа.")

        if len(request.form['email']) < 6:
            flash("Помилка відправки email")
        else:
            flash("Повідомлення відправлене")
        print(request.form)
    return render_template('contact.html', menu=menu)


@app.route('/')
def index():
    db = get_db()
    # print(g.link_db)
    dbase = FDataBase(db)

    # print(url_for('index'))

    products = dbase.get_product_atributes()

    return render_template('index.html', menu=menu, products=products)
    # return render_template('index.html', menu=dbase.get_menu())


# Маршрут, який дістає картинку з БД і віддає її як файл
@app.route('/image/<int:image_id>')
def get_image(image_id):
    db = get_db()
    dbase = FDataBase(db)

    image_bytes = dbase.get_image_by_id(image_id)

    if image_bytes is None:
        abort(404)

    return send_file(io.BytesIO(image_bytes), mimetype='image/jpeg')


# Додайте імпорт redirect, якщо його не було

# ... (ваш існуючий код) ...


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        # 1. Отримуємо текстові дані з форми
        name = request.form.get('name')
        model = request.form.get('model')
        color = request.form.get('color')
        price = request.form.get('price')
        arrival_date = request.form.get('arrival_date')

        # 2. Отримуємо файл картинки
        file = request.files.get('image')

        # Перевірка на заповненість обов'язкових полів
        if not (name and model and file):
            flash("Будь ласка, заповніть необхідні поля форми!")
            return render_template('admin.html', menu=menu)

        # Перевірка розширення файлу (дозволяємо лише jpg, jpeg, png)
        if file.filename:
            filename = file.filename.lower()
        if not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png')):
            flash("Недопустимий формат файлу! Дозволено лише .jpg, .jpeg, .png")
            return render_template('admin.html', menu=menu)

        try:
            # 3. Зчитуємо файл у байтовий формат прямо з оперативної пам'яті
            image_bytes = file.read()

            # 4. Записуємо в базу даних
            db = get_db()
            dbase = FDataBase(db)

            if dbase.add_product(name, model, color, price, arrival_date, image_bytes):
                flash("Товар успішно додано до бази даних!")
                # Перенаправлення на головну вітрину
                return redirect(url_for('index'))
            else:
                flash("Помилка при збереженні в базу даних.")

        except Exception as e:
            flash(f"Помилка обробки файлу: {e}")

    return render_template('admin.html', menu=menu)


@app.route('/login')
def login():
    log = ''
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')

    res = make_response(f"<h1>Форма авторизації</h1><p>logged: {log}</p>")
    res.set_cookie("logged", "yes")
    return res


@app.route('/logout')
def logout():
    res = make_response("<h4>Ви більше не авторизований</h4>")
    res.set_cookie("logged", "", 0)
    return res


@app.errorhandler(404)
def page_not_found(error):
    return "Сторінка не знайдена", 404


if __name__ == '__main__':
    app.run(debug=True)
