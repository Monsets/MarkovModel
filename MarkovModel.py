import random

class _Dictogram(dict):
    def __init__(self, iterable=None):
        # Инициализируем наше распределение как новый объект класса,
        # добавляем имеющиеся элементы
        super(_Dictogram, self).__init__()
        self.types = 0  # число уникальных ключей в распределении
        self.tokens = 0  # общее количество всех слов в распределении
        if iterable:
            self.update(iterable, )

    def update(self, iterable, **kwargs):
        # Обновляем распределение элементами из имеющегося
        # итерируемого набора данных
        for item in iterable:
            if item in self:
                self[item] += 1
                self.tokens += 1
            else:
                self[item] = 1
                self.types += 1
                self.tokens += 1

    def count(self, item):
        # Возвращаем значение счетчика элемента, или 0
        if item in self:
            return self[item]
        return 0

    def return_random_word(self):
        random_key = random.sample(self, 1)
        # Другой способ:
        # random.choice(histogram.keys())
        return list(random_key)[0]

    def return_weighted_random_word(self):
        # Сгенерировать псевдослучайное число между 0 и (n-1),
        # где n - общее число слов
        random_int = random.randint(0, self.tokens - 1)
        index = 0
        list_of_keys = list(self.keys())
        # вывести 'случайный индекс:', random_int
        for i in range(0, self.types):
            index += self[list_of_keys[i]]
            # вывести индекс
            if (index > random_int):
                # вывести list_of_keys[i]
                return list_of_keys[i]

class MarkovModel():
    def __init__(self, order = 1, fully_connected = False):
        self._statics = dict()
        self._order = order
        self._fully_connected = fully_connected


    def fit(self, data):
        for current_slice in data:
            for i in range(0, len(current_slice) - 1):
                if current_slice[i] in self._statics:
                    # Просто присоединяем к уже существующему распределению
                    self._statics[current_slice[i]].update([current_slice[i + 1]])
                else:
                    self._statics[current_slice[i]] = _Dictogram([current_slice[i + 1]])

                if self._fully_connected:
                    if current_slice[i + 1] in self._statics:
                        self._statics[current_slice[i + 1]].update([current_slice[i]], )
                    else:
                        self._statics[current_slice[i + 1]] = _Dictogram([current_slice[i]])

    def generate(self, initial_word = None, length = 100):
        if initial_word == None:
            current_word = random.choice(list(self._statics.keys()))
        else:
            current_word = initial_word

        sentence = [current_word]

        for i in range(0, length):

            if current_word not in self._statics.keys():
                current_word = random.choice(list(self._statics.keys()))

            else:
                current_dictogram = self._statics[current_word]
                current_word = current_dictogram.return_weighted_random_word()

            sentence.append(current_word)

        return sentence

    def distribution_over(self, item):
        if item in self._statics.keys():
            return self._statics[item]
        return None

def make_higher_order_markov_model(order, data):
    markov_model = dict()

    for i in range(0, len(data) - order):
        # Создаем окно
        window = tuple(data[i: i + order])
        # Добавляем в словарь
        if window in markov_model:
            # Присоединяем к уже существующему распределению
            markov_model[window].update([data[i + order]], )
        else:
            markov_model[window] = _Dictogram([data[i + order]])
    return markov_model

