#!/usr/bin/python
'''
 Simple web-server to show data from Redis DB
'''
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

import pprint
import redis
import json
import yaml

from jinja2 import Template

# template
from index_html2 import *

# config
my_config = yaml.load(open("steemapi.yml"))
log = my_config['log']
prefix = my_config["prefix"]
last_info = my_config["last_info"]
blocks_list = my_config["blocks_list"]

host = "localhost"
port = 8787
key = "steem"
iface = "127.0.0.1"

url = "http://%s:%s/%s/" % (host, port, key)
print url

rdb = redis.Redis(host="localhost", port=6379)
pp = pprint.PrettyPrinter(indent=4)

template = Template(html_slots)

class Last(Resource):
    isLeaf = True
    
    def render_GET(self, request):
        block_head = json.loads( rdb.get(prefix + last_info).decode() ) # from last steem-flow2.py start
        redis_key = "%s%s:%s" % (prefix, block_head["start_block"], block_head["end_block"])
        read_stats = json.loads( rdb.get(redis_key).decode() )
        #pp.pprint(read_stats)
        out = str(html_all % read_stats)
        return out

class Slots(Resource):
    isLeaf = True
    
    def render_GET(self, request):
        redis_keys = rdb.zrange(prefix + blocks_list, 0, -1) # list all items
        out = template.render(http = "http://%s:%s/%s" % (host, port, key + "slot/") , items = redis_keys)
        return str(out)

class Slot(Resource):
    isLeaf = True
    
    def render_GET(self, request):
        redis_key = request.postpath[0]
        try:
            read_stats = json.loads( rdb.get(redis_key).decode() )
            #pp.pprint(read_stats)
            out = html_all % read_stats
        except:
            out = ""

        return str(out)
                
root = Resource()
root.putChild(key, Last()) # last slot
root.putChild(key + "slots", Slots()) # slot list
root.putChild(key + "slot", Slot()) # some slot


factory = Site(root)
reactor.listenTCP(port, factory, interface=iface)

reactor.run()


