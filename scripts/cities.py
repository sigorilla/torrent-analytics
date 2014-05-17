import pygeoip
from pymongo import Connection

gic = pygeoip.GeoIP('GeoIPCity.dat')
connection = Connection('localhost', 27017)
db = connection.ips
i = 0
for item in db.test.find():
    geo = gic.record_by_addr(item['_id'])
    try:
        city = geo['city'];
        latitude = geo['latitude'];
        longitude = geo['longitude'];
    except:
        print item
    if city == None:
        continue
    if latitude == None:
        continue
    if longitude == None:
        continue
    tmp = db.cities.find_one({"_id" : geo['city']})
    if tmp != None:
        tmp['number'] += 1
        db.cities.save(tmp)
    else:
        post = { "_id" : city, "number" : 1 , "latitude" : latitude, "longitude" : longitude}
        db.cities.insert(post)
    i+=1
    if i % 10000 == 0:
        print i
