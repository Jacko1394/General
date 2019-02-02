#!/usr/bin/python3
import os.path
import datetime
import time
import subprocess
import re
import json
import gist
import requests

# Configs:
transSettings = '/etc/transmission-daemon/settings.json'
gistDirectory = '/home/xxx/ffc8ffec35c242f113a1ca1e86e43b53'
pwd = 'birdie133'
drivePath = '/media/HD'
hdDisk = '/dev/sdb2'
torrentPath = drivePath + '/Downloads'

# Globals:
public = ''
local = ''
port = ''
output = ''

def pPrint(text):
	print('\033[95m' + str(text) + '\033[0m')
	global output
	output += text + '\n'

def main():

	initialize()
	runUpdates()
	# installSoftware()

	if not mountDrive():
		return False

	getPortForward()
	updateTransmissionSettings()
	checkIpAdresses()
	updateGist()
	startNgrok()

	return True

def test():

	#Open, load config:
	f1 = open('/home/xxx/test.txt', 'r+')
	f1.write('ok')
	f1.close()

def initialize():

	status = False
	
	pPrint('Initialising...')

	while not status:
		os.system('echo %s|sudo -S %s' % (pwd, 'systemctl stop openvpn@vpn.service'))
		os.system('echo %s|sudo -S %s' % (pwd, 'service transmission-daemon stop'))
		#reset network here:::
		time.sleep(5)
		status = verifyInternet()
		if status:
			break

	#stop vpn, wait 10, check internet 3 times, waiting 10 inbetween
	#reboot

def verifyInternet():

	try:
		result = requests.head('http://www.google.com/', timeout=8)

		if 200 <= result.status_code <= 226:
			pPrint('Internet success code: ' + str(result.status_code))
			return True
		else:
			pPrint('Error: ' + result)
			return False

	except:
		pPrint('Error: Network not working!')
		return False

def runUpdates():

	pPrint('Updating packages (apt-get)...')

	#Updates: -y is assume Yes:
	os.system('echo %s|sudo -S %s' % (pwd, 'apt-get -y update'))
	os.system('echo %s|sudo -S %s' % (pwd, 'apt-get -y full-upgrade'))

def installSoftware():

	pPrint('Installing software...')

	#Installs:
	pPrint('Installing git...')
	os.system('echo %s|sudo -S %s' % (pwd, 'apt-get install -y git'))

	pPrint('Installing transmission...')
	os.system('echo %s|sudo -S %s' % (pwd, 'apt-get install -y git'))

def mountDrive():

	result = False

	pPrint('Mounting hard drive...')

	if os.path.ismount(drivePath):
		pPrint('Drive is mounted: ' + drivePath)
		result = True
	else:
		if os.system('echo %s|sudo -S %s' % (pwd, 'mount ' + hdDisk + ' ' + drivePath)):
			result = False
		else:
			pPrint('Successfully mounted drive: ' + drivePath)
			result = True
	
	if not result:
		pPrint('Error mounting drive :(\nMight not be plugged in?)')
		os.system('echo %s|sudo -S %s' % (pwd, 'systemctl stop openvpn@vpn.service'))
		os.system('echo %s|sudo -S %s' % (pwd, 'service transmission-daemon stop'))
		result = False

	return result

def getPortForward():

	global port

	pPrint('Getting port forward...')
	os.system('echo %s|sudo -S %s' % (pwd, 'systemctl restart openvpn@vpn.service'))
	time.sleep(5)

	try:
		port = subprocess.check_output('head -n 100 /dev/urandom | sha256sum | tr -d " -"', shell=True)
		port = port.decode('UTF-8').rstrip()
		port = subprocess.check_output('curl -m 8 "http://209.222.18.222:2000/?client_id=%s"' % (port), shell=True, close_fds=True, stdin=None, stderr=None)
		port = port.decode('UTF-8').rstrip()
	except:
		return False

	port = re.findall(r'\d+', port)[0]
	pPrint('PORT: ' + port)
	return True

