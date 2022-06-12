import json
from datetime import datetime
from flask import request, render_template, jsonify

from models_init import *

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///HW16.db"  # создание базы данных 'HW16.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # отслеживание изменения объектов
db: SQLAlchemy = SQLAlchemy(app)


@app.route("/")  # Главная страница
def main_page():
	return render_template("main_page.html")


@app.route("/users/", methods=["GET", "POST"])  # Получение данных всех пользователей
def get_all_users():
	if request.method == "GET":
		user_list = User.query.all()

		user_response = []

		for user_ in user_list:
			user_response.append(
				{
					"id": user_.id,
					"first_name": user_.first_name,
					"last_name": user_.last_name,
					"age": user_.age,
					"email": user_.email,
					"role": user_.role,
					"phone": user_.phone,
				}
			)

		return jsonify(user_response)

	if request.method == "POST":
		try:
			new_user = json.loads(request.data)
			new_user_data = User(
				id=new_user["id"],
				first_name=new_user["first_name"],
				last_name=new_user["last_name"],
				age=new_user["age"],
				email=new_user["email"],
				role=new_user["role"],
				phone=new_user["phone"],
			)

			db.session.add(new_user_data)
			db.session.commit()
			db.session.close()
			return "Новый пользователь был добавлен."
		except TypeError as error:
			return error
		except Exception as e:
			return e


@app.route("/users/<int:qid>/", methods=["GET", "PUT", "DELETE"])  # Получение, изменение и удаление данных одного пользователя по его id
def get_one_user(qid: int):
	if request.method == "GET":
		user_ = User.query.get(qid)

		if user_ is None:
			return render_template("error_404.html")

		return jsonify(
			{
				"id": user_.id,
				"first_name": user_.first_name,
				"last_name": user_.last_name,
				"age": user_.age,
				"email": user_.email,
				"role": user_.role,
				"phone": user_.phone,
			}
		)

	elif request.method == "PUT":
		user_edit = json.loads(request.data)
		user_put = db.session.query(User).get(qid)

		if user_put is None:
			return render_template("error_404.html")

		user_put.first_name = user_edit["first_name"]
		user_put.last_name = user_edit["last_name"]
		user_put.age = user_edit["age"]
		user_put.email = user_edit["email"]
		user_put.role = user_edit["role"]
		user_put.phone = user_edit["phone"]

		db.session.add(user_put)
		db.session.commit()
		db.session.close()

		return f"Пользователь с id = {qid} успешно изменен!"

	elif request.method == "DELETE":
		user_del = db.session.query(User).get(qid)

		if user_del is None:
			return render_template("error_404.html")

		db.session.delete(user_del)
		db.session.commit()
		db.session.close()

		return f"Пользователь с id = {qid} успешно удален!"


@app.route("/orders/", methods=["GET", "POST"])  # Получение данных всех заказов
def get_all_orders():
	if request.method == "GET":
		order_list = Order.query.all()

		order_response = []

		for order_ in order_list:
			order_response.append(
				{
					"id": order_.id,
					"name": order_.name,
					"description": order_.description,
					"start_date": order_.start_date,
					"end_date": order_.end_date,
					"address": order_.address,
					"price": order_.price,
					"customer_id": order_.customer_id,
					"executor_id": order_.executor_id,
				}
			)

		return jsonify(order_response)

	if request.method == "POST":
		try:
			new_order = json.loads(request.data)
			new_order_data = Order(
				id=new_order["id"],
				name=new_order["name"],
				description=new_order["description"],
				start_date=datetime.date(int(year_start), int(month_start), int(day_start)),
				end_date=datetime.date(int(year_end), int(month_end), int(day_end)),
				address=new_order["address"],
				price=new_order["price"],
				customer_id=new_order["customer_id"],
				executor_id=new_order["executor_id"],
									)

			db.session.add(new_order_data)
			db.session.commit()
			db.session.close()
			return f"Новый заказ был добавлен."
		except Exception as e:
			return e


