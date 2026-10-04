from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c68310e032c7aa6aec8f5b01e475bb9b'

menu = [{'name': 'Жіночий', 'url': 'women'},
        {'name': 'Чоловічий', 'url': 'men'},
        {'name': 'Про нас', 'url': 'about'},
        {'name': "Зворотній зв'язок", 'url': 'contact'}
        ]


@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', menu=menu)


@app.route('/profile/<username>')
def profile(username):
    print(url_for('profile', username='Slava'))
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


if __name__ == '__main__':
    app.run(debug=True)
