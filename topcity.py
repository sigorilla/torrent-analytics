from pymongo import Connection
import bcode
import json
from collections import defaultdict
import operator
import matplotlib.pyplot as plt
def biggestTownsFunction():
    sum1=0
    connection1 = Connection('localhost', 27017)
    db1 = connection1.ips
    country_nums = defaultdict(int)
    for item in db1.cities.find():
        sum1+=item['number']
        country_nums[item['country']] += (item['number'])#/39611
    #print sum1
    return sorted(country_nums.iteritems(), key=operator.itemgetter(1),  reverse=True )
data =  biggestTownsFunction()
#print data
labels = []
sizes = []
explode= []
sum = 0
for i in range(10):
    labels.append(data[i][0])
    sizes.append(data[i][1])
    sum += sizes[i]
    explode.append(0)
labels.append('Others')
sizes.append(3961180-sum)
explode.append(0)
print labels
print sizes
colors = ['#ff8c00','#98fb98','#6495ed','#ffc0cd','#f4a460','#e0eee0','#d8bfd8','#fa8072','#f0e68c','#e6e6fa', '#cdcdc1']
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.show()
