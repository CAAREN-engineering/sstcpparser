# Parsing the Socket Details

## Second line
```commandline
cubic wscale:6,7 rto:220 rtt:19.566/2.687 ato:40 mss:1186 pmtu:1500 rcvmss:1186 advmss:1428 cwnd:10 bytes_sent:260133 bytes_retrans:52 bytes_acked:260081 bytes_received:29501 segs_out:1626 segs_in:1977 data_segs_out:1608 data_segs_in:679 send 4.8Mbps lastsnd:16 lastrcv:20 lastack:8 pacing_rate 9.7Mbps delivery_rate 4.7Mbps delivered:1609 busy:12460ms retrans:0/1 dsack_dups:1 reord_seen:1 rcv_space:14400 rcv_ssthresh:64096 minrtt:10.797
```

These are the TCP details of the socket.  There is a lot of useful information here.  It is 'semi-structured' in that many of the items are key:value pairs, but not all of them

To deal with this, first we're going to split the line on a space to create a list of strings.
Most of the items will be in the form key:value which is easy to deal with.
There are a number of items that are not, however.  From the `ss` [source code](https://fossies.org/linux/iproute2/misc/ss.c) we see:
```commandline
  840     char            cong_alg[16];
  888     bool            has_ts_opt;  
  889     bool            has_usec_ts_opt;  
  890     bool            has_sack_opt;  
  891     bool            has_ecn_opt;  
  892     bool            has_ecnseen_opt;  
  893     bool            has_fastopen_opt;  
  894     bool            has_wscale_opt;  
  895     bool            app_limited;
```
The boolean items will only appear if the option is in use.  It is displayed without a key.  For example if the timestamp option is set, `ts` will appear.  If it is not, it will not be in the output
