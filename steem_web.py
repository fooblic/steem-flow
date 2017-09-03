#!/usr/bin/python
'''
 Simple web-server to show data from Redis DB
'''
import pprint
import json

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

import redis
import yaml
from jinja2 import Template

# template
from index_html2 import html_slots, html_all, html_up, template_out
from get_redis import get_slot_dates

# config
my_config = yaml.load(open("./steem_flow/steemapi.yml"))
log         = my_config['log']
prefix      = my_config["prefix"]
last_info   = my_config["last_info"]
blocks_list = my_config["blocks_list"]

host  = my_config["host"]
port  = my_config["port"]
key   = my_config["key"]
iface = my_config["iface"]

url = "http://%s:%s/%s/" % (host, port, key)
print url

rdb = redis.Redis(host=my_config["redis_host"], port=my_config["redis_port"])
pp = pprint.PrettyPrinter(indent=4)

template = Template(html_slots)
templ_up = Template(html_up)

class Last(Resource):
    isLeaf = True

    def render_GET(self, request):
        '''Display last slot data'''
        block_head = json.loads( rdb.get(prefix + last_info).decode() ) # from last steem-flow2.py start
        redis_key = "%s%s:%s" % (prefix, block_head["start_block"], block_head["end_block"])
        read_stats = json.loads( rdb.get(redis_key).decode() )
        #pp.pprint(read_stats)
        out = str(html_all % read_stats)
        return out

class Slots(Resource):
    isLeaf = True

    def render_GET(self, request):
        '''Get a list of all slots with dates from the end'''
        redis_keys = rdb.zrange(prefix + blocks_list, 0, -1) # list all items

        slot_dates = []
        for each in redis_keys[::-1]:  # from the list end
            slot_dates.append( get_slot_dates(rdb, each) )

        out = template.render(http="http://%s:%s/%s" % (host, port, key + "slot/"),
                              items=redis_keys[::-1],
                              dates=slot_dates)
        return str(out)

class Slot(Resource):
    isLeaf = True

    def render_GET(self, request):
        '''Display given slot data'''
        redis_key = request.postpath[0]
        try:
            read_stats = json.loads( rdb.get(redis_key).decode() )
            #pp.pprint(read_stats)
            #out = html_all % read_stats
            out = str(template_out % read_stats)
        except:
            out = ""

        return str(out)

class Upvote(Resource):
    isLeaf = True

    def render_GET(self, request):
        '''Display a list of all upvoted items from the end'''
        redis_keys = rdb.zrange("steembot:upvoted", 0, -1) # list all items

        post_dates = []
        post_urls = []
        for post in redis_keys[::-1]:  # from the list end
            item = json.loads(rdb.get(post).decode())

            post_dates.append("%s - @%s/%s" % (item["time"],
                                               item["author"],
                                               item["parent_permlink"]))

            post_urls.append("https://steemit.com/%s/@%s/%s" % (item['parent_permlink'],
                                               item['author'],
                                               item['permlink']))

        out = templ_up.render(http="http://%s:%s/%s" % (host, port, "post/"),
                                  items=redis_keys[::-1],
                                  tup_urls=zip(post_dates, post_urls))
                                 # dates=post_dates,
                                #  urls=post_urls)
        #print out

        return str(out)

class Vote(Resource):
    isLeaf = True

    def render_GET(self, request):
        redis_keys = rdb.zrange("steembot:index", 0, -1) # list all items
        out = template.render(http = "http://%s:%s/%s" % (host, port, "post/") , items = redis_keys)
        return str(out)

class Post(Resource):
    isLeaf = True

    def render_GET(self, request):
        redis_key = request.postpath[0]
        try:
            read_stats = json.loads( rdb.get(redis_key).decode() )
            #pp.pprint(read_stats)
            url = "https://steemit.com/%s/@%s/%s" % (read_stats['parent_permlink'],
                                                     read_stats['author'],
                                                     read_stats['permlink'])

            out = u'''<html><head><meta content="text/html; charset=utf-8" http-equiv="content-type"></head><body>
author: %s <br>
tag: %s <br>
link: %s <br>
time: %s <br>
title: %s <br>
tags: %s <br>
<a href="%s"> -> </a>
</body></html>'''.encode('utf-8') % (read_stats['author'],
                read_stats['parent_permlink'],
                read_stats['permlink'],
                read_stats['time'],
                read_stats['title'],
                str(json.loads(read_stats['json_metadata'])['tags']),
                url)

            #out = pp.pformat(read_stats)
        except:
            out = ""

        return out.encode('ascii', 'ignore')


root = Resource()
root.putChild(key, Last()) # last slot
root.putChild(key + "slots", Slots()) # slot list
root.putChild(key + "slot", Slot()) # some slot

root.putChild("upvoted", Upvote())  # upvoted posts list
root.putChild("vote", Vote())  # Vote list
root.putChild("post", Post())

factory = Site(root)
reactor.listenTCP(port, factory, interface=iface)

reactor.run()

