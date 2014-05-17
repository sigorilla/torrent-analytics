from pymongo import Connection
import unicodedata
connection = Connection('144.76.168.108', 27017)
connection1 = Connection('localhost', 27017)
connection.peers.authenticate('mipt', 'mipt')
db = connection.peers
mydb = connection1.ips
#print db, mydb

i = 0
log = []
for item in db.history.find():
    #print item
    #ip = unicodedata.normalize("NFKD", item['ip']).encode('ascii', 'ignore')
    #hashid = unicodedata.normalize("NFKD", item['hash']).encode('ascii', 'ignore')
    tmp = mydb.test.find_one( { "_id" : item['ip']} )
    if tmp != None:
        #print tmp#['_id']
        tmp['hashes'].append(item['hash'])
        #print tmp
        #post = {"_id": item['_id'], "hashes": tmp['hashes'], "ip":item['ip']}
        mydb.test.save(tmp)
    else:
        post = {"_id": item['ip'], "hashes": [item['hash']]}
        mydb.test.insert(post)
    #log[item['ip']].append(item['id'])
    i+=1
    if i % 10000 == 0:
        print i
#print log

