#!/usr/bin/env python
import sys
from pyfiglet import Figlet

# Intended usage:
# python comment.py '#' Comment.py
# Outputs...

#    _  _      ____                                     _
#  _| || |_   / ___|___  _ __ ___  _ __ ___   ___ _ __ | |_   _ __  _   _
# |_  ..  _| | |   / _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \| __| | '_ \| | | |
# |_      _| | |__| (_) | | | | | | | | | | |  __/ | | | |_ _| |_) | |_| |
#   |_||_|    \____\___/|_| |_| |_|_| |_| |_|\___|_| |_|\__(_) .__/ \__, |
#                                                            |_|    |___/

def pPrint(text):
	print('\033[95m' + str(text) + '\033[0m')

def main():

	sys.argv.pop(0)                    # remove script name
	commentType = sys.argv[0]          # gets first word to use as comment symbol
	input = str(' '.join(sys.argv))    # joins all terms into a string
	f = Figlet()                       # text art library
	text = f.renderText(input)         # convert input to art string
	lines = text.splitlines()          # get each line of art string
	output = ''

	for line in lines: # add comment symbol to start of each line
		output += commentType + ' ' + line + '\n'

	pPrint(output) # print in pink
	return True

if __name__ == '__main__':
	main()

# jd:Misc jd$ python comment.py // sudo rm -rf /
# //     ____                _                                      __      __
# //    / / /  ___ _   _  __| | ___    _ __ _ __ ___          _ __ / _|    / /
# //   / / /  / __| | | |/ _` |/ _ \  | '__| '_ ` _ \   _____| '__| |_    / /
# //  / / /   \__ \ |_| | (_| | (_) | | |  | | | | | | |_____| |  |  _|  / /
# // /_/_/    |___/\__,_|\__,_|\___/  |_|  |_| |_| |_|       |_|  |_|   /_/
