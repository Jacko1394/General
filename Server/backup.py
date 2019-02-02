#!/usr/bin/python3
import sys
import os.path
import subprocess

gitDir = '/media/HD'
outputFile = '/home/xxx/output.txt'

def pPrint(text):
	print('\033[95m' + str(text) + '\033[0m')


def main():

	# Checks if a directory was specified in the command line call:
	if len(sys.argv) > 1:
		global gitDir
		gitDir = str(sys.argv[1])


	pPrint('Checking sizes...')

	list = os.listdir(gitDir)

	pPrint('Directory: ' + gitDir)

	pPrint(list)
	pPrint('Directory count: ' + str(len(list)))
	pPrint('\n----------------')

	rezip = False

	r1 = subprocess.check_output('du -hs ./*', shell=True, cwd=gitDir)
	r1 = r1.decode('UTF-8').rstrip()
	pPrint(r1)

	pPrint('----------------')

	if rezip:
		pPrint('Re-zipping GITS...')

if __name__ == '__main__':
	main()
