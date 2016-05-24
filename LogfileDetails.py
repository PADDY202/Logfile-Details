#!/usr/bin/env python3
#Padraig Mitchell
#proggamme works by parsing the log file, and uses the classes hosts and vist to store parsed data
#the ips dict is the core structure for all the iformation relating to the ips and their vists to the site
# The class FixedOffset is just used for parsing the the time
import re
import sys
import host
import vist
from datetime import datetime, tzinfo, timedelta

class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, string):
        #import pudb ; pudb.set_trace()
        if string[0] == '-':
            direction = -1
            string = string[1:]
        elif string[0] == '+':
            direction = +1
            string = string[1:]
        else:
            direction = +1
            string = string

        hr_offset = int(string[0:2], 10)
        min_offset = int(string[2:3], 10)
        min_offset = hr_offset * 60 + min_offset
        min_offset = direction * min_offset

        self.__offset = timedelta(minutes = min_offset)

        self.__name = string

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return timedelta(0)

    def __repr__(self):
        return repr(self.__name)

ips = {}# dict of ip addresses to matching host obj's
if (len(sys.argv) >1):
	if (sys.argv[1] == "-l"):
		file = sys.argv[2]
else:
	print ("Yo need 2 arguments to read in file -l and file name")
	
month_map = {'Jan': 1, 'Feb': 2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7,
        'Aug':8,  'Sep': 9, 'Oct':10, 'Nov': 11, 'Dec': 12}
parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]

pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')
with open(file, 'r') as content_file:
    content = content_file.read()

content = content.splitlines()
for i, val in enumerate(content):
	m = pattern.match(val)
	res = m.groupdict()
	if res["host"] in ips:
		ips.get(res["host"]).request_count += 1
		s=res["time"]
		tz_string = s[21:26]
		tz = FixedOffset(tz_string)
		v=vist.Vist(datetime(year=int(s[7:11]), month=month_map[s[3:6]], day=int(s[0:2]), hour=int(s[12:14]), minute=int(s[15:17]), second=int(s[18:20]), tzinfo=tz ), res["request"])		
		ips.get(res["host"]).vists.append(v)
	else:
		ips[res["host"]]=(host.Host(res["host"]))
		s=res["time"]
		tz_string = s[21:26]
		tz = FixedOffset(tz_string)
		v=vist.Vist(datetime(year=int(s[7:11]), month=month_map[s[3:6]], day=int(s[0:2]), hour=int(s[12:14]), minute=int(s[15:17]), second=int(s[18:20]), tzinfo=tz ), res["request"])		
		ips.get(res["host"]).vists.append(v)
		
vals = list(ips.values())
vals.sort(key=lambda x: x.request_count, reverse=True)#sorted by most requests
if (len(sys.argv) > 3):	
	if (sys.argv[3] == "-n"):
			print(len(ips)); 	#prints the number of unique hosts in the log
if (len(sys.argv) > 4):	
	if (sys.argv[3] == "-t"):
		n = int(sys.argv[4])
		for i in range(0,n):
			print(vals[i].name,"\t",len(vals[i].vists))		#the most requesting host
	if (sys.argv[3] == "-v"):
		ip = sys.argv[4]
		print(ips[ip].count_vists())	# get each vist >1 hour by adding a method to host that goes through each time and see's if its with in a huour of the previous if so deduct 1 from overall requests
	if (sys.argv[3] == "-L"):
		ip = sys.argv[4]
		for i, val in enumerate (ips[ip].vists): #each request for a given IP
		   print(val.request)
	if (sys.argv[3] == "-d"):
		date = sys.argv[4]
		for i, val in enumerate (vals):
			print( val.name,"\t",val.count_req_date(date))
