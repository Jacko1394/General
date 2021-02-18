#!/usr/bin/python3

senchaSearchTerm = "let devIP = '"
senchaPath = '/Users/jd/GIT/magiq_mobile/documents/app/app/Main.js'

senchaUrlTerm = "//:::COMMENT OUT FOR DEV:::"
senchaPhonePath = "/Users/jd/GIT/magiq_mobile/documents/app/profile/Phone.js"

nativeSearchTerm = 'public const string DocsIP'
native2ndTerm = 'public static readonly bool DevSetup'
nativePath = '/Users/jd/GIT/MAGIQ Mobile/src/Magiq.Mobile.Configuration/Config.cs'

apiIP = '/Users/jd/.ip'

def pPrint(text):
	print('\033[95m' + str(text) + '\033[0m')

def main():
	ip = api = open(apiIP, 'r').read()
	#update(nativePath, nativeSearchTerm, '\t\t' + nativeSearchTerm + ' = "http://' + ip + ':1841/documents";')
	#update(nativePath, native2ndTerm, '\t\t' + native2ndTerm + ' = true;')
	update(senchaPath, senchaSearchTerm, "    let devIP = '" + ip + "';")
	update(senchaPhonePath, senchaUrlTerm, '          //Url.base = url; //:::COMMENT OUT FOR DEV:::')
	return True

def update(path, searchTerm, newLine):

	pPrint(path)
	newLine += '\n'
	file = open(path, 'r+', encoding='utf8')
	text = ''
	found = False

	for line in file.readlines():
		if searchTerm in line:
			if line == (newLine):
				pPrint('\tALREADY DONE! ' + newLine.strip())
				return False
			text += newLine
			pPrint('\tDONE: ' + newLine.strip())
			found = True
		else:
			text += line

	if not found:
		pPrint('\tNOT FOUND: Term = ' + searchTerm)

	file.seek(0)
	file.write(text)
	file.truncate()
	file.close()

main()
