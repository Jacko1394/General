#!/usr/bin/python3
from subprocess import check_output

def pPrint(text):
	print('\033[95m' + str(text) + '\033[0m')

def main():

	pPrint('Checking for API processes already running...')

	processes = check_output("ps aux | grep 'Magiq.Documents.AspNetCore.Api.Web.dll'", shell=True)
	
	for line in processes.splitlines():

		line = line.decode('UTF-8').rstrip()

		if 'Magiq.Documents.AspNetCore.Api.Web.dll' in line:

			if 'grep' in line:
				continue

			line = line.split()

			for bit in line:

				if bit.isdigit() and bit != 0:
					pPrint('KILLING: ' + bit)
					check_output('kill ' + bit, shell=True)
					return True

	pPrint('Nothing to kill.')
	return False

if __name__ == '__main__':
	main()
