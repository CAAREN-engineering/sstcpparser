#!/usr/bin/env python3.12

#######
## This version uses a modified version of `ss` which addresses some of the parsing difficulties when using the
## stock version.
## All items are reported as key:value pairs, including the TCP congestion algorithm (cong_alg) and the various
## Booleans (eg, ts, ecn, etc)
## This modified ss is a statically linked binary
######

# TODO: test if `ss` is where we expect it

from datetime import datetime
import json
import pathlib
import re
import subprocess
import time

# unix epoch for dict metadata
now = int(time.time())

# time for filename
timestamp = datetime.now().isoformat(timespec='seconds').replace(":", "-")
filename = f"./results/pretty-ss_{timestamp}.json"

# make sure we can write to a results directory
path = pathlib.Path('results')
path.mkdir(parents=True, exist_ok=True)

def get_info():
    """
    get the output from `ss`
    :return:
    """
    command = './modifiedss/ss -H -t -i state established'

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # convert output to a list
    ssresults = result.stdout.split('\n')

    ### remove empty last lin
    if len(ssresults[-1]) == 0:
        del(ssresults[-1])

    return ssresults


def extract_v6_sockets(insocket):
    """
    # IPv4 sockets have the format addr:port, which is easy to deal with
    # IPv6 is more complicated because the ':' to denote the port would be confusing if it were simply appended
    # to the raw address.  So, the address is wrapped in square brackets.  We need to extract what's inside the brackets
    # as the addr, and what follows ']:' as the port number
    :param insocket: string
    :return: tuple: addr,port
    """
    match = re.match(r'\[([^\]]+)\]:(.+)', insocket)
    if match:
        address = match.group(1)
        port = match.group(2)
        return address, port
    else:
        return None, None


def parse_results(ssitems):
    # create a dictionary
    analysis = { 'metadata': {'time': now}}
    analysis['sockets'] = []        # sockets will be a list of dicts within this dictionary

    for i in range(0, len(ssitems), 2):
        # initialize a temporary dictionary
        tdict = {}

        # deal with the first line - socket endpoints
        socket_endpoints = ssitems[i].split()
        recvq = socket_endpoints[0]
        sendq = socket_endpoints[1]
        # handle IPv4 vs IPv6
        if '[' in socket_endpoints[2]:
            localaddr, localport = extract_v6_sockets(socket_endpoints[2])
            remoteaddr, remoteport = extract_v6_sockets(socket_endpoints[2])
        else:
            localaddr, localport = socket_endpoints[2].split(':')
            remoteaddr, remoteport = socket_endpoints[2].split(':')
        tdict['recvq'] = recvq
        tdict['sendq'] = sendq
        tdict['localaddr'] = localaddr
        tdict['remoteaddr'] = remoteaddr
        tdict['remoteport'] = remoteport
        tdict['localport'] = localport
        tdict['remoteport'] = remoteport


        # second line
        details = ssitems[i + 1].split()

        for item in details:
            key, value = item.split(':')
            tdict[key] = value

        analysis['sockets'].append(tdict)
    return analysis


def main():
    info = get_info()
    parsed_results = parse_results(info)
    with open(filename, 'w') as outfile:
        json.dump(parsed_results, outfile, indent=4)



if __name__ == '__main__':
    main()