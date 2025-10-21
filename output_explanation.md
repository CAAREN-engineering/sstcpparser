
## some docs about detailed output of `ss`

https://unix.stackexchange.com/questions/542712/detailed-output-of-ss-command
https://blog.mygraphql.com/en/notes/low-tec/network/tcp-inspect/
https://elixir.bootlin.com/linux/v5.4/source/include/linux/tcp.h#L217


##
ts              # TCP timescale option in use
sack            # selective ack enabled
cubic           # congestion window algo in use
wscale:9,7      # window scaling snd_wscale, rcv_wscale
rto:288         # retrans timeout in msec
rtt:85.24/0.172 # RTT measurements average, median deviation in msec
ato:40          # delay ack timeout in msec
mss:1428        # maximum segment size
pmtu:1500       # path mtu to the peer
rcvmss:1428     # maximum segment size you let peers know you will accept
advmss:1428     # advertised mss
cwnd:3          # Congestion window size in bytes= cwnd * mss.
ssthresh:2      # slow-start threshold
bytes_sent:9505730          # RFC4898 tcpEStatsPerfHCDataOctetsOut: total number of data bytes sent
bytes_retrans:38508         # RFC4898 tcpEStatsPerfOctetsRetrans: Total data bytes retransmitted
bytes_acked:9467223         # RFC4898 tcpEStatsAppHCThruOctetsAcked : how many bytes were acked
bytes_received:697633335    # RFC4898 tcpEStatsAppHCThruOctetsReceived: how many bytes were aa
segs_out:2439583            # RFC4898 tcpEStatsPerfSegsOut: The total number of segments sent
segs_in:3874072             # RFC4898 tcpEStatsPerfSegsIn: total number of segments in
data_segs_out:1539547       # RFC4898 tcpEStatsPerfDataSegsOut: total number of data segments sent
data_segs_in:2350829        # RFC4898 tcpEStatsPerfDataSegsIn: total number of data segments in
send 402kbps            # transmit rate
lastsnd:960             # time since data was last sent, in msec
lastrcv:960             # time since data was received, in msec
lastack:876             # time since last ack received, in msec
pacing_rate 482kbps     #
delivery_rate 396kbps   # The most recent goodput, as measured by tcp_rate_gen()
delivered:1533209       # Total data packets delivered incl. rexmits
app_limited             # A boolean indicating if the goodput was measured when the socket's throughput was limited by the sending application
busy:131223008ms        # 
retrans:0/6338          #
reord_seen:93           # number of data packet reordering events
rcv_rtt:314.704         #
rcv_space:454752        # a helper variable for TCP internal auto tuning socket receive buffer
rcv_ssthresh:2513472    # rcv_ssthresh is the window clamp, a.k.a. the maximum receive window size
minrtt:84.967           # minimum round trip time, min time a packet to travel from source to dest 
rcv_ooopack:72388       # Received out-of-order packets
snd_wnd:65536           # The window we expect to receive