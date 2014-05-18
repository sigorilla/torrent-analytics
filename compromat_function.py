from pymongo import Connection
import bcode
import json


def compromatFunction(ip):
    connection1 = Connection('localhost', 27017)
    db1 = connection1.ips
    
    temp = db1.test.find({ "_id" : ip })
    if temp == None:
        return []
    connection2 = Connection('144.76.168.108', 27017)
    connection2.metadata.authenticate('mipt', 'mipt')
    db2 = connection2.metadata
    print temp
    item = db2.bcoded_metadata.find_one({"_id" : temp['hashes']})
    if item == None:
        return []
    temp = []
    for it in item:
        meta = bcode.bdecode(it['bcoded_metadata'])
        temp.append([ item["_id"], meta['name'] ])
    return temp

print compromatFunction("127.0.0.1")