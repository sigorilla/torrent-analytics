from pymongo import Connection
import bcode

connection = Connection('144.76.168.108', 27017)
connection.from_radars.authenticate('mipt', 'mipt')
db = connection.from_radars

item = db.torrents.find({ 'heard_times' : {"$gte" : 1}, u'metadata_exists' : True}).sort(u'heard_times' , -1).limit(2000)
i = 0
file = open("01_thousand_most_popular","w")
for it in item:
    temp = str(i) + ' ' + str(it['_id'])+' ' + str(it['heard_times']) 
    file.write(temp+ '\n')
    print(temp)
    i = i + 1
file.close()
print("Dumped to file -> 01_thousand_most_popular")