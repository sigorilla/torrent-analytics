from pymongo import Connection
import bcode
import pygeoip
import math
import operator
import os.path
import sys
import json

gic = pygeoip.GeoIP('../data/GeoIPCity.dat')

file_read = open('03_ids_towns', 'r')

class Countrys:
    countrys = {}
    ids_most_popular = {}
    ids_names = {}
    def __init__(self):
        file_read = open('01_thousand_most_popular', 'r')
        i = 0
        for line in file_read:
            temp = line.split()
            self.ids_most_popular[temp[1]] = float(temp[2])
            i = i + 1
            if i > 1400:
                break;
        self.getNames()
    def addItem( self, country, id ):
        if country in self.countrys:
            if id in self.countrys[country]:
                self.countrys[country][id] = self.countrys[country][id] + 1
            else:
                self.countrys[country][id] = 1;
        else:
            self.countrys[country] = {}
            self.addItem( country = country, id = id )
    def backup(self):
        
        for country in self.countrys:
            i = 0
            
            for it in self.ids_most_popular:
                self.addItem( country , it)
                i = i + 1
                if i > 10:
                    break
            i = 0
            for id1 in self.ids_most_popular:
                self.addItem( country , id1 )
                i = i + 1
                if i > 50:
                    break
            mass = self.countrys[country]
            for id in mass:
                mass[id] = math.sqrt( float(mass[id]) ) * self.ids_most_popular[id]
            mass = sorted(mass.iteritems(), key=operator.itemgetter(1),  reverse=True )


            basepath = os.path.dirname(__file__)
            filepath = os.path.abspath(os.path.join(basepath, "..", "/data" , "/countrys", country))
            file_write = open(filepath, 'w')
            i = 0
            temp_list = []
            print self.ids_names
            for ( id1 , raiting )  in mass:
                temp = str(id1) + " " + str(raiting) + " "
                print temp
                (name1, length1) =  self.ids_names[id1]
                temp_list.append([id1, str(raiting), unicode(name1, errors='ignore'), length1])
                i = i + 1
                if i > 50:
                    break
            file_write.write(json.dumps(temp_list))
            file_write.close()
    def getNames(self):
        i = 0
        connection = Connection('144.76.168.108', 27017)
        connection.metadata.authenticate('mipt', 'mipt')
        db = connection.metadata
        print self.ids_most_popular
        for it in self.ids_most_popular :
            item = db.bcoded_metadata.find_one({"_id":it})
            item =  bcode.bdecode(item['bcoded_metadata'])
            print i
            #print self.ids_names
            i = i + 1
            #if i > 1500:
            #    break;
            try:
                self.ids_names[it] = (item['name'],str(item['piece length']))
            except:
                self.ids_names[it] = ("name","10")
            
countrys = Countrys()
for line in file_read:
    i = int( line.split()[0] )
    if ( i < 0):
        continue
    id = line.split()[1]
    country = line.split()[3]
    countrys.addItem( country = country , id = id )
file_read.close()
countrys.backup()

