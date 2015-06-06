#!/usr/bin/env python

"""publicip.py: A simple Public IP Display Tool"""

__author__      = "Oliver Vivell"
__copyright__   = "Copyright 2015"
__license__ 	= "MIT"
__version__ 	= "1.0"
__maintainer__ 	= "Oliver Vivell"
__email__ 		= "oliver@badfoc.us"
__status__ 		= "Production"

import sys, re, os
from bs4 import BeautifulSoup
import urllib2  
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PublicIP:
	refreshed = 0

	def __init__(self):

		self.response = self.requestPage()
		self.ip = self.requestIP()
		self.city = ""
		self.isp = ""
		self.state = ""
		self.country = ""
		self.proxy = ""
		self.refresh = self.refresh()
		PublicIP.refreshed += 1
		self.parseParameters()

	def parseParameters(self):
		params = ["the-proxy","the-city", "the-isp", "the-state", "the-country"]
		value = []
		for param in params:
			for span in self.response.find('div', param):
				value.append(span)
		
		self.proxy = str(value[0]).title()
		self.city = str(value[1]).title()
		self.isp = str(value[2]).title()
		self.state = str(value[3]).title()
		self.country = str(value[4]).upper()[:2]
	
		return self

	def requestPage(self):
		req = urllib2.Request('http://www.whatismyip.com', headers={'User-Agent':'Mozilla/5.0'})
		response = urllib2.urlopen(req, timeout=5)
		self.response = BeautifulSoup(response)
		return self.response

	def requestIP(self):
		self.ip = urllib2.urlopen('http://ip.42.pl/raw').read()
		return self.ip

	def showIP(self):
		print "[%s+%s] Public IP: %s %s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.WARNING, self.ip, bcolors.ENDC)
	
	def showISP(self):
		print "[%s+%s] ISP: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.OKBLUE, self.isp, bcolors.ENDC)

	def showCity(self):
		print "[%s+%s] City: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.OKBLUE, self.city, bcolors.ENDC)

	def showState(self):
		print "[%s+%s] State: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.OKBLUE, self.state, bcolors.ENDC)

	def showCountry(self):
		print "[%s+%s] Country: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.OKBLUE, self.country, bcolors.ENDC)
	
	def showProxy(self):
		print "[%s+%s] Proxy: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.WARNING, self.proxy, bcolors.ENDC)


	def displayAll(self):
		self.showIP()
		self.showISP()
		self.showCity()
		self.showState()
		self.showCountry()
		self.showProxy()
		

	def refresh(self):
		return 5

def Main():
	os.system('clear')
	myIP = PublicIP()
	myIP.displayAll()

if __name__ == "__main__":
	Main()