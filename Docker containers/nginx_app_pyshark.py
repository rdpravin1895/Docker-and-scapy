import docker
import time
import pyshark
import json
import ast	
import threshold
from app1_create import *
client = docker.APIClient(base_url='unix://var/run/docker.sock')

class App1_start(App1,App2):
	
	def __init__(self):
		print "contructor created for App"
		
e=App1_start()

list=client.containers(all=True)
ap1='app_1' in json.dumps(list)
print ap1

if(ap1==False):
	e.App1_method_create()
	e.App1_method_start()
else:
	print "App_1 already exists"
	
class Nginx_start(Nginx_lb):

	def __init__(self):
		print "contructor created for nginx_lb"

ngn=Nginx_start()

capture = pyshark.LiveCapture(interface="docker0")
capture.sniff(timeout=1)
count=0
pkt_count=0
th=threshold.threshold_rate
length=0
diff=0
then=time.time()

for pkt in capture:
	
	print pkt.layers
	print "Packet sent at: ",then
	if(("ICMP" in str(pkt.layers) or "IP" in str(pkt.layers)) and "IPV6" not in str(pkt.layers)):
		print "yes"
		
		if(pkt.ip.src=='127.0.0.1' and (pkt.ip.dst == '172.17.0.2' or pkt.ip.dst=='172.17.0.3')):
			count=count+1
			print "Count: ", count
			print "destination succeeded"

			length+=float(pkt.length)
			print "Packet length= ", length
			
			'''diff+=float(now-start)
			print "Time difference= ", diff
			bandwidth=float(length/diff)
			print "Bandwidth= ", bandwidth/1000'''
			print ""


			if(count==200):
				now=time.time()
				print "Packet received at :", now
				diff=int(now-then)
				print "Time= ",diff
				bandwidth=float(length/diff)
				print "Bandwidth= ",bandwidth
				
				if(bandwidth>=th):

					#print (length/count)
					print"Loadbalancing required"
					list=client.containers(all=True)
					ap='app_2' in json.dumps(list)
					print ap

					ng='nginx_lb' in json.dumps(list)
					print ng

					if(ap==False):

						e.App2_method_create()
						e.App2_method_start()

					if(ng==False):
						ngn.Nginx_method_create()
						ngn.Nginx_method_start()
						print "Loadbalancer has been created"
						print ""

				else:

					#print (length/count)
					print"Loadbalancing not required"
					print""
					list=client.containers(all=True)
					ap='app_2' in json.dumps(list)
					print ap

					ng='nginx_lb' in json.dumps(list)
					print ng

					if(ap==True):
						e.App2_method_stop()

					if(ng==True):
						ngn.Nginx_method_stop()
					
				count=0
				then=time.time()