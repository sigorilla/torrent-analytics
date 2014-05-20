from pymongo import Connection
import matplotlib.pyplot as plt
import numpy as np
import json

connection = Connection('144.76.168.108', 27017)
connection.metadata.authenticate('mipt','mipt')
db = connection.metadata

first = 50000000
second = 0
num = []
x = []
for i in range(250):
    second = first+20000000
    num.append(db.filelist.find({'length' : {'$lt' : second, '$gte' : first }}).count())
    x.append(second/1000000)
    first = second
    #print num[i], second/1000000
x_pos = np.array(x)
y_pos = np.array(num)
print x_pos, y_pos
print ""
print ""
print ""
print ""
print ""
print ""
#print json.dump(x_pos)
#print json.dump(y_pos)
plt.bar(x_pos, y_pos)
plt.xlabel('Size, mb')
plt.ylabel('N/20 mb')
plt.show()
