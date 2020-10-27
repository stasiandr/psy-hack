from models import Person
import itertools as it

from extentions import remap

f = open('FinalData.csv', encoding="utf-8")

DB = []
Data = []

for line in f.readlines():
	data = line[1:-2].split('\",\"')
	Data.append(data)
	DB.append((data[0], Person.parse(data[3:])))

f.close()


min_age = min([x[1][0] for x in DB])
max_age = max([x[1][0] for x in DB])
weights = [9, 10, 3, 3, 8, 2, 3, 0]

for i, elem in enumerate(DB):
	elem[1][0] = remap(elem[1][0], max_age, min_age, 1, 0)
	DB[i] = elem


def dist(a, b):
	ans = 0
	for i, (a_n, b_n) in enumerate(zip(a, b)):
		ans += (a_n - b_n)**2 * weights[i]
	return ans

def dist_func(e):
	return e[0][1]

DB_comb = sorted(it.combinations(DB, 2), key=lambda elem: dist(elem[0][1], elem[1][1]))

f = open("output.csv", 'w', encoding="utf-8")

for comb in DB_comb[:]:
	row1 = next(x for x in Data if x[0] == comb[0][0])
	row2 = next(x for x in Data if x[0] == comb[1][0])

	f.write("\"" + str(row1[1]) + "\",\"" + str(row1[2]) + "\",\"" + str(row2[1]) + "\",\"" + str(row2[2]) + "\",\"" + str(dist(comb[0][1], comb[1][1])) + "\"\n")


f.close()