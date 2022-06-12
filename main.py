from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sqlite3.db"
db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
	firstname = db.Column(db.TEXT(50))
	lastname = db.Column(db.TEXT(50))
	age = db.Column(db.INTEGER)
	email = db.Column(db.TEXT(100))
	role = db.Column(db.TEXT(50))
	phone = db.Column(db.TEXT(20))


class Order(db.Model):
	__tablemodel__ = "order"
	id = db.Column(db.INTEGER, primary_key=True)
	name = db.Column(db.TEXT(75))
	description = db.Column(db.TEXT(200))
	start_date = db.Column(db.DATE)
	end_date = db.Column(db.DATE)
	address = db.Column(db.TEXT(100))
	price = db.Column(db.INTEGER)
	customer_id = db.Column(db.INTEGER)
	executor_id = db.Column(db.INTEGER)


class Offer(db.Model):
	__tablemodel__ = "offer"
	id = db.Column(db.INTEGER, primary_key=True)
	order_id = db.Column(db.INTEGER)
	executor_id = db.Column(db.INTEGER)
