'''This program is to analyze the protocol of incoming packet and forward 
	to the corresponding destination'''

from scapy.all import * 
import time
import docker
import json

client = docker.APIClient(base_url='unix://var/run/docker.sock')

def PacketHandler(pkt):
		
	if IP in pkt:
		#If the received packet is of TCP type, send to ip 172.18.0.2
		if TCP in pkt: 
			print pkt[IP].dst
			print pkt[IP].src
			if pkt[IP].src=='127.0.0.1':

				pkt[IP].dst='172.18.0.2'
				print pkt[IP].dst
				sendp(pkt,iface='br-7baaf397016e')
		
		#If the received packet is of ICMP type, send to ip 172.17.0.2
		elif ICMP in pkt:
			count=0
			print pkt[IP].dst
			print pkt[IP].src
			list=client.containers(all=True)
			ap='app_2' in json.dumps(list) #checking whether scaling has been done
			if pkt[IP].src=='127.0.0.1':
				
				if (ap==False): #if scaling not done, send packets to app_1
					pkt[IP].dst='172.17.0.2'
					print pkt[IP].dst
					sendp(pkt,iface='docker0')
				else:
					count+=1
					if(count%2==0):#if scaling done, send packets based on round robin method
						pkt[IP].dst='172.17.0.2'
						print pkt[IP].dst
						sendp(pkt,iface='docker0')
					
					else:
						pkt[IP].dst='172.17.0.3'
						print pkt[IP].dst
						sendp(pkt,iface='docker0')
					
		#If the received packet is of TCP type, send to ip 172.19.0.3
		elif UDP in pkt:
			print pkt[IP].dst
			print pkt[IP].src
			if pkt[IP].src=='127.0.0.1':

				pkt[IP].dst='172.19.0.3'
				print pkt[IP].dst
				sendp(pkt,iface='br-f1fa2871cb70')
			
sniff(iface='lo',prn=PacketHandler)	     #use scapy to sniff the localhost interface "lo" and perform the Packethandler function on the incoming packet
