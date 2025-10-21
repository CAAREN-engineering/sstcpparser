#!/usr/bin/env python3

import time
import subprocess

now = int(time.time())

command = 'ss -H -t -i state established'

result = subprocess.run(command, shell=True, capture_output=True, text=True)

# convert output to a list
ssitems = result.stdout.split('\n')


### remove empty last line
if len(ssitems[-1]) == 0:
    del(ssitems[-1])


# iterate over the list of sockets, two at a time because the output has two lines per socket
#   one for the summary (local:port dest:port)
#   the second for detailed TCP stats

def extract_v6_sockets(insocket):
    """
    # IPv4 sockets have the format addr:port, which is easy to deal with
    # IPv6 is more complicated because the ':' to denote the port would be confusing if it were simply appended
    # to the raw address.  So, the address is wrapped in square brackets.  We need to extract what's inside the brackets
    # as the addr, and what follows ']:' as the port number
    :param insocket: string
    :return: tuple: addr,port
    """
    match = re.match(r'\[([^\]]+)\]:(.+)', s)
    if match:
        address = match.group(1)
        port = match.group(2)
        return address, port
    else:
        return None, None


# create a dictionary
analysis = { 'metadata': {'time': now}}
analysis['sockets'] = []        # sockets will be a list of dicts within this dictionary

for i in range(0, len(ssitems), 2):
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
    summary = [ recvq, sendq, localaddr, localport, remoteaddr, remoteport]

    # second line
    # this part makes the dangerous assumption that the output format is stable
    # when split on space we get a list of items that that look mostly key:value pairs, except for a few values
    # which we'll try to handle.
    # specifically
    #   - there are several booleans that may or may not appear in the output; see parsing_details.md
    #   - the congestion control (eg, reno, cubic) is not a key:value pair
    #   - the 'send' (transmit rate) is not ':' delimited
    #   - pacing_rate is not ':' delimited
    #   - delivery_rate is not ':' delimited
    #   ** for both of the above cases, when we split on space, we'll have the key and value as different items (ie, on different lines)
    #   ** so, we'll have to check the item + 1 when we're iterating through the list
    #   - app_limited is another  boolean - if present, it is true.  if absent, not true?
    #   - other items (such as wscale) return multiple values, '/' separated.  we'll leave those as is
    # first, let's split the details into a list (assuming the string is space delimited)
    details = ssitems[i + 1].split()

    # list of know tcp algorithms
    tcp_algos = ['reno', 'cubic', 'bic', 'bbr']

    for item in details:
        # set the booleans to default False
        timestamp, sack, ecn, ecnseen, fastopen, wscale, app_limited = False
        if len(item.split(':')) == 1:       # we have one of those cases that aren't key:value
            if item in tcp_algos:
                cong_alg = item     # using the var name from `ss` source code
            elif item == "ts": 'timestamp' = True
            elif item == "ecn": 'ecn' = True
            elif item == "ecnseen": 'ecnseen = True'
            elif item == "fastopen": 'fastopen = True'
            # not sure about this one. in the example output, we have a wscale k:v pair, but not bool
            elif item == "wscale": 'wscale = True'
            elif item == "app_limited": 'app_limited = True'
            # TODO ** haven't yet dealt with the send, pacing_rate, and delivery_rate yet!! *************************
        else:                               # we have a 'standard' item in the form k:v
            key, value = item.split(':')




    analysis['sockets'].append(socket)
