# SS TCP Parser

This is a simple Python script to make the detailed output of `ss` more readable.

Specifically, `ss -i` provides a lot of detailed information about the TCP socket.  For established connections, the first line is the summary: local socket, remote socket, Send & Receive queues.  

The second line is a dump of a lot of the TCP internals for this socket.  For example:
```commandline
cubic wscale:7,7 rto:204 rtt:1.835/0.586 ato:40 mss:1428 pmtu:1500 rcvmss:1428 advmss:1428 cwnd:10 bytes_sent:47948 bytes_acked:47949 bytes_received:3087501 segs_out:3342 segs_in:5715 data_segs_out:1113 data_segs_in:5676 send 62.3Mbps lastsnd:390948 lastrcv:390940 lastack:390940 pacing_rate 124Mbps delivery_rate 20.3Mbps delivered:1114 app_limited busy:2968ms rcv_rtt:6.79 rcv_space:272808 rcv_ssthresh:1626148 minrtt:1.139 snd_wnd:75648
```

That's hard to read.

This program with put the info into a more readable JSON file.

## Requirements
Python 3.11+

****** This script requires a modified version of `ss` which corrects some parsing difficulties.  Specifically, most items are key:value pairs, except:


 - The congestion algorithm (in the above example `cubic`) is listed without a key
 - There are a number of booleans which are only printed when true:
```
        - bool            has_ts_opt;  
        - bool            has_usec_ts_opt;  
        - bool            has_sack_opt;  
        - bool            has_ecn_opt;  
        - bool            has_ecnseen_opt;  
        - bool            has_fastopen_opt;  
        - bool            has_wscale_opt;  
        - bool            app_limited;
```


Also, a few items are missing `:`, which we use to find key:value pairs.  Specifically, `pacing_rate` and `delivery_rate`

The source code of `ss` has been modified to always print the booleans, add a key for the TCP congestion algorithm item, and add `:` for the rate values.

`ss` included with this repo is statically link.  It has been tested on Debian and Rocky systems.

It appears there are some additional items for `bbr` which are untested, so this script may mangle output for any connections using that algorithm.
