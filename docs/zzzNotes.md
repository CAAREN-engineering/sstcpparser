## some docs about detailed output of `ss`

https://unix.stackexchange.com/questions/542712/detailed-output-of-ss-command
https://blog.mygraphql.com/en/notes/low-tec/network/tcp-inspect/





command = ss -t -i -o state established

result = subprocess.run(command, shell=True, capture_output=True, text=True)

## splilt each line
ssitems = result.stdout.split('\n')

header: 'Recv-Q Send-Q               Local Address:Port                               Peer Address:Port Process'

each socket is them a pair of lines:

v4:  128.164.13.1:ssh                                128.164.13.2:52017 timer:(keepalive,60min,0)
v6: [2606:69c0:5120:5013:f0::1]:ssh   [2606:69c0:5120:5013:b4b4:d647:6628:183a]:51455 timer:(keepalive,14min,0)

identify v4 --
identify v6 if contains []


## first line split
    [
     '0',                       # Recv-Q
     '0',                       # Send-Q
     '128.164.13.1:ssh',        # Local Address:Port
     '128.164.13.2:52017',      # Peer Address:Port
     'timer:(keepalive,60min,0)'# Process
    ]

### remove header
if 'Recv-Q' in ssitems[0]:
    del ssitems[0]

### remove empty last line
if len(ssitems[-1]) == 0:
    del(ssitems[-1])

analysis = {}
analysis['metadata']['time'] = now
for index, item in enumerate(ssitems):
    # deal with the first line - socket endpoints
    socket_endpoints = item.split()
    recvq = socket_endpoints[0]
    sendq = socket_endpoints[1]
    localaddr, localport = socket_endpoints[2].split(':')
    remoteaddr, remoteport = socket_endpoints[2].split(':')
    socket = [ ]



     print(index, item)












## data structure
{ metadata: {
    datetime
    },
  index: #,
  data : {
    Recv-Q, Send-Q, LocalAddrPort, RemoteADdrPort, Process,
    details:
        {}
}
}




----
to get to items in the dict
In [29]: results['sockets'][item]['localaddr'] + ' ' + results['sockets'][item]['localport']
Out[29]: '2606:69c0:5120:5013:f0::1 ssh'


In [35]: for item in results['sockets'].keys():
    ...:     srcsocket = results['sockets'][item]['localaddr'] + ' ' + results['sockets'][item]['localport']
    ...:     dstsocket = results['sockets'][item]['remoteaddr'] + ' ' + results['sockets'][item]['remoteport']
    ...:     print(f"Socket: {item}\tsource: {srcsocket} -- dest: {dstsocket}")
