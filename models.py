import random
from extentions import remap

class PersonAttribute:
	rules = []

	def __init__(self, rules):
		self.rules = rules

	def parse(self, values):
		answer = 0
		for rule, value in zip(self.rules, values):
			answer += rule[value]
		
		return answer / len(self.rules)

	def sample(self):
		return [random.choice(list(rule.keys())) for rule in self.rules]

	def sampleValue(self):
		return self.parse(self.sample())


class IQAttribute(PersonAttribute):
	right_answers = [5, 5, 47]

	def parse(self, values):
		answer_academic_perfomance = self.rules[values[0]]
		answer_iq = 0
		for right_answer, value in zip(self.right_answers, values[1:]):
			try:
				if int(right_answer) == int(value):
					answer_iq += 1
			except ValueError:
				pass
				# print("someone is gunius")

		answer_iq /= len(self.right_answers)
		return answer_academic_perfomance * 0.5 + answer_iq * 0.5


	def sample(self):
		request = [random.choice(list(self.rules.keys()))]
		request.append(random.randint(4, 6))
		request.append(random.randint(4, 5))
		request.append(random.randint(46, 48))

		return request



class ExtraversionAttribute(PersonAttribute):
	
	def clip(self, value, lower, upper):
	    return lower if value < lower else upper if value > upper else value

	def parse(self, values):
		answer = 0.5
		for elem in values:
			answer += self.rules[0][elem]

		return self.clip(answer, 0, 1)


class Person:
	age = -1
	sex = PersonAttribute([{"Мужчина": 0, "Женщина": 1}])
	education = PersonAttribute([{"Среднее" : 0, "Среднее профессиональное" : 0.25, "Неоконченное высшее" : 0.5, "Высшее": 0.75, "Несколько высших" : 1}])
	iq = IQAttribute({"Отличник" : 1, "Хорошист" : 0.75, "По-разному получалось": 0.315})
	extraversion = ExtraversionAttribute([{"Полностью согласен" : 0.1, "Не согласен" : -0.1, "Затрудняюсь ответить" : 0}])
	altruistic = PersonAttribute([{"Сначала помогу другу, потом пойду на работу" : 1, "Объясню другу, что смогу помочь ему после работы" : 0}])
	hobby = PersonAttribute([{"Активное времяпровождение (спорт, туризм, любительский театр и проч.)" : 1, "В равной степени увлекаюсь и тем, и другим" : 0.5, "Домашние хобби (коллекционирование, любительская фотография, чтение и проч.)" : 1}])
	trust = PersonAttribute([
		{"Скорее всего, приобрету какую-нибудь из предлагаемых вещей" : 1, "Внимательно рассмотрю товары, которые мне предлагают, и если мне что-то понравится, я сделаю покупку" : 0.5, "Не буду ничего покупать, наверняка они предлагают некачественный товар" : 0}, 
		{"С удовольствием приму помощь" : 1, "Да, но после тщательно проверю выполненную им работу" : 0.5, "Нет, свою работу я всегда выполняю только самостоятельно" : 0},
		{"Да, зачем иначе делать комплимент" : 1, "Иногда верю комплиментам, а иногда нет" : 0.5, "Нет, мне кажется, что чужие люди не могут искренне хвалить кого-либо": 0}])

	@staticmethod
	def parse(values):
		answer = []

		answer.append(int(values[0]))
		answer.append(Person.sex.parse([values[1]]))
		answer.append(Person.education.parse([values[2]]))
		answer.append(Person.iq.parse(values[3:7]))
		answer.append(Person.extraversion.parse(values[7:12]))
		answer.append(Person.altruistic.parse([values[12]]))
		answer.append(Person.hobby.parse([values[13]]))
		answer.append(Person.trust.parse(values[14:17]))

		return answer

	@staticmethod
	def sample():
		answer = []

		answer.append(random.random())
		answer.append(Person.sex.sampleValue())
		answer.append(Person.education.sampleValue())
		answer.append(Person.iq.sampleValue())
		answer.append(Person.extraversion.sampleValue())
		answer.append(Person.altruistic.sampleValue())
		answer.append(Person.hobby.sampleValue())
		answer.append(Person.trust.sampleValue())

		return answer

	@staticmethod
	def fromFile(filename):
		DB = []

		f = open(filename, encoding="utf-8")
		for line in f.readlines():
			data = line[1:-2].split('\",\"')
			DB.append(Person.parse(data[3:]))
		f.close()

		min_age = min([x[0] for x in DB])
		max_age = max([x[0] for x in DB])

		for i, elem in enumerate(DB):
			elem[0] = remap(elem[0], max_age, min_age, 1, 0)
			DB[i] = elem

		return DB

