#!/usr/bin/python3
import os.path
import datetime
import time
import subprocess
import re
import json
import requests
import pyfiglet


# Configs:
transSettings = '/etc/transmission-daemon/settings.json'

# Globals:
public = ''
output = ''


def pPrint(text):
	print('\033[95m' + str(text) + '\033[0m')
	global output
	output += text + '\n'


def main():
	pPrint('swag')
	return True


if __name__ == '__main__':
	main()
