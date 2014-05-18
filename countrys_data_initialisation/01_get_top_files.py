from pymongo import Connection
import bcode
import json

connection = Connection('144.76.168.108', 27017)
connection.from_radars.authenticate('mipt', 'mipt')
db = connection.from_radars

connection2 = Connection('144.76.168.108', 27017)
connection2.metadata.authenticate('mipt', 'mipt')
db2 = connection2.metadata


item = db.torrents.find({ 'heard_times' : {"$gte" : 1}, u'metadata_exists' : True}).sort(u'heard_times' , -1).limit(10000)
i = 0
mass = []
file = open("01_thousand_most_popular","w")
for it in item:
    try:
        meta = db2.bcoded_metadata.find_one({"_id" : it["_id"]})
        meta = bcode.bdecode(meta['bcoded_metadata'])
        name = unicode(meta['name'], errors='ignore')
        length = meta['piece length']
        temp = [str(i), str(it['_id']),str(it['heard_times']), name, length]
        mass.append(temp)
    except:
        print "error"
    i = i + 1
    print i
data = json.dumps(mass)
file.write(data)
file.close()
print("Dumped to file -> 01_thousand_most_popular")