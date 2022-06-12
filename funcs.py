import json

data_list = []


def load_data_from_json(path):
	"""Загрузка списка данных из файлов JSON"""
	global data_list

	with open(path, "r", encoding="utf-8") as data_file:
		data_list = json.load(data_file)
	return data_list
