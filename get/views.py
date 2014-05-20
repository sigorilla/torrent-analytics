from django.shortcuts import render
from pymongo import Connection
import bcode
import pprint
import json
import re
from django import template
from ipware.ip import get_ip
import pygeoip
import unicodedata

countries = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anonymous Proxy', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Chad', 'Chile', 'China', 'Colombia', 'Congo', 'Congo, The Democratic Republic of the', 'Costa Rica', "Cote D'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Europe', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palestinian Territory', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'San Marino', 'Satellite Provider', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Yemen', 'Zambia', 'Zimbabwe']

def compromatFunction(ip):
    connection1 = Connection('127.0.0.1', 27017)
    db1 = connection1.ips
    
    temp = db1.test.find_one({ "_id" : ip })
    if temp == None:
        return []
    #print temp
    connection2 = Connection('144.76.168.108', 27017)
    connection2.metadata.authenticate('mipt', 'mipt')
    db2 = connection2.metadata
    
    item = db2.bcoded_metadata.find({"_id" : { "$in" :temp['hashes'][:15]}})
    if item == None:
        return []
    temp = []
    for it in item:
        meta = bcode.bdecode(it['bcoded_metadata'])
        if meta['name'].strip() != "" and meta['name'] is not(None):
            temp.append([ it["_id"], meta['name'] ])
    return temp


def index(request):
	if request.method == 'POST':
		client = request.POST.get('ip', None)
	else:
		client = get_ip(request)
	gic = pygeoip.GeoIP("/home/paul/mhack/GeoIPCity.dat")
	geo = gic.record_by_addr(client)
	try:
		country = '/home/paul/prison/countries/' + geo['country_name']
	except:
		country = '/home/paul/prison/countries/Russian Federation'
	json_data = open(country)
	data = json.load(json_data)
	json_data.close()

	k = 1
	for dat in data:
		dat[2] = dat[2].encode("ISO-8859-1")
		dat[3] = k
		k += 1
	
	connection = Connection('127.0.0.1', 27017)
	db_data = connection.ips
	out = []
	cities = db_data.cities.find().sort('number', -1).limit(200)
	#pprint.pprint(cities)	
	try:
		g = (geo['latitude'], geo['longitude'])
	except:
		g = (55.76, 37.64)
	cc = "<script> var myMap; ymaps.ready(init); function init () { myMap = new ymaps.Map('map', {center: [ " + str(g[0]) + ", " + str(g[1]) + "], zoom: 5});"

	finish = "} </script>"

	for city in cities:
		city['id'] = unicodedata.normalize('NFKD', city['_id']).encode('ascii','ignore')
		del city['_id']
		cc += "var " + re.sub(r'^[a-zA-Z0-9]$', "", str(city['id']).replace(" ", "").replace("-", ""))  + " = new ymaps.Circle([ [" + str(city['latitude']) + ", " + str(city['longitude']) + "], Math.sqrt(" + str(city['number']) + " )*500 + 200], { balloonContent: '" + str(city['id']) + "'}, { fillColor: '#DB709377', strokeColor: '#990066', strokeOpacity: 0.8, strokeWidth: 3 }); myMap.geoObjects.add(" + re.sub(r'^[a-zA-Z0-9]$', "", str(city['id']).replace(" ", "").replace("-", "")) + ");"
	cc += finish
	

	#pprint.pprint(data)
	context = {'get_id': data, 'ip': client, 'geo': g, 'cities': cities, 'text': cc, 'countries': countries, 'this': 'Russian Federation', }
	return render(request, 'index.html', context)

def history(request):    

	connect = Connection('127.0.0.1', 27017)
	db = connect.ips
	if request.method == 'POST':
		ip = request.POST.get('ip', None)
		country = request.POST.get('country', None)
	else:
		ip = get_ip(request)
		gic = pygeoip.GeoIP("/home/paul/mhack/GeoIPCity.dat")
		geo = gic.record_by_addr(ip)
		try:
			country = geo['country']
		except:
			country = 'Russian Federation'

	if country is None:
		country = 'Russian Federation'
	if ip is None:
		ip = get_ip(request)

	path = '/home/paul/prison/countries/' + country
	json_countr = open(path)
	data = json.load(json_countr)
	json_countr.close()

	for dat in data:
		dat[2] = dat[2].encode("ISO-8859-1")
		
	out = compromatFunction(ip)
	context = {'hist_data': out, 'ip': ip, 'countries': countries, 'top': data, 'this': country, }
	return render(request, 'history.html', context)

def analytics(request):
	path1 = "image/figure_1.png"
	path2 = "image/figure_2.png"
	context = {'path1': path1, 'path2': path2, }
	return render(request, 'analytics.html', context)	

def about(request):
	return render(request, 'about.html')
