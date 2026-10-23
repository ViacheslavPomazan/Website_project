from flask import g, send_file
import sqlite3
import os
import io
from flsite import app

# З'єднання з БД


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    print('conn:', conn)
    return conn


# З'єднання з БД в момент створення контексту додатка
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
# Закриваємо з'єднання з БД при знищення контексту додатка
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

#     def get_menu(self):
#         sql = '''SELECT title, url FROM mainmenu'''
#         try:
#             self.__cur.execute(sql)
#             res = self.__cur.fetchall()
#             if res:
#                 return res
#         except:
#             print("Reading DB error")
#         return []

    def get_product_atributes(self):
        try:
            self.__cur.execute(
                "SELECT image_id, name, model, color, price FROM product_images ORDER BY image_id DESC")
            prod_attrs = self.__cur.fetchall()
            if prod_attrs:
                return prod_attrs
        except sqlite3.Error as e:
            print(f"Помилка читання з БД: {e}")
            return []

    def get_image_by_id(self, image_id):
        try:
            self.__cur.execute(
                "SELECT image FROM product_images WHERE image_id = ?", (image_id,))
            row = self.__cur.fetchone()
            if row:
                return row['image']  # Повертаємо суто бінарні дані
        except sqlite3.Error as e:
            print(f"Помилка читання зображення з БД: {e}")
        return None

    def add_product(self, name, model, color, price, arrival_date, image_bytes):
        try:
            sql = '''INSERT INTO product_images
                        (name, model, color, price, arrival_date, image)
                        VALUES (?, ?, ?, ?, ?, ?)'''
            self.__cur.execute(
                sql, (name, model, color, price, arrival_date, image_bytes))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Помилка додавання товару в БД: {e}")
            return False


# Завантаження зображення в БД
# Переконайтеся, що файл 'photo.jpg' лежить поруч із цим скриптом
def convert_jpg_to_blob():
    # Читаємо файл картинки в бінарному форматі ('rb')
    with open('Darda_3.jpg', 'rb') as file:
        blob_data = file.read()

    db = connect_db()
    cursor = db.cursor()
    # Виконуємо INSERT INTO, використовуючи знак ? як плейсхолдер
    sql_query = "INSERT INTO product_images (product_id, name, image) VALUES (?, ?, ?)"
    cursor.execute(sql_query, (103, 'Darda_3.jpg', blob_data))

    db.commit()
    db.close()
