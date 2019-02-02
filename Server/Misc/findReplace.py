#!/usr/bin/python3

searchTerm = '"docsIP":'
path = '/Users/jd/GIT/MAGIQ Mobile/MagiqMobile/Configuration/config.json'
newLine = 'swag'

def pPrint(text):
	print('\033[95m' + str(text) + '\033[0m')

def main():
	update(path, searchTerm, newLine)
	return True

def update(path, searchTerm, newLine):

	pPrint('Updating: ' + path)
	newLine += '\n'
	file = open(path, 'r+')
	text = ''

	for line in file.readlines():
		if searchTerm in line:
			if line == (newLine):
				pPrint('Already correct! ' + newLine.strip())
				return False
			text += newLine
			pPrint('UPDATED: ' + newLine.strip())
		else:
			text += line

	file.seek(0)
	file.write(text)
	file.truncate()
	file.close()

main()
