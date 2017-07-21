'''This program is to generate tcp,udp and icmp packets randomly 
	and send it to localhost (ie) 127.0.0.1'''

from scapy.all import * 
import time
count=0

def tcp_proto(): #function to generate tcp packets
	packet = IP(dst="127.0.0.1")/TCP(dport=80)/"from scapy packet"
	send(packet)
	print "tcp sent"
	
	
def icmp_proto(): #function to generate icmp packets
	packet=IP(dst="127.0.0.1")/ICMP()/"Hello World"
	send(packet)
	print "icmp sent"

def udp_proto(): #function to generate udp packets
	packet=IP(dst="127.0.0.1")/UDP(sport=8888, dport=8888)/Raw(load="test")
	send(packet)
	print "udp sent"

pkts=[tcp_proto,icmp_proto,udp_proto] #creating a list containing the above functions for randomly generating the packets


while(True):
	'''tcp_proto()
	icmp_proto()
	udp_proto()'''
	
	random.choice(pkts)() #packets are generated and sent randomly