from django.shortcuts import render
from pymongo import Connection
import bcode
import pprint
from django import template
from ipware.ip import get_ip

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    connection = Connection('144.76.168.108', 27017)
    connection.from_radars.authenticate('mipt', 'mipt')
    db = connection.from_radars
    connection.metadata.authenticate('mipt', 'mipt')
    db_data = connection.metadata
    out = []
    i = 0
    for item in db.torrents.find():
        if item['metadata_exists']:
            torr = db_data.bcoded_metadata.find_one({'_id': item['_id']})
            it = bcode.bdecode(torr['bcoded_metadata'])
            it['id'] = item['_id']
            del it['pieces']
            out.append(it)
            if i == 10:
                break
            i += 1
    client = get_ip(request)   
    context = {'get_id': out, 'ip': client}
    #pprint.pprint(out)
    return render(request, 'get/index.html', context)
# Create your views here..
