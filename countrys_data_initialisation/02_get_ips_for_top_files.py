from pymongo import Connection
import bcode
import json

connection = Connection('144.76.168.108', 27017)
connection.peers.authenticate('mipt', 'mipt')
db = connection.peers

file_read = open("01_thousand_most_popular", "r")
data = json.load(file_read)
ids = []
file_write = open("02_ips_most_popular", "w")

for dat in data:
    ids.append(dat[1]) 

i = 0
item = db.history.find({ 'hash' : {"$in" : ids }})
for it in item:
    temp = str(i)+ ' ' + str(it['hash']) + ' ' + str(it['ip'])
    file_write.write(temp + '\n')
    print temp
    i = i + 1
file_read.close()
file_write.close()