@app.route("/orders/<int:qid>/", methods=["GET", "PUT", "DELETE"])  # Получение, изменение и удаление данных одного заказа по его id
def get_one_order(qid: int):
	if request.method == "GET":
		order_ = Order.query.get(qid)

		if order_ is None:
			return render_template("error_404.html")

		return jsonify(
			{
				"id": order_.id,
				"name": order_.name,
				"description": order_.description,
				"start_date": order_.start_date,
				"end_date": order_.end_date,
				"address": order_.address,
				"price": order_.price,
				"customer_id": order_.customer_id,
				"executor_id": order_.executor_id,
			}
		)
	elif request.method == "PUT":
		try:
			order_edit = json.loads(request.data)
			order_put = db.session.query(Order).get(qid)

			if order_put is None:
				return render_template("error_404.html")

			order_put.id = order_edit["id"]
			order_put.name = order_edit["name"]
			order_put.description = order_edit["description"]
			order_put.start_date = datetime.date(int(year_start), int(month_start), int(day_start))
			order_put.end_date = datetime.date(int(year_end), int(month_end), int(day_end))
			order_put.address = order_edit["address"]
			order_put.price = order_edit["price"]
			order_put.customer_id = order_edit["customer_id"]
			order_put.executor_id = order_edit["executor_id"]

			db.session.add(order_put)
			db.session.commit()
			db.session.close()

			return f"Заказ с id = {qid} успешно изменен!"
		except Exception as e:
			return e

	elif request.method == "DELETE":
		order_del = db.session.query(Order).get(qid)

		if order_del is None:
			return render_template("error_404.html")

		db.session.delete(order_del)
		db.session.commit()
		db.session.close()

		return f"Заказ с id = {qid} успешно удален!"


@app.route("/offers/", methods=["GET", "POST"])  # Получение данных всех предложений
def get_all_offers():
	if request.method == "GET":
		offer_list = Offer.query.all()

		offer_response = []

		for offer_ in offer_list:
			offer_response.append(
				{
					"id": offer_.id,
					"order_id": offer_.order_id,
					"executor_id": offer_.executor_id,
				}
			)

		return jsonify(offer_response)

	if request.method == "POST":
		try:
			new_offer = json.loads(request.data)
			new_offer_data = Offer(
				id=new_offer["id"],
				order_id=new_offer["order_id"],
				executor_id=new_offer["executor_id"],
			)

			db.session.add(new_offer_data)
			db.session.commit()
			db.session.close()
			return f"Новое предложение было добавлено."
		except Exception as e:
			return e


@app.route("/offers/<int:qid>/", methods=["GET", "PUT", "DELETE"])  # Получение, изменение и удаление данных одного предложения по его id
def get_one_offer(qid: int):
	if request.method == "GET":
		offer_ = Offer.query.get(qid)

		if offer_ is None:
			return render_template("error_404.html")

		return jsonify(
			{
				"id": offer_.id,
				"order_id": offer_.order_id,
				"executor_id": offer_.executor_id,
			}
		)

	if request.method == "PUT":
		offer_edit = json.loads(request.data)
		offer_put = db.session.query(Offer).get(qid)

		if offer_put is None:
			return render_template("error_404.html")

		offer_put.id = offer_edit["id"]
		offer_put.order_id = offer_edit["order_id"]
		offer_put.executor_id = offer_edit["executor_id"]

		db.session.add(offer_put)
		db.session.commit()
		db.session.close()

		return f"Предложение с id = {qid} успешно изменено!"

	if request.method == "DELETE":
		offer_del = db.session.query(Offer).get(qid)

		if offer_del is None:
			return render_template("error_404.html")

		db.session.delete(offer_del)
		db.session.commit()
		db.session.close()

		return f"Предложение с id = {qid} успешно удалено!"


@app.errorhandler(404)  # Форма для вывода ошибка при неправильном URL-адресе, если страница не будет найдена
def page_not_found(e):
	return render_template("error_404.html", e=e), 404


@app.errorhandler(500)  # Форма при проблемах с сервером, внутренней ошибке в программе
def page_not_found(e):
	return render_template("error_500.html", e=e), 500


if __name__ == "__main__":
	app.run(debug=True)
