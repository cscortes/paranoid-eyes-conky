#!/home/cscortes/.local/share/virtualenvs/.conky-dlbkzSpR/bin/python
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
	network = ipaddress.ip_network("{}/{}".format(net, netmask))

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
	op = d.Dhcp4Config.Options
	AP = d.ActiveAccessPoint

	if (len(op["domain_name_servers"]) < 1):
		nameservers = ["Null", "Null"]
	elif (len(op["domain_name_servers"]) < 2):
		nameservers = [op["domain_name_servers"][0], "Null"]
	else:
		nameservers = [op["domain_name_servers"][0], op["domain_name_servers"][1]]

	print("${color4}WIFI:")
	print("${color2}DyIP: ${color6}%DyIP% ${alignr}%MAC%${color2} :MAC".replace("%DyIP%",op["ip_address"]).replace("%MAC%",d.HwAddress))
	print("${color2}IFACE: ${color1}%IFACE% ${alignr}%BCAST%${color2} :BCAST".replace("%IFACE%",d.Interface).replace("%BCAST%",op["broadcast_address"]))
	print("${color2}NETID: ${color1}%NETID% ${alignr}%SUBNET%${color2} :SUBNET".replace("%NETID%",op["network_number"]).replace("%SUBNET%",op["subnet_mask"]))
	print("${color2}NS1: ${color1}%NS1% ${alignr}%NS2%${color2} :NS2${color1}".replace("%NS1%",nameservers[0]).replace("%NS2%",nameservers[1]))
	print("${color2}NEXT_HOP:${color1}",d.Dhcp4Config.Options["next_server"])

	print("\n${color4}ACCESS POINT:")
	print("${color2}SSID: ${color6}%SSID% ${color1}${alignr}%MAC%${color2} :MAC".replace("%SSID%",AP.Ssid).replace("%MAC%",AP.HwAddress))
	print("${color2}STRENGTH:${color1} %STRENGTH% ${alignr}%FREQ%${color2} :FREQ".replace("%STRENGTH%",str(AP.Strength)).replace('%FREQ%', str(AP.Frequency/1000)))
	print("${color2}MAXBITRATE:${color1}", AP.MaxBitrate/1000)

	print("\n${color2}NIEGHBORS IP${alignr}NAME")
	for ip, mach in find_machines(op["network_number"],op["subnet_mask"], [op["ip_address"]]):
		print("${color1}%IP% ${alignr}%MACH%".replace("%IP%",str(ip)).replace('%MACH%', mach))

# wireless_devices = [d for d in devices if type(d) == Wireless]
# wired_devices = [d for d in devices if type(d) == Wired]
# print(wireless_devices)
# print(wired_devices)

def nocomm():
	print("${color6}${alignc}NO INTERNET CONNECTION")


# get all the devices
devices = NetworkManager.GetAllDevices()

bFound = False

for d in devices:
	if type(d) == Wireless:
		if d.ActiveConnection != None:
			if (bFound):
				print("${color1}${hr 1}")
			wireless(d)
			bFound = True

	if type(d) == Wired:
		if d.ActiveConnection != None:
			if (bFound):
				print("${color1}${hr 1}")
			wired(d)
			bFound = True

if (not bFound):
	nocomm()

