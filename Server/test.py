import os.path
import datetime
import time
import subprocess
# import re
# import json
# import gist

transSettings = '/etc/transmission-daemon/settings.json'
pwd = ''
drivePath = '/media/TORRENTS'

class c:
    PINK = '\033[95m'
    END = '\033[0m'

def main():

    #Initial startup wait timer:
    #time.sleep(60)

    print(c.PINK + "START" + c.END)

    #Updates:
    text = subprocess.check_output('ls', shell=True)
    text += subprocess.check_output('cal', shell=True)
    text += subprocess.check_output('pwd', shell=True)
    text = text.decode('UTF-8').strip()

    print(c.PINK + "END" + c.END)

    #Open, load config:
    # f1 = open(transSettings, 'r')
    # data = json.loads(f1.read())
    # f1.close()

    #Save 
    f1 = open('output.txt', 'w+')
    f1.write(str(text))
    f1.close()

    return 0

if __name__ == '__main__':
    main()
