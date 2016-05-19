from pymongo import MongoClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt


client = MongoClient('mongodb://localhost:27017/')
db = client.analysis
table = db.tags_with_spam

tbp = table.find()

first_n = input("Top X words: ")

freq = {}

for row in tbp:
	tag = row['tensorflow_tag']
	if row['tensorflow_correct'] == 1 and row['tensorflow_confidence'] > 0.5:
		if tag in freq:
			freq[tag] += 1
		else:
			freq[tag] = 1

bleh = sorted(freq, key=freq.get, reverse=True)
bleh = bleh[:first_n]
tup = [(x,freq[x]) for x in bleh]
wordcloud = WordCloud(width=1200, height=600).generate_from_frequencies(tup)

plt.axis("off")
plt.imshow(wordcloud, 'gray'),plt.show()