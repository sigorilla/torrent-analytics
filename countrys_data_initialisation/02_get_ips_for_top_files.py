from pymongo import Connection
import bcode


connection = Connection('144.76.168.108', 27017)
connection.peers.authenticate('mipt', 'mipt')
db = connection.peers

file_read = open("01_thousand_most_popular", "r")
file_write = open("02_ips_most_popular", "w")
i = 0
for line in file_read:
    if ( int(line.split()[0]) < 0):
        continue
    
    id = line.split()[1]
    item = db.history.find({ 'hash' : id}).limit(10000)
    for it in item:
        temp = str(i)+ ' ' + str(id) + ' ' + str(it['ip'])
        file_write.write(temp + '\n')
        print temp
        i = i + 1
    print line
file_read.close()
file_write.close()