#!/usr/bin/python3
import sys
import os.path
import subprocess

gitDir = '/home/xxx/Documents/'
outputFile = '/home/xxx/output.txt'

def pPrint(text):
	print('\033[95m' + str(text) + '\033[0m')


def main():

	# Checks if a directory was specified in the command line call:
	if len(sys.argv) > 1:
		global gitDir
		gitDir = str(sys.argv[1])


	pPrint('Updating git repos...')

	list = os.listdir(gitDir)

	pPrint('Directory: ' + gitDir)

	pPrint(list)
	pPrint('Directory count: ' + str(len(list)))
	pPrint('\n----------------')

	rezip = False

	for dir in list:
		print('\033[95m' + '|- ' + dir + '\n|------' + '\033[0m', end='')
		r1 = subprocess.check_output('git pull', shell=True, cwd=gitDir + '/' + dir)
		r1 = r1.decode('UTF-8').rstrip()
		pPrint(r1)

		if r1 != 'Already up to date.': # NOT WORKING, always zips
			rezip = True
			pPrint('----------------')
			pPrint('Not up to date!')

	pPrint('----------------')

	if rezip:
		pPrint('Re-zipping GITS...')
		r2 = subprocess.check_output('zip -r GITS.zip Documents', shell=True, cwd=gitDir + '/..')
		r2 = subprocess.check_output('cp GITS.zip /media/HD/Documents', shell=True, cwd=gitDir + '/..')
		pPrint('DONE!')

if __name__ == '__main__':
	main()