def updateTransmissionSettings():

	global port

	pPrint('Updating transmission configuration...')

	#Restart the transmission-daemon service, and wait:
	os.system('echo %s|sudo -S %s' % (pwd, 'service transmission-daemon stop'))
	os.system('echo %s|sudo -S %s' % (pwd, 'service transmission-daemon start'))
	time.sleep(5)

	#Change permissions of settings.json so python can modify it:
	os.system('echo %s|sudo -S %s' % (pwd, 'chown xxx -R %s' % (transSettings)))

	#Open, load config:
	f1 = open(transSettings, 'r+')
	data = json.load(f1)

	#Change values:
	data['rpc-port'] = int(port)
	data['rpc-whitelist-enabled'] = False
	data['rpc-authentication-required'] = True
	data['rpc-username'] = 'jacko1394'
	data['rpc-password'] = 'pelican420'
	data['incomplete-dir'] = torrentPath
	data['download-dir'] = torrentPath

	#Save 
	f1.seek(0)
	f1.write(json.dumps(data))
	f1.truncate()
	f1.close()

	#Reset settings.json permissions, reload configuration:
	os.system('echo %s|sudo -S %s' % (pwd, 'chown debian-transmission -R %s' % (transSettings)))
	os.system('echo %s|sudo -S %s' % (pwd, 'service transmission-daemon reload'))
	return 0

def checkIpAdresses():

	global public
	global local

	pPrint('Checking IP addresses...')

	public = subprocess.check_output('curl -m 8 ipinfo.io/ip', shell=True, close_fds=True, stdin=None, stderr=None)
	public = public.decode('UTF-8').rstrip()
	pPrint('Public IP: ' + public)

	local = subprocess.check_output('/sbin/ifconfig | grep 192.168', shell=True, cwd='/home/xxx')
	local = local.decode('UTF-8').rstrip()
	local = re.search('inet (.*) netmask', local)
	local = str(local.group(1)).rstrip()
	pPrint('Local IP: ' + local)

	return True

def updateGist():

	global public
	global local
	global port

	pPrint('Updating Gist link.txt...')

	# Loads data:
	f1 = open(gistDirectory + '/link.txt', 'r+')
	f2 = open('/home/xxx/cronn.log', 'r')
	
	date = subprocess.check_output('date', shell=True)
	date = date.decode('UTF-8').rstrip()
	uname = subprocess.check_output('uname -a', shell=True)
	uname = uname.decode('UTF-8').rstrip()
	drives = subprocess.check_output('df -h | grep /dev/sd', shell=True)
	drives = drives.decode('UTF-8').rstrip()

	# Writes data:
	f1.seek(0)
	f1.write('SYSTEM:\n' + uname + '\n\nTIME:\n')
	f1.write(datetime.datetime.now().strftime('%-d/%-m/%Y %A %-I:%M%p') + '\n')
	f1.write(date + '\n\n')
	f1.write('DRIVES:\nFilesystem      Size  Used Avail Use% Mounted on\n')
	f1.write(drives + '\n\n')
	f1.write('URL:\n' + public + ':' + port + '\n')
	f1.write(local + ':' + port + '\n\nOUTPUT:\n' + output) # + '\nCRON LOG:\n')
	# f1.write(f2.read()) # cron log

	# Finalise:
	f1.truncate()
	f1.close()

	# Save changes to gist repo:
	r1 = subprocess.check_output('git add -A && git commit -m "xxx"', cwd=gistDirectory, shell=True)
	r1 = subprocess.check_output('git push origin master', cwd=gistDirectory, shell=True)
	pPrint('Updated Gist repo.')

	return 0

def startNgrok():

	pPrint('Starting ngrok connection...')
	r1 = subprocess.check_output('/home/xxx/ngrok tcp 22', shell=True, stdin=None, stderr=None, close_fds=True)

if __name__ == '__main__':
	main()
