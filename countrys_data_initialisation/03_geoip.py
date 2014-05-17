import pygeoip
gic = pygeoip.GeoIP('../data/GeoIPCity.dat')


file_read = open('02_ips_most_popular', 'r')
file_write = open('03_ids_towns', 'w')

for line in file_read:
    i = int( line.split()[0] )
    if ( i < 0):
        continue
    try:
        id = line.split()[1]
        ip = line.split()[2]
        geo = gic.record_by_addr(ip)
        temp = str(i)+ ' ' + str(id) + ' ' + str(ip) + ' ' + geo['country_name'] + ' ' + geo['city'] + ' ' + str(geo['latitude']) + ' ' + str(geo['longitude'])
        file_write.write(temp + '\n')
        print temp
    except:
        print str(i)
file_read.close()
file_write.close()