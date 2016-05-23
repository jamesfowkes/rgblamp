from functools import partial

import requests

import logging
import datetime

def get_logger():
    return logging.getLogger(__name__)
 
class HTTPAlarmDataProvider:

	def __init__(self, url):
		self.url = url

	def get_time(self, n):
	    resp = requests.get("%salarm/%d/time" % (self.url, n))
	    time_str = resp.json()['time']
	    time = datetime.datetime.strptime(time_str, "%H:%M").time()
	    get_logger().info("Got time for alarm 1: %s", time_str)
	    return time
