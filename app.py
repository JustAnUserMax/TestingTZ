import datetime
import gspread
import psycopg2
import requests as re
from flask import Flask, render_template

general_url = "http://127.0.0.1:5000"

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def table():  # try для проверки на существование БД
    try:
        conn = psycopg2.connect(user="postgres",
                                password="1user_2",
                                host="127.0.0.1",
                                port="5432",
                                database="postgres")
        table_str = "orders"
        cursor = conn.cursor()
        # Проверка на существование таблицы, если ее нет, то создает ее
        cursor.execute("select exists(select relname from pg_class where relname='" + table_str + "')")

        exists = cursor.fetchone()[0]
        if not exists:
            cursor.execute("""CREATE TABLE ORDERS
                                    ( num CHARACTER VARYING(30), number_of_order CHARACTER VARYING(30),
                                      price_in_dollars CHARACTER VARYING(30), deadline CHARACTER VARYING(30),
        	                          price_in_rubles CHARACTER VARYING (30)
        	                        );
        	                """)
        # Подключение к сервисному аккаунту Google Sheets
        gs = gspread.service_account(filename='keys/tester-353417-b878ec101783.json')
        sh = gs.open("test")
        data_rub = re.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        doll_to_rub = data_rub['Valute']['USD']['Value']
        # Получение данных первого листа таблицы
        list_of_list = sh.sheet1.get_all_values()
        # Срез заголовков
        headers = list_of_list[:1]
        headers[0] += ['стоимость в рублях']
        # Заголовки
        headings = tuple(headers[0])
        rdata = list_of_list[1:]
        # Все остальные строчки
        list_of_tuple = []
        for row in rdata:
            list_of_tuple.append(tuple(row))
        # Промежуточные данные
        data = tuple(list_of_tuple)
        pros = 0
        for row in data:
            if datetime.datetime.today() > datetime.datetime.strptime(f'{row[3]}', '%d.%m.%Y'):
                pros += 1
        print(pros)
        # Обновление данных в случае изменения
        cursor.execute("""delete from orders""")
        for row in data:
            cursor.execute(f"""INSERT INTO orders (num, number_of_order, price_in_dollars, deadline, price_in_rubles) 
                            VALUES ({row[0]}, {row[1]}, {row[2]}, '{row[3]}', {row[2]}*{doll_to_rub});""")
            conn.commit()
        # Выборка данных из БД
        cursor.execute("""SELECT * from orders;""")
        rows = cursor.fetchall()
        my_list = []
        for row in rows:
            my_list.append(tuple(row))
        # Данные из БД
        data = tuple(my_list)
    except psycopg2.Error as e:
        print(e)
    return render_template("table.html", headings=headings, data=data)


if __name__ == '__main__':
    app.run()
