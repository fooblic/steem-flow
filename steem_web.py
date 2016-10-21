#!/usr/bin/python
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

#import pprint
import redis
import json

'''
 Simple web-server to show data from Redis DB
'''

# template
from index_html2 import *

# config
host = "localhost"
port = 8787
key = "mkf7j65khws96gkl"
iface = "127.0.0.1"
print "http://%s:%s/%s/" % (host, port, key)

rdb = redis.Redis(host="localhost", port=6379)
#pp = pprint.PrettyPrinter(indent=4)

block_head = json.loads( rdb.get("block_head").decode() )
redis_key = "steem:%s:%s" % (block_head["start_block"], block_head["end_block"])

class Data(Resource):
    isLeaf = True
    
    def render_GET(self, request):
        read_stats = json.loads( rdb.get(redis_key).decode() )
        #pp.pprint(read_stats)
        out = str(html_all % read_stats)
        return out
                
root = Resource()
root.putChild(key, Data())

factory = Site(root)
reactor.listenTCP(port, factory, interface=iface)

reactor.run()


