from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import datetime
from funcs import load_data_from_json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///HW16.db"  # создание базы данных 'HW16.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # отслеживание изменения объектов
db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):  # Создание класса 'User' со структурой
	__tablename__ = "user"
	id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
	first_name = db.Column(db.TEXT(50))
	last_name = db.Column(db.TEXT(50))
	age = db.Column(db.INTEGER)
	email = db.Column(db.TEXT(100))
	role = db.Column(db.TEXT(50))
	phone = db.Column(db.TEXT(20))


class Order(db.Model):  # Создание класса 'Order' со структурой
	__tablemodel__ = "order"
	id = db.Column(db.INTEGER, primary_key=True)
	name = db.Column(db.TEXT(75))
	description = db.Column(db.TEXT(200))
	start_date = db.Column(db.DATE)
	end_date = db.Column(db.DATE)
	address = db.Column(db.TEXT(100))
	price = db.Column(db.INTEGER)
	customer_id = db.Column(db.INTEGER, db.ForeignKey("user.id"))  # вторичный ключ на 'id' из таблицы 'user'
	executor_id = db.Column(db.INTEGER, db.ForeignKey("user.id"))  # вторичный ключ на 'id' из таблицы 'user'


class Offer(db.Model):  # Создание класса 'Offer' со структурой
	__tablemodel__ = "offer"
	id = db.Column(db.INTEGER, primary_key=True)
	order_id = db.Column(db.INTEGER, db.ForeignKey("user.id"))  # вторичный ключ на 'id' из таблицы 'user'
	executor_id = db.Column(db.INTEGER, db.ForeignKey("user.id"))  # вторичный ключ на 'id' из таблицы 'user'


db.drop_all()  # Удаление данных из всех таблиц

db.create_all()  # Добавление всех данных в таблицы

data_list_user = load_data_from_json("JSON-files/Users.json")  # Через функцию загружаем данные JSON-файла в переменную по 'Users'

for user in data_list_user:
	db.session.add(User(
		id=user["id"],
		first_name=user["first_name"],
		last_name=user["last_name"],
		age=user["age"],
		email=user["email"],
		role=user["role"],
		phone=user["phone"]
						)
	               )
	db.session.commit()  # Вносим все изменения в базу данных


data_list_order = load_data_from_json("JSON-files/Orders.json")  # Через функцию загружаем данные JSON-файла в переменную по 'Order'

for order in data_list_order:
	# start_date_format = order["start_date"].split("/")
	# end_date_format = order["end_date"].split("/")

	month_start, day_start, year_start = order['start_date'].split('/')
	month_end, day_end, year_end = order['end_date'].split('/')

	db.session.add(Order(
		id=order["id"],
		name=order["name"],
		description=order["description"],
		# start_date=datetime.date(day=int(start_date_format[1]), month=int(start_date_format[0]), year=int(start_date_format[2])),
		# end_date=datetime.date(day=int(end_date_format[1]), month=int(end_date_format[0]), year=int(end_date_format[2])),
		start_date=datetime.date(int(year_start), int(month_start), int(day_start)),
		end_date=datetime.date(int(year_end), int(month_end), int(day_end)),
		address=order["address"],
		price=order["price"],
		customer_id=order["customer_id"],
		executor_id=order["executor_id"]
						)
	               )
	db.session.commit()  # Вносим все изменения в базу данных


data_list_offer = load_data_from_json("JSON-files/Offers.json")  # Через функцию загружаем данные JSON-файла в переменную по 'Offer'

for offer in data_list_offer:
	db.session.add(Offer(id=offer["id"], order_id=offer["order_id"], executor_id=offer["executor_id"],))
	db.session.commit()  # Вносим все изменения в базу данных
