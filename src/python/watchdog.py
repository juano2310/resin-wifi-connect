#!/usr/bin/python
# coding=UTF-8

print "Starting Infinite Gateway Watchdog"

import os,string,time

try:
	import daemon
except ImportError:
    print "Error: You need to install python-daemon extension for Python"
    print "$ sudo wget http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg#md5=fe1f997bc722265116870bc7919059ea"
    print "sudo sh setuptools-0.6c11-py2.7.egg"
    print "rm setuptools-0.6c11-py2.7.egg"
    print "sudo wget http://pypi.python.org/packages/source/p/python-daemon/python-daemon-1.5.5.tar.gz"
    print "sudo tar zxvf python-daemon-1.5.5.tar.gz$ cd python-daemon-1.5.5"
    print "sudo python setup.py install"
    sys.exit(1)

with daemon.DaemonContext():

	while True:
		sensors = 0
		actions = 0
		conditions = 0
		halt = 0
		value = 0
		pids= [pid for pid in os.listdir('/proc') if pid.isdigit()]
		
		for pid in pids:
			try:
				value = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
			except:
				value = "" 
			if string.find(value,"conditions.py") >= 0:
				conditions = 1  
				 	
		if conditions == 0:
		 	os.system('python /var/garagedoor/conditions.py') 	
		 	time.sleep(5)
