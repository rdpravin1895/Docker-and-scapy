'''This program is to generate tcp,udp and icmp packets randomly 
	and send it to localhost (ie) 127.0.0.1'''

from scapy.all import * 
import time
import threading
count=0

def tcp_proto(): #function to generate tcp packets
	while(True):
		packet = IP(dst="127.0.0.1")/TCP(dport=80)/"from scapy packet"
		send(packet)
		print "tcp sent"
		time.sleep(1)

	
def icmp_proto(): #function to generate icmp packets
	while(True):
		packet=IP(dst="127.0.0.1")/ICMP()/"Hello World"
		send(packet)
		print "icmp sent"
		time.sleep(1)



def udp_proto(): #function to generate udp packets
	while(True):
		packet=IP(dst="127.0.0.1")/UDP(sport=8888, dport=8888)/Raw(load="test")
		send(packet)
		print "udp sent"
		time.sleep(1)

		
a_thread=threading.Thread(target=tcp_proto)
a_thread.start()

b_thread=threading.Thread(target=icmp_proto)
b_thread.start()

c_thread=threading.Thread(target=udp_proto)
c_thread.start()

a_thread.join()
b_thread.join()
c_thread.join()


#pkts=[tcp_proto,icmp_proto,udp_proto] #creating a list containing the above functions for randomly generating the packets


'''while(True):
	tcp_proto()
	icmp_proto()
	udp_proto()'''
	
	#random.choice(pkts)() #packets are generated and sent randomly'''