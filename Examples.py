from MarkovModel import MarkovModel

text = [['hello', 'its', 'me', 'i', 'would', 'like', 'to', 'buy', 'some', 'cheese']]

mm = MarkovModel()
mm.fit(text)
print(mm.generate(length = 5))
print(mm.distribution_over('hello'))
