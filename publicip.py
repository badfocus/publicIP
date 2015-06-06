#!/usr/bin/env python

"""publicip.py: A simple Public IP Display Tool"""

__author__      = "Oliver Vivell"
__copyright__   = "(c) June, 2015"
__license__ 	= "MIT"
__version__ 	= "1.0.2"
__email__ 	= "oliver@badfoc.us"
__status__ 	= "Production"

import sys, os
from bs4 import BeautifulSoup
import urllib2  
import argparse

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

	def showIP(self, verbose):
		if verbose:
			print "[%s+%s] Public IP: %s %s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.WARNING, self.ip, bcolors.ENDC)
		else:
			print self.ip 

	def showISP(self, verbose):
		if verbose:
			print "[%s+%s] ISP: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.OKBLUE, self.isp, bcolors.ENDC)
		else:
			print self.isp

	def showCity(self, verbose):
		if verbose:
			print "[%s+%s] City: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.OKBLUE, self.city, bcolors.ENDC)
		else:
			print self.city

	def showState(self, verbose):
		if verbose:
			print "[%s+%s] State: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.OKBLUE, self.state, bcolors.ENDC)
		else:
			print self.state

	def showCountry(self, verbose):
		if verbose:
			print "[%s+%s] Country: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.OKBLUE, self.country, bcolors.ENDC)
		else:
			print self.country

	def showProxy(self, verbose):
		if verbose:
			print "[%s+%s] Proxy: %s \t%s %s" % (bcolors.OKGREEN, bcolors.ENDC,bcolors.WARNING, self.proxy, bcolors.ENDC)
		else: 
			print self.proxy

	def displayAll(self, verbose):
		self.showIP(verbose)
		self.showISP(verbose)
		self.showCity(verbose)
		self.showState(verbose)
		self.showCountry(verbose)
		self.showProxy(verbose)

	def refresh(self):
		return 5

def Main():
	
	parser = argparse.ArgumentParser(description='%(prog)s: Simple utility to display public ip address')
	parser.add_argument('-I', "--ip",action='store_true',dest='ip',help="Display Public IP address")
	parser.add_argument("-i", "--isp",action='store_true',dest='isp',help="Display ISP name")
	parser.add_argument("-s", "--state",action='store_true',dest='state',help="Display ISP State")
	parser.add_argument("-c", "--city",action='store_true',dest='city',help="Display ISP City")
	parser.add_argument("-C", "--country",action='store_true',dest='country',help="Display ISP Country")
	parser.add_argument("-p", "--proxy",action='store_true',dest='proxy',help="Display Proxy")
	parser.add_argument("-a", "--all",action='store_true',dest='all',help="Display all information")
	parser.add_argument("-v", "--verbose",action='store_true',dest='verbose',help="Display verbose information")
	parser.add_argument("-b", "--clear",action='store_true',dest='clear',help="Clear screen before displaying information")
	parser.add_argument('--version', action='version', version='%(prog)s Version ' + __version__)

	args = parser.parse_args()

	if args.ip or args.isp or args.state or args.city or args.proxy or args.all:
		myIP = PublicIP()
		if args.clear:
			os.system('clear')
		if args.ip:
			myIP.showIP(args.verbose)
		if args.isp:
			myIP.showISP(args.verbose)
		if args.state:
			myIP.showState(args.verbose)
		if args.city:
			myIP.showCity(args.verbose)
		if args.country:
			myIP.showCountry(args.verbose)
		if args.proxy:
			myIP.showProxy(args.verbose)
		if args.all:
			myIP.displayAll(args.verbose)
	else:
		print bcolors.FAIL + "Error: " + bcolors.ENDC + "Please provide one of the folloing arguments"
		parser.print_help()		


if __name__ == "__main__":
	Main()