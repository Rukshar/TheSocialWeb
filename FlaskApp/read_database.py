import csv

def stringtupletotuple(s):
	if s == "":
		return None
	s = s.strip("()")
	l = s.split(", ")
	return tuple([float(x) for x in l])

def read_data():
	database = None

	with open('maga.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')

		database = []
		for i, row in enumerate(spamreader):
			if i == 0:
				continue

			if len(row) < 11:
				continue

			row[10] = stringtupletotuple(row[10])
			database.append(row)

	return database

read_data()