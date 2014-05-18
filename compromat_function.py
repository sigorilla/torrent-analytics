from pymongo import Connection
import bcode
import json


def compromatFunction(ip):
    connection1 = Connection('localhost', 27017)
    db1 = connection1.ips
    
    temp = db1.test.find_one({ "_id" : ip })
    if temp == None:
        return []
    #print temp
    connection2 = Connection('144.76.168.108', 27017)
    connection2.metadata.authenticate('mipt', 'mipt')
    db2 = connection2.metadata
    
    item = db2.bcoded_metadata.find({"_id" : { "$in" :temp['hashes']}})
    if item == None:
        return []
    temp = []
    for it in item:
        meta = bcode.bdecode(it['bcoded_metadata'])
        temp.append([ it["_id"], meta['name'] ])
    return temp

print compromatFunction("127.0.0.1")
