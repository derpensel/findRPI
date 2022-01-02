import socket
import nmap
import os, subprocess 

def checkRoot():
	ret = 0
	if os.geteuid() != 0:
		msg = "[sudo] password for %u:"
		ret = subprocess.check_call("sudo -v -p '%s'"%msg, shell=True)
	return ret

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def makeIpr(dirty):
	return(".".join(dirty.split('.')[:-1])+".1/24")
	
	

def getRPI():
	test = checkRoot()
	if test != 0:
		print("Wrong PW")
		exit()
	
	nm = nmap.PortScanner()
	nm.scan(hosts=makeIpr(getIp()),arguments="-sP")
	res = []
	for host in nm.all_hosts():
		res.append((host,list(nm[host].get('vendor').values())))
	#print(res)
	wut = []
	try:
		for o in res:
			if o[1] :
				wut.append((o[0],o[1][0]))
	except Exception:
		pass
		#print("NOT ROOT")

	rpi = []
	for fuckme in wut:
		if fuckme[1] == 'Raspberry Pi Foundation':
			rpi.append(fuckme)
			print(fuckme[0])

	return rpi

def main():
	getRPI()

if __name__ == '__main__':
    main()
