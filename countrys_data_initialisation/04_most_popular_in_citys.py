from pymongo import Connection
import bcode
import math
import operator
import os.path
import sys
import json
import pygeoip
gic = pygeoip.GeoIP('../data/GeoIPCity.dat')

file_read = open('02_ips_most_popular', 'r')

class Countries:
    countries = {}
    ids_most_popular = {}
    ids_names = {}
    def __init__(self):
        file_read = open('01_thousand_most_popular', 'r')
        i = 0
        data = json.load(file_read)
        for line in data:
            self.ids_most_popular[line[1]] = line[2]
        self.getNames()
    def addItem( self, country, id ):
        if country in self.countries:
            if id in self.countries[country]:
                self.countries[country][id] = self.countries[country][id] + 1
            else:
                self.countries[country][id] = 1;
        else:
            self.countries[country] = {}
            self.addItem( country = country, id = id )
    def backup(self):
        
        for country in self.countries:
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
            mass = self.countries[country]
            for id in mass:
                mass[id] = mass[id] * self.ids_most_popular[id]
            mass = sorted(mass.iteritems(), key=operator.itemgetter(1),  reverse=True )


            basepath = os.path.dirname(__file__)
            try:
                filepath = os.path.abspath(os.path.join(basepath, "../countries", country))
                file_write = open(filepath, 'w')
                i = 0
                temp_list = []
                for ( id1 , raiting )  in mass:
                    temp = str(id1) + " " + str(raiting) + " "
                    (name1, length1) =  self.ids_names[id1]
                    temp_list.append([id1, str(raiting), name1, length1])
                    i = i + 1
                    if i > 50:
                        break
                file_write.write(json.dumps(temp_list))
                file_write.close()
            except :
                print "Exception in Countries -> backup -> saving"
    def getNames(self):
        json_data = open("01_thousand_most_popular", "r")
        data = json.load(json_data)
        for it in data :
            print it[0]
            try:
                self.ids_names[it[1]] = (it[3],it[4])
            except:
                self.ids_names[it[1]] = ("name","10")
            
countries = Countries()
for line in file_read:
    i = int( line.split()[0] )
    if ( i < 0):
        continue
    id = line.split()[1]
    ip = line.split()[2]
    country = 0
    try:
        geo = gic.record_by_addr(ip)
        country = geo['country_name']
    except:
        continue
    countries.addItem( country = country , id = id )
file_read.close()
countries.backup()

