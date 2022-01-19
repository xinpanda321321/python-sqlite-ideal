import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

conn = sqlite3.connect('train.db')
cursor = conn.cursor()

# read training data
def read_csv(path):
	df = pd.read_csv(path)
	result_dict = {}
	columns = list(df.columns)
	for i in range(len(columns)):
		result_dict[columns[i]] = list(df[columns[i]])

	return result_dict

# create train_table 
def create_train_table(conn, data):
	keys = list(data.keys())
	temp_values = list(data.values())

	cursor = conn.cursor()
	cursor.execute("Drop table if exists train_table")
	table  = "create table train_table ("
	for i in range(len(keys)):
		if i == len(keys) - 1:
			table += keys[i] + " float);"
		else:
			table += keys[i] + " float, "

	sql = "insert into train_table("
	for i in range(len(keys)):
		if i == len(keys) - 1:
			sql += keys[i] + ') values('
		else:
			sql += keys[i] + ','
	for i in range(len(keys)):
		if i == len(keys) - 1:
			sql += "?)"
		else:
			sql += "?,"

	values = []
	for i in range(len(temp_values[0])):
		temp = []
		for j in range(len(temp_values)):
			temp.append(temp_values[j][i])
		values.append(temp)

	cursor.execute(table)
	cursor.executemany(sql, values)
	conn.commit()

# create test table
def create_test_table(conn, data):
	keys = list(data.keys())
	temp_values = list(data.values())

	cursor = conn.cursor()
	cursor.execute("Drop table if exists test_table")
	table  = "create table test_table ("
	for i in range(len(keys)):
		if i == len(keys) - 1:
			table += keys[i] + " float);"
		else:
			table += keys[i] + " float, "

	sql = "insert into test_table("
	for i in range(len(keys)):
		if i == len(keys) - 1:
			sql += keys[i] + ') values('
		else:
			sql += keys[i] + ','
	for i in range(len(keys)):
		if i == len(keys) - 1:
			sql += "?)"
		else:
			sql += "?,"

	values = []
	for i in range(len(temp_values[0])):
		temp = []
		for j in range(len(temp_values)):
			temp.append(temp_values[j][i])
		values.append(temp)

	cursor.execute(table)
	cursor.executemany(sql, values)
	conn.commit()

def create_ideal_table(conn, data):
	keys = list(data.keys())
	temp_values = list(data.values())

	cursor = conn.cursor()
	cursor.execute("Drop table if exists ideal_table")
	table  = "create table ideal_table ("
	for i in range(len(keys)):
		if i == len(keys) - 1:
			table += keys[i] + " float);"
		else:
			table += keys[i] + " float, "

	sql = "insert into ideal_table("
	for i in range(len(keys)):
		if i == len(keys) - 1:
			sql += keys[i] + ') values('
		else:
			sql += keys[i] + ','
	for i in range(len(keys)):
		if i == len(keys) - 1:
			sql += "?)"
		else:
			sql += "?,"

	values = []
	for i in range(len(temp_values[0])):
		temp = []
		for j in range(len(temp_values)):
			temp.append(temp_values[j][i])
		values.append(temp)

	cursor.execute(table)
	cursor.executemany(sql, values)
	conn.commit()

def get_best_ideal(conn):
	cursor = conn.cursor()
	ideal_index = []
	for k in range(4):
		cursor.execute('select x, y' + str(k + 1) + ' from train_table')
		result_train = cursor.fetchall()

		result = []
		for j in range(50):
			sum_value = 0
			for i in range(len(result_train)):
				sql = 'select y' + str(j + 1) + ' from ideal_table where x=' + str(result_train[i][0])
				cursor.execute(sql)
				ideal_value = cursor.fetchall()
				sum_value += (result_train[i][1] - ideal_value[0][0]) ** 2
			sum_value = sum_value ** 0.5
			result.append(sum_value)

		# get min index
		min_value = min(result)
		min_index = result.index(min_value) + 1
		print('train y' + str(k + 1) + " : ideal y" + str(min_index))
		ideal_index.append(min_index)
	return ideal_index

def calculate_test(conn, ideal_index):
	cursor = conn.cursor()
	test_values = []

	cursor.execute('select x, y from test_table')
	result_test = cursor.fetchall()

	for i in range(len(ideal_index)):
		sum_value = 0
		temp_y = []
		for j in range(len(result_test)):
			sql = 'select y' + str(ideal_index[i]) + ' from ideal_table where x=' + str(result_test[j][0])
			cursor.execute(sql)
			test_value = cursor.fetchall()
			temp_y.append(result_test[j][0] - test_value[0][0])
			sum_value += (result_test[j][0] - test_value[0][0]) ** 2
		sum_value = sum_value ** 0.5
		test_values.append(sum_value)
		print("test y" + str(i + 1) + " : " + str(sum_value))

def graph_plot(conn, ideal_index):
	cursor = conn.cursor()

	fig, axs = plt.subplots(4)
	fig.set_size_inches(100, 70)
	for i in range(4):
		cursor.execute('select x, y' + str(i + 1) + ' from train_table')
		result_train = cursor.fetchall()

		cursor.execute('select y' + str(ideal_index[i]) + ' from ideal_table')
		resutl_ideal = cursor.fetchall()

		x_value = []
		y_train = []
		y_ideal = []
		for j in range(len(result_train)):
			x_value.append(result_train[j][0])
			y_train.append(result_train[j][1])
			y_ideal.append(resutl_ideal[j][0])

		axs[i].plot(x_value, y_train, label="train y" + str(i + 1))
		axs[i].plot(x_value, y_ideal, label="ideal y" + str(ideal_index[i]))
	for ax in axs.flat:
		ax.set(xlabel='x value', ylabel='y value')
		ax.legend()
	plt.show()
	

# train_data = read_csv('train.csv')
# print(train_data)
# test_data = read_csv('test.csv')
# ideal_data = read_csv('ideal.csv')

# create_train_table(conn, data)
# create_test_table(conn, test_data)
# create_ideal_table(conn, ideal_data)

ideals = get_best_ideal(conn)
# calculate_test(conn, ideals)
graph_plot(conn, ideals)