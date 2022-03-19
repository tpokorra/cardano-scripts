#!/usr/bin/python3

# apt-get install python3 python3-requests

import requests
import subprocess
import os
import json
import datetime

bashCmd = ["cardano-cli", "query", "tip", "--testnet-magic", "1097911063"]
nodePath = "/home/cardano/"
my_env = {'CARDANO_NODE_PATH': nodePath, 'CARDANO_NODE_SOCKET_PATH': nodePath+'/node.socket', 'PATH': os.environ['PATH']+':/usr/share/cardano'}
process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE, env=my_env)

output, error = process.communicate()
mynode = json.loads(output)
print("<pre>")
print("my node: ")
#print(mynode)
print("  epoch: {0}".format(mynode['epoch']))
print("  block: {0}".format(mynode['block']))
print("  sync:  {0}".format(mynode['syncProgress']))

# get your free API key at https://blockfrost.io/auth/signin
# see https://developers.cardano.org/docs/get-started/blockfrost/
APIKey="topsecret"
url="https://cardano-testnet.blockfrost.io/api/v0/blocks/latest"
header = {'project_id': APIKey}
response = requests.get(url, headers=header)
if response.status_code == 200:
    check = response.json()
    #print(response.json())
    print("  epoch: {0}".format(check['epoch']))
    print("  height: {0}".format(check['height']))
    if check['epoch'] == mynode['epoch']:
        if mynode['block'] - check['height'] <= 10:
            print("my node is uptodate")
            exit()

if float(mynode['syncProgress']) > 99.0 and float(mynode['syncProgress']) <= 100.0:
  print("my node is uptodate")
  exit()

print("my node is not uptodate")
exit(-1)

