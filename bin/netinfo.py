#!/usr/bin/env python

from NetworkManager import *
import pprint as pp
import ipaddress
import subprocess
import socket
import threading

class myThread (threading.Thread):
	def __init__(self, name, ip):
		threading.Thread.__init__(self)
		self.name = name
		self.ip = ip

	def ping_it(self, ip):
		try:
			out = subprocess.check_output(["ping","-c","1","-w", "2", str(ip)])
			return ip
		except subprocess.CalledProcessError:
			pass
		return None

	def run(self):
		print ("## Starting " + self.name)
		self.ans = self.ping_it(self.ip)

def get_name(nm):
	try:
		return socket.gethostbyaddr(nm)[0]
	except:
		return "Null"

def find_machines(net,netmask, exclude):
	live = []
	mynet = "%s/%s" % (net, netmask)
	network = ipaddress.ip_network(mynet, False)

	threads = []
	# fire off all threads, now
	ips = list(network.hosts())
	if (len(ips))> 255:
		print("${color8}${alignc}>>> HUGE LAN, ONLY 255 RESULTS <<<")

	for ip in ips[0:255]:
		t = myThread("Thread: " + str(ip), ip)
		threads.append(t)
		t.start()

	for t in threads:
		t.join()

		if t.ans:
			ipaddr = str(t.ans)
			if (ipaddr not in exclude):
				live.append((ipaddr, get_name(ipaddr)))
		
	return live

def wired(d):
	op = d.Dhcp4Config.Options

	if (len(op["domain_name_servers"]) < 1):
		nameservers = ["Null", "Null"]
	elif (len(op["domain_name_servers"]) < 2):
		nameservers = [op["domain_name_servers"][0], "Null"]
	else:
		nameservers = [op["domain_name_servers"][0], op["domain_name_servers"][1]]

	print("${color4}LAN:")
	print("${color2}DyIP: ${color6}%DyIP% ${alignr}%MAC%${color2} :MAC".replace("%DyIP%",op["ip_address"]).replace("%MAC%",d.HwAddress))
	print("${color2}IFACE: ${color1}%IFACE% ${alignr}%BCAST%${color2} :BCAST".replace("%IFACE%",d.Interface).replace("%BCAST%",op["broadcast_address"]))
	print("${color2}NETID: ${color1}%NETID% ${alignr}%SUBNET%${color2} :SUBNET".replace("%NETID%",op["network_number"]).replace("%SUBNET%",op["subnet_mask"]))
	print("${color2}NS1: ${color1}%NS1% ${alignr}%NS2%${color2} :NS2${color1}".replace("%NS1%",nameservers[0]).replace("%NS2%",nameservers[1]))
	print("${color2}NEXT_HOP:${color1}",d.Dhcp4Config.Options["next_server"])

	print("\n${color4}ADD INFO:")
	print("${color2}MUT: ${color1}%MUT% ${alignr}%SPEED%${color2} :SPEED".replace("%MUT%",str(d.Mtu)).replace("%SPEED%",str(d.Speed)))
	print("${color2}RXBytes:${color1} %RXBytes% ${alignr}%TxBytes%${color2} :TxBytes".replace("%RXBytes%",str(d.RxBytes)).replace('%TxBytes%', str(d.TxBytes)))


def wireless(d):
	print("\n${color2}NIEGHBORS IP${alignr}NAME")
	for ip, mach in find_machines(op["network_number"],op["subnet_mask"], [op["ip_address"]]):
		print("${color1}%IP% ${alignr}%MACH%".replace("%IP%",str(ip)).replace('%MACH%', mach))

def nocomm():
	print("${color6}${alignc}NO ACTIVE CONNECTIONS")

def ipv4_info(op, iface):
	# -------------------------------------------------------------------
	# find name servers
	if (len(op.Nameservers) < 1):
		nameservers = ["Null", "Null"]
	elif (len(op.Nameservers) < 2):
		nameservers = [op.Nameservers[0], "Null"]
	else:
		nameservers = [op.Nameservers[0], op.Nameservers[1]]    

	ip = op.AddressData[0]['address']

	print("${color2}IPv4: ${color6}%DyIP% ${alignr}%IFACE%${color2} :IFACE".replace("%DyIP%",op.AddressData[0]['address']).replace("%IFACE%", iface))
	#print("${color2}NETID: ${color1}%NETID% ${alignr}%SUBNET%${color2} :SUBNET".replace("%NETID%",op["network_number"]).replace("%SUBNET%",op["subnet_mask"]))
	print("${color2}NS1: ${color1}%NS1% ${alignr}%NS2%${color2} :NS2${color1}".replace("%NS1%",nameservers[0]).replace("%NS2%",nameservers[1]))
	print("${color2}NEXT_HOP:${color1}",op.Gateway)    
	print("\n${color2}NIEGHBORS IP${alignr}NAME")
	for ip, mach in find_machines(ip,"24", [ip]):
		print("${color1}%IP% ${alignr}%MACH%".replace("%IP%",str(ip)).replace('%MACH%', mach))


def print_access_point():
	# get device, to find access point
	aps = [ap for ap in AccessPoint.all()]
	print("${color1}${hr 1}")  
	print("${color4}Access Points (%d):" % len(aps) )
	for ap in aps:
		ssid = ap.Ssid
		if (ap.flags):
			ssid += " *"
		print("# ", ap.Ssid, ap.Strength, ap.MaxBitrate, ap.Frequency)
		print("${color2}AP: ${color1}%SSID% ${alignr}%STRENGTH%${color2} :STRENGTH${color1}"
		.replace("%SSID%",ssid).replace("%STRENGTH%","%d" % ap.Strength ))
		print("${color2}BitRate: ${color1}%BitRate% k ${alignr}%FREQ% k${color2}  :FREQUENCY${color1}"
		.replace("%BitRate%","%.0f" % (ap.MaxBitrate/1000.0)).replace("%FREQ%","%.3f" % (ap.Frequency / 1000.0)))
		print(" ")

def print_network_connections():
	# get all active connections
	active_connections = NetworkManager.ActiveConnections     
	# remove duplicate connections (like tun or vpn)
	my_conns = [conn for conn in active_connections if conn.Type not in ['tun'] ]
	connection_count = len(my_conns)  
	print("${color4}NET CONNECTIONS (%s):" % connection_count)    
	for active_conn in my_conns:
		name = active_conn.Id 
		typ = active_conn.Type         
		print("\n${color4}%s (%s):" % ( name,typ))
		ipv4_info(active_conn.Ip4Config, active_conn.Devices[0].Interface)
	return connection_count

if (print_network_connections() < 1):
	nocomm()
else:
	print_access_point()
