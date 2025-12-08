# Secure SDWAN Laboratory 01

## Use Case: SD-WAN Dual HUB (Testing and Troubleshooting)

| Info | Result |
| ---- | ---- |
| Time to Complete | 30 Minutes |
| Dependencies | Use Case: Secure SDWAN Laboratory 03 |

!!! note "About this Use Case"

    In this use case you will create and SD-WAN configuration with 2 HUBs in Primary - Secondary mode using the SDWAN Overlay Template to simplify the configuration.

### 4.1. Validate

1. Navigate to **Device Manager ->** **Monitors** -> **VPN Monitor** and Enable **Show Table**.

    ??? bug

        You might get an error at the Map loading, this is due Lab environment not always having the resources the VMs need but don't worry about it.

    All the VPNs withing the LATAM region should be UP.

    ![IMG](../images/06/img50.jpeg){ width="1000" }

1. Go to **SD-WAN Monitor -> Table View**

    As well as SD-WAN template should have been associated with LATAM's spokes.

    ![IMG](../images/feature/sdw_mon_tview-e.png){ width="800" }

    !!! question

        Why is port4 in grey?

    ??? tip "Answer"

        There are not Health Checks for port4, we removed the default HC, the Overlay Template only created HC for the VPNs and we created an HC for Internet (port1 and port2)

1. Navigate to **Device Manager** -> **Device & Groups** -> **Logging FortiGate** and notice the FortiGates are logging into the FMG, this is from the System Template configuration.

    ![IMG](../images/sdwan/nav_device_logging-e.png){ width="800" }

### 4.2. Testing Connectivity to HUBs

!!! abstract "Let's test!"

    Connectivity will be tested from **client1-1** and **client1-2.**

1. Go to the POD dashboard connect to **client1-1** via **SSH.**

    Ping **to 10.1.0.7** *(HUB 1 LAN)* and **10.2.0.7** *(HUB 2 LAN)*

    ```
    ping 10.1.0.7
    ```

    ``` title="ping 10.1.0.7"
    PING 10.1.0.7 (10.1.0.7) 56(84) bytes of data.
    64 bytes from 10.1.0.7: icmp_seq=1 ttl=62 time=1.48 ms
    64 bytes from 10.1.0.7: icmp_seq=2 ttl=62 time=1.35 ms
    64 bytes from 10.1.0.7: icmp_seq=3 ttl=62 time=1.35 ms
    64 bytes from 10.1.0.7: icmp_seq=4 ttl=62 time=1.44 ms
    64 bytes from 10.1.0.7: icmp_seq=5 ttl=62 time=1.17 ms
    64 bytes from 10.1.0.7: icmp_seq=6 ttl=62 time=1.34 ms
    --- 10.1.0.7 ping statistics ---
    6 packets transmitted, 6 received, 0% packet loss, time 5007ms
    rtt min/avg/max/mdev = 1.172/1.357/1.479/0.097 ms
    ```

    ```
    ping 10.2.0.7
    ```

    ``` title="ping 10.2.0.7"
    PING 10.2.0.7 (10.2.0.7) 56(84) bytes of data.
    64 bytes from 10.2.0.7: icmp_seq=1 ttl=62 time=2.14 ms
    64 bytes from 10.2.0.7: icmp_seq=2 ttl=62 time=1.40 ms
    64 bytes from 10.2.0.7: icmp_seq=3 ttl=62 time=1.39 ms
    64 bytes from 10.2.0.7: icmp_seq=4 ttl=62 time=1.23 ms
    64 bytes from 10.2.0.7: icmp_seq=5 ttl=62 time=1.10 ms
    ^C
    --- 10.2.0.7 ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 4006ms
    rtt min/avg/max/mdev = 1.104/1.453/2.142/0.361 ms
    ```

1. Go to the POD dashboard connect to **client1-2** via **SSH.**

    Ping **to 10.1.0.7** and **10.2.0.7**

    ``` 
    ping 10.1.0.7
    ```

    ``` title="ping 10.1.0.7"
    PING 10.1.0.7 (10.1.0.7) 56(84) bytes of data.
    64 bytes from 10.1.0.7: icmp_seq=1 ttl=62 time=1.82 ms
    64 bytes from 10.1.0.7: icmp_seq=2 ttl=62 time=0.992 ms
    64 bytes from 10.1.0.7: icmp_seq=3 ttl=62 time=1.19 ms
    64 bytes from 10.1.0.7: icmp_seq=4 ttl=62 time=1.13 ms
    64 bytes from 10.1.0.7: icmp_seq=5 ttl=62 time=1.04ms
    --- 10.1.0.7 ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 4004ms
    rtt min/avg/max/mdev = 0.992/1.233/1.818/0.300 ms
    ```

    ```
    ping 10.2.0.7
    ```

    ``` title="ping 10.2.0.7"
    PING 10.2.0.7 (10.2.0.7) 56(84) bytes of data.
    64 bytes from 10.2.0.7: icmp_seq=1 ttl=62 time=1.57 ms
    64 bytes from 10.2.0.7: icmp_seq=2 ttl=62 time=1.17 ms
    64 bytes from 10.2.0.7: icmp_seq=3 ttl=62 time=1.25 ms
    64 bytes from 10.2.0.7: icmp_seq=4 ttl=62 time=1.08 ms
    --- 10.2.0.7 ping statistics ---
    4 packets transmitted, 4 received, 0% packet loss, time 3003ms
    rtt min/avg/max/mdev = 1.083/1.269/1.572/0.184 ms
    ```

    ???+ success

        That confirms that connectivity is working properly from LATAM branches to both datacenters.

### 4.3. Testing Connectivity to Branch

ADVPN (Auto Discovery VPN) is an IPsec technology that allows a traditional hub-and-spoke VPN to establish dynamic, on-demand, direct tunnels between spokes to avoid routing through the topology's hub device. The primary advantage is that it provides full meshing capabilities to a standard hub-and-spoke topology.

SD-WAN monitors ADVPN shortcut's link quality by dynamically creating link monitors for each ADVPN link. The dynamic link monitor on the spoke will use ICMP probes and the IP address of the gateway as the monitored server

!!! abstract "Testing"

    Connectivity will be tested from **client1-1** to **client1-2.**

1. Connect to client1-1 to do

    ```
    ping 10.0.2.101
    ```

    ![IMG](../images/06/img81.jpeg){ width="600" }

    ???+ info

        The red arrow shows the first packet went through the HUB, **delay=10.8 ms** also with **TTL=61**

        The Blue arrow means that subsequent packets will go through the shortcut tunnel, **delay=1.76 ms** now with **TTL=62.**

1. Navigate back to FortiManager

    Go to **Device Manager-> Monitors -> SD-WAN Monitor**

    Click **site1-1\[root\]**

    ![IMG](../images/06/img82.jpeg){ width="600" }

1. Check the **HUB1_HC (Ping: 169.254.0.253)** and notice that **HUB1-VPN_0** have been automatically added to the performance SLA

    ![IMG](../images/sdwan/monitor-sdwa-shortcut-1-e.png){ width="800" }

1. Click **VPN Monitor** -> **Show Table**

    Notice that **site1-1** and **site2-1** have created a shortcut IPsec tunnel via **HUB1-VPN1.**

    ![IMG](../images/06/img84.jpeg){ width="600" }


### 4.4. Wan Simulator

1. Open a tab at the WAN Simulator by using the link on your Lab.

    !!! bug

        WAN Simulator runs on HTTP, some browsers will automatically redirect you to HTTPS, you need to use a browser that doesn't redirect you, we have tested Safari on Mac and Firefox on windows to work.

    !!! tip

        You can use WAN Simulator included in the Lab to create situations such as higher latency or dead interfaces and see the logs.

        ![IMG](../images/sdwan/wan_simulator.png){ width="600" }

    Keep the WAN Simulator around, we will use it later.

### 4.5. Routes

1. On FortiManager navigate to **Device Manager** -> **Device & Groups** -> **Managed FortiGate** -> **site1-1** -> **Dashboard:Summary** -> **Operation** **>_**

    ![IMG](../images/sdwan/nav_dashboard_cmd-e.png){ width="600" }

1. Get the static routes

    ``` console
    get router info routing-table static
    ```

    ``` console title="The output will look like this"
    Routing table for VRF=0
    S*      0.0.0.0/0 [1/0] via 192.2.0.2, port1, [1/0]
                    [1/0] via 192.2.0.10, port2, [1/0]
    S       169.254.1.29/32 [15/0] via HUB1-VPN1 tunnel 100.64.1.1, [1/0]
    S       169.254.1.61/32 [15/0] via HUB1-VPN2 tunnel 100.64.1.9, [1/0]
    S       169.254.1.93/32 [15/0] via HUB1-VPN3 tunnel 172.16.1.5, [1/0]
    S       169.254.1.157/32 [15/0] via HUB2-VPN1 tunnel 100.64.2.1, [1/0]
    S       169.254.1.189/32 [15/0] via HUB2-VPN2 tunnel 100.64.2.9, [1/0]
    S       169.254.1.221/32 [15/0] via HUB2-VPN3 tunnel 172.16.2.5, [1/0]
    S       172.16.0.0/16 [5/0] via 172.16.0.2, port4, [1/0]
    ```

    !!! question

        Take a moment to analyze how does all this routes got there!

    ??? tip "TODO: Answer"

        0.0.0.0 Comes from the Static Route Template you created before, notice that even though we left the **Distance** at 10 at the Template it is set to 1, this is because SD-WAN routes will always have the higher priority.

        HUBx-VPNx Are added by the IPSec

        port4 is added by DHCP

1. Let's check some Kernel Routes

    ``` console
    get router info kernel | grep proto=18
    ```

    ``` console title="The output will look like this"    
    tab=254 vf=0 scope=0 type=1 proto=18 prio=0 192.2.0.9/255.255.255.255/0->8.8.8.8/32 pref=0.0.0.0 gwy=192.2.0.10 dev=4(port2)
    tab=254 vf=0 scope=0 type=1 proto=18 prio=0 192.2.0.1/255.255.255.255/0->8.8.8.8/32 pref=0.0.0.0 gwy=192.2.0.2 dev=3(port1)
    tab=254 vf=0 scope=0 type=1 proto=18 prio=0 169.254.1.130/255.255.255.255/0->169.254.0.252/32 pref=0.0.0.0 gwy=100.64.2.1 dev=23(HUB2-VPN1)
    tab=254 vf=0 scope=0 type=1 proto=18 prio=0 169.254.1.162/255.255.255.255/0->169.254.0.252/32 pref=0.0.0.0 gwy=100.64.2.9 dev=24(HUB2-VPN2)
    tab=254 vf=0 scope=0 type=1 proto=18 prio=0 169.254.1.194/255.255.255.255/0->169.254.0.252/32 pref=0.0.0.0 gwy=172.16.2.5 dev=25(HUB2-VPN3)
    tab=254 vf=0 scope=0 type=1 proto=18 prio=0 169.254.1.34/255.255.255.255/0->169.254.0.253/32 pref=0.0.0.0 gwy=100.64.1.9 dev=21(HUB1-VPN2)
    tab=254 vf=0 scope=0 type=1 proto=18 prio=0 169.254.1.2/255.255.255.255/0->169.254.0.253/32 pref=0.0.0.0 gwy=100.64.1.1 dev=20(HUB1-VPN1)
    tab=254 vf=0 scope=0 type=1 proto=18 prio=0 169.254.1.66/255.255.255.255/0->169.254.0.253/32 pref=0.0.0.0 gwy=172.16.1.5 dev=22(HUB1-VPN3)
    ```

    !!! question

        What are the proto=18 routes?

    ??? tip "Answer"

        proto=18 are routes installed by Fortigate at kernel level for the health checks. See [Technical Tip: Understanding Kernel routing table](https://community.fortinet.com/t5/FortiGate/Technical-Tip-Understanding-Kernel-routing-table/ta-p/199661) for more information.

1. Let's check BGP routes 

    ```
    get router info bgp summary
    get router info routing-table bgp
    ```

    ``` title="get router info bgp summary"
    VRF 0 BGP router identifier 169.254.0.3, local AS number 65005
    BGP table version is 12
    1 BGP AS-PATH entries
    0 BGP community entries

    Neighbor      V         AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
    169.254.1.29  4      65005     406     380        8    0    0 02:13:44        7
    169.254.1.61  4      65005     413     381        7    0    0 02:13:49        7
    169.254.1.93  4      65005     409     383        6    0    0 02:13:50        7
    169.254.1.157 4      65005     295     338        9    0    0 00:14:03        7
    169.254.1.189 4      65005     293     336       11    0    0 00:12:41        7
    169.254.1.221 4      65005     296     336       10    0    0 00:13:16        7

    Total number of neighbors 6
    ```

    ``` title="get router info routing-table bgp"
    Routing table for VRF=0
    B       10.0.2.0/24 [200/0] via 169.254.1.2 [3] (recursive is directly connected, HUB1-VPN1_0), 00:01:32, [1/0]
                        [200/0] via 169.254.1.34 [3] (recursive is directly connected, HUB1-VPN2), 00:01:32, [1/0]
                        [200/0] via 169.254.1.66 [3] (recursive is directly connected, HUB1-VPN3), 00:01:32, [1/0]
                        [200/0] via 169.254.1.130 [3] (recursive is directly connected, HUB2-VPN1), 00:01:32, [1/0]
                        [200/0] via 169.254.1.162 [3] (recursive is directly connected, HUB2-VPN2), 00:01:32, [1/0]
                        [200/0] via 169.254.1.194 [3] (recursive is directly connected, HUB2-VPN3), 00:01:32, [1/0]
    B       10.1.0.0/24 [200/0] via 169.254.1.29 (recursive via HUB1-VPN1 tunnel 100.64.1.1), 11:31:24, [1/0]
                        [200/0] via 169.254.1.61 (recursive via HUB1-VPN2 tunnel 100.64.1.9), 11:31:24, [1/0]
                        [200/0] via 169.254.1.93 (recursive via HUB1-VPN3 tunnel 172.16.1.5), 11:31:24, [1/0]
    B       10.2.0.0/24 [200/0] via 169.254.1.157 (recursive via HUB2-VPN1 tunnel 100.64.2.1), 11:31:24, [1/0]
                        [200/0] via 169.254.1.189 (recursive via HUB2-VPN2 tunnel 100.64.2.9), 11:31:24, [1/0]
                        [200/0] via 169.254.1.221 (recursive via HUB2-VPN3 tunnel 172.16.2.5), 11:31:24, [1/0]
    ```

    !!! question

        Answer the following questions

        - Can you identify the different neighbors?
        - Why does 10.0.2.0 have 7 paths?
        - Why does 10.1.0.0 have 3 paths?
        - If you send traffic to 10.0.2.100 which path will it take?

    ??? tip "Answer Neighbors"

        There are 6 neighbors, 3 per HUB as we have 3 interfaces (port1, port2 and port4), FortiSASE divided the 169.254.1.0/24 Overlay Network you provided in ranges for each overlay port, that is why you have peers with 169.254.1.29/169.254.1.61/169.254.1.93 for HUB1.

    ??? tip "Answer 10.0.2.0"

        10.0.2.0 is a Branch network you can reach it through HUB1 or HUB2.

        Special attention to the path going through HUB1-VPN1_0, this is the shortcut created by the ping.

    ??? tip "Answer 10.1.0.0"

        10.1.0.0 is HUB network, you can access it only from HUB1 as there is no HUB1 to HUB2 communication.

    ??? tip "Answer 10.0.2.100"

        From the BGP Table we can't know, to know we need to check the SD-WAN Rules that create proutes for steering traffic.

### 4.6. SD-WAN

1. Navigate to **Device Manager** -> **Monitors** -> **SD-WAN Monitor** -> **site-1-1** and take a look at all the different dashboards, take your time to understand them, for example in the **SD-WAN Rules** Dashboard you can see the rules and the SD-WAN Member selected at the moment.

    ![IMG](../images/sdwan/sdwan_monitor_02-e.png){ width="800" }

    !!! tip

        The FortiManager monitoring history is only there for 10 minutes, if you want FortiManager to keep it longer you need to enable sdwan-monitoring-history at system admin setting in FortiManager.

        See  [Enabling SD-WAN monitoring history](https://docs.fortinet.com/document/fortimanager/7.4.7/administration-guide/302510) for more information.

    !!! tip

        If you want to see the bandwidth percentage you need to tell FortiGate what bandwidth you have on each interface, that is done through the *estimated-upstream-bandwidth* and *estimated-downstream-bandwidth* configuration at port level.

1. Go to **site1-1** CLI (You already know how) and execute

    ```
    diagnose sys sdwan service4
    ```

    ``` title="diagnose sys sdwan service4"
    Service(1): Address Mode(IPV4) flags=0x4200 use-shortcut-sla use-shortcut
    Tie break: cfg
    Shortcut priority: 2
    Gen(13), TOS(0x0/0x0), Protocol(0): src(1->65535):dst(1->65535), Mode(sla), sla-compare-order
    Member sub interface(4): 
        2: seq_num(4), interface(HUB1-VPN1):
        1: HUB1-VPN1_0(32)
    Members(4): 
        1: Seq_num(4 HUB1-VPN1_0 HUB1), alive, sla(0x1), gid(0), cfg_order(0), local cost(0), selected
        2: Seq_num(4 HUB1-VPN1 HUB1), alive, sla(0x1), gid(0), cfg_order(0), local cost(0), selected
        3: Seq_num(5 HUB1-VPN2 HUB1), alive, sla(0x1), gid(0), cfg_order(1), local cost(0), selected
        4: Seq_num(6 HUB1-VPN3 HUB1), alive, sla(0x1), gid(0), cfg_order(2), local cost(0), selected
    Src address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255

    Dst address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255


    Service(2): Address Mode(IPV4) flags=0x4200 use-shortcut-sla use-shortcut
    Tie break: cfg
    Shortcut priority: 2
    Gen(9), TOS(0x0/0x0), Protocol(0): src(1->65535):dst(1->65535), Mode(sla), sla-compare-order
    Members(3): 
        1: Seq_num(7 HUB2-VPN1 HUB2), alive, sla(0x1), gid(0), cfg_order(0), local cost(10), selected
        2: Seq_num(8 HUB2-VPN2 HUB2), alive, sla(0x1), gid(0), cfg_order(1), local cost(10), selected
        3: Seq_num(9 HUB2-VPN3 HUB2), alive, sla(0x1), gid(0), cfg_order(2), local cost(10), selected
    Src address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255

    Dst address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255


    Service(4): Address Mode(IPV4) flags=0x4200 use-shortcut-sla use-shortcut
    Tie break: cfg
    Shortcut priority: 2
    Gen(7), TOS(0x0/0x0), Protocol(0): src(1->65535):dst(1->65535), Mode(manual)
    Members(2): 
        1: Seq_num(1 port1 WAN1), alive, selected
        2: Seq_num(2 port2 WAN2), alive, selected
    Application Control(2): Salesforce(16920,0) Microsoft.Office.365(33182,0) 
    Src address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255


    Service(3): Address Mode(IPV4) flags=0x4200 use-shortcut-sla use-shortcut
    Tie break: cfg
    Shortcut priority: 2
    Gen(11), TOS(0x0/0x0), Protocol(0): src(1->65535):dst(1->65535), Mode(priority), link-cost-factor(latency), link-cost-threshold(10), heath-check(Internet)
    Members(2): 
        1: Seq_num(1 port1 WAN1), alive, latency: 5.715, selected
        2: Seq_num(2 port2 WAN2), alive, latency: 5.736, selected
    Src address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255

    Dst address(1): 
            0.0.0.0-255.255.255.255
    ```

    !!! tip

        Take a good look at the output from *sdwan service4*, you must understand every detail of it, match it against the one you get from the GUI.

    Try this other commands and understand the output
    ```
    diagnose sys sdwan health-check status HUB1_HC
    diagnose sys link-monitor interface HUB1-VPN1
    diagnose firewall proute list
    ```

    !!! tip

        Make sure you completely understand
        
        - **sla_map=0x1** tag at *sdwan health-check* status, read more information [here](https://community.fortinet.com/t5/FortiGate/Technical-Tip-Understanding-SLA-Target-Map/ta-p/332724)
        - **vwl_** tag at *proute list*, read more information [here](https://community.fortinet.com/t5/FortiGate/Technical-Tip-How-to-find-out-the-Policy-Route-Types/ta-p/270555)

1. From **site1-1** CLI set a debug flow to check the session setup of an ssh connection

    ```
    diagnose debug flow filter daddr 10.0.2.101
    diagnose debug flow trace start 10
    diagnose debug enable 
    ```

1. Go to **client1-1** and ssh to **10.0.2.101**

    ``` 
    ssh root@10.0.2.101
    ```

1. Initiate a ping from the remote server to keep the connection alive

    ```
    ping 10.2.0.7
    ```

1. Head back to **site1-1** CLI and analyze the debug flow, I'm posting some of the interesting SD-WAN lines below

    ```
    id=65308 trace_id=1 func=print_pkt_detail line=6005 msg="vd-root:0 received a packet(proto=6, 10.0.1.101:40070->10.0.2.101:22) tun_id=0.0.0.0 from port5. flag [S], seq 4037558586, ack 0, win 64240"
    id=65308 trace_id=1 func=init_ip_session_common line=6204 msg="allocate a new session-00006d1f"
    id=65308 trace_id=1 func=rpdb_srv_match_input line=1149 msg="Match policy routing id=2130837505: to 10.0.2.101 via ifindex-32"
    id=65308 trace_id=1 func=__vf_ip_route_input_rcu line=1989 msg="find a route: flag=00000000 gw-169.254.1.2 via HUB1-VPN1_0"
    id=65308 trace_id=1 func=__iprope_tree_check line=535 msg="gnum-100004, use addr/intf hash, len=4"
    id=65308 trace_id=1 func=fw_forward_handler line=1002 msg="Allowed by Policy-2:"
    id=65308 trace_id=1 func=ip_session_confirm_final line=3179 msg="npu_state=0x1100, hook=4"
    id=65308 trace_id=1 func=ids_receive line=466 msg="send to ips"
    id=65308 trace_id=1 func=ipsecdev_hard_start_xmit line=662 msg="enter IPSec interface HUB1-VPN1_0, tun_id=0.0.0.0"
    id=65308 trace_id=1 func=_do_ipsecdev_hard_start_xmit line=222 msg="output to IPSec tunnel HUB1-VPN1_0, tun_id=203.0.113.1, vrf 0"
    id=65308 trace_id=1 func=esp_output4 line=917 msg="IPsec encrypt/auth"
    ...
    ```

    !!! tip

        Make sure you understand the output of debug flow.

1. From **site1-1** get the session information for the SSH connection

    ```
    diagnose sys session filter dst 10.0.2.101
    diagnose sys session list
    ```

    ``` title="diagnose sys session list"
    session info: proto=6 proto_state=11 duration=228 expire=3599 timeout=3600 refresh_dir=both flags=00000000 socktype=0 sockport=0 av_idx=0 use=3
    origin-shaper=
    reply-shaper=
    per_ip_shaper=
    class_id=0 ha_id=0 policy_dir=0 tunnel=/ tun_id=203.0.113.1/0.0.0.0 vlan_cos=0/0
    state=log may_dirty ndr f00 
    statistic(bytes/packets/allow_err): org=22240/290/1 reply=24584/188/1 tuples=2
    tx speed(Bps/kbps): 52/0 rx speed(Bps/kbps): 144/1
    orgin->sink: org pre->post, reply pre->post dev=7->30/30->7 gwy=169.254.1.2/0.0.0.0
    hook=pre dir=org act=noop 10.0.1.101:49962->10.0.2.101:22(0.0.0.0:0)
    hook=post dir=reply act=noop 10.0.2.101:22->10.0.1.101:49962(0.0.0.0:0)
    pos/(before,after) 0/(0,0), 0/(0,0)
    src_mac=02:09:0f:00:01:02
    misc=0 policy_id=2 pol_uuid_idx=15846 auth_info=0 chk_client_info=0 vd=0
    serial=000002b6 tos=ff/ff app_list=0 app=0 url_cat=0
    sdwan_mbr_seq=0 sdwan_service_id=1
    rpdb_link_id=ff000001 ngfwid=n/a
    npu_state=0x001108
    no_ofld_reason:  redir-to-ips denied-by-nturbo
    total session: 1
    ```

    !!! tip

        About this Output:
        
        - **dev=** tells you about the interface being used
        - **state** includes the *may_dirty* flag
        - **sdwan_mbr_seq** line tells you information about the SD-WAN decision for this session.

#### 4.7. SD-WAN Fail Over

!!! note

    Now, lets see SD-WAN in action.

1. On **site1-1** sniff the traffic going to 10.0.2.101.

    ```
    diagnose sniffer packet any 'host 10.0.2.101' 4
    ```

    ``` title="diagnose sniffer packet any 'host 10.0.2.101' 4"
    Using Original Sniffing Mode
    interfaces=[any]
    filters=[host 10.0.2.101]
    0.957911 HUB1-VPN1_0 in 10.0.2.101.22 -> 10.0.1.101.49962: psh 204303218 ack 3053437421 
    0.957998 port5 out 10.0.2.101.22 -> 10.0.1.101.49962: psh 204303218 ack 3053437421 
    0.958163 port5 in 10.0.1.101.49962 -> 10.0.2.101.22: ack 204303310 
    0.958191 HUB1-VPN1_0 out 10.0.1.101.49962 -> 10.0.2.101.22: ack 204303310 
    1.958523 HUB1-VPN1_0 in 10.0.2.101.22 -> 10.0.1.101.49962: psh 204303310 ack 3053437421 
    1.958614 port5 out 10.0.2.101.22 -> 10.0.1.101.49962: psh 204303310 ack 3053437421 
    1.958738 port5 in 10.0.1.101.49962 -> 10.0.2.101.22: ack 204303402 
    1.958764 HUB1-VPN1_0 out 10.0.1.101.49962 -> 10.0.2.101.22: ack 204303402
    ...
    ```

    Don't stop the Sniffer!

    !!! tip

        Notice the interface being used is the shortcut HUB1-VPN1_0

1. Go to the WAN Simulator and add +300 ms to **S11-ISP1** (*site1-1 port1*)

    ``` title="diagnose sniffer packet any 'host 10.0.2.101' 4"
    Using Original Sniffing Mode
    interfaces=[any]
    filters=[host 10.0.2.101]
    79.715191 HUB1-VPN1_0 out 10.0.1.101.40070 -> 10.0.2.101.22: ack 289049583 
    80.716537 HUB1-VPN1_0 in 10.0.2.101.22 -> 10.0.1.101.40070: psh 289049583 ack 4037562267 
    80.716662 port5 out 10.0.2.101.22 -> 10.0.1.101.40070: psh 289049583 ack 4037562267 
    80.717012 port5 in 10.0.1.101.40070 -> 10.0.2.101.22: ack 289049675 
    80.717069 HUB1-VPN2 out 10.0.1.101.40070 -> 10.0.2.101.22: ack 289049675 
    ```

    !!! tip
    
        Notice traffic moved to HUB1-VPN2 because VPN1 is out of SLA.
        
        Traffic stopped! why? Answer a few test below!.

    Query the session again
    ```
    diagnose sys session filter dst 10.0.2.101
    diagnose sys session list
    ```

    ``` title="diagnose sys session list"
    ...
    session info: proto=6 proto_state=11 duration=469 expire=3599 timeout=3600 refresh_dir=both flags=00000000 socktype=0 sockport=0 av_idx=0 use=3
    origin-shaper=
    reply-shaper=
    per_ip_shaper=
    class_id=0 ha_id=0 policy_dir=0 tunnel=/ tun_id=10.0.0.1/0.0.0.0 vlan_cos=0/0
    state=log may_dirty ndr f00 
    statistic(bytes/packets/allow_err): org=35028/535/1 reply=59956/433/1 tuples=2
    tx speed(Bps/kbps): 57/0 rx speed(Bps/kbps): 158/1
    orgin->sink: org pre->post, reply pre->post dev=7->21/21->7 gwy=169.254.1.2/0.0.0.0
    hook=pre dir=org act=noop 10.0.1.101:49962->10.0.2.101:22(0.0.0.0:0)
    hook=post dir=reply act=noop 10.0.2.101:22->10.0.1.101:49962(0.0.0.0:0)
    pos/(before,after) 0/(0,0), 0/(0,0)
    src_mac=02:09:0f:00:01:02
    misc=0 policy_id=2 pol_uuid_idx=15846 auth_info=0 chk_client_info=0 vd=0
    serial=000002b6 tos=ff/ff app_list=0 app=0 url_cat=0
    sdwan_mbr_seq=0 sdwan_service_id=1
    rpdb_link_id=ff000001 ngfwid=n/a
    npu_state=0x001108
    no_ofld_reason:  redir-to-ips denied-by-nturbo
    total session: 1
    ```

    !!! question

        From the session out, how do you know the interface being used?

    ??? tip "Answer"

        From the Device information *dev=7->21/21->7* (it might be different on your environment) you know device 21 is being used, to know which one is device 21 do 

        ```
        diagnose netlink interface list
        ```

        ``` title="diagnose netlink interface list"
        if=HUB1-VPN2 family=00 type=768 index=21 mtu=1420 link=0 master=0
        ref=25 state=start present fw_flags=10000000 flags=up p2p run noarp multicast
        ```

        Index 30 was the VPN1_0 shortcut that was used on the first session setup, not is using Index 31 which is VPN2_0 shortcut.

1. Query sdwan service again

    ```
    diagnose sys sdwan health-check status HUB1_HC
    ```

    ``` title="diagnose sys sdwan health-check status HUB1_HC"
    Health Check(HUB1_HC): 
    Seq(4 HUB1-VPN1): state(alive), packet-loss(0.000%) latency(340.927), jitter(5.839), mos(3.547), bandwidth-up(9999999), bandwidth-dw(9999999), bandwidth-bi(19999998) sla_map=0x0
    Seq(4 HUB1-VPN1_0): state(alive), packet-loss(0.000%) latency(336.618), jitter(0.659), mos(3.616), bandwidth-up(10000000), bandwidth-dw(10000000), bandwidth-bi(20000000) sla_map=0x0
    Seq(5 HUB1-VPN2): state(alive), packet-loss(0.000%) latency(6.617), jitter(5.349), mos(4.396), bandwidth-up(9999999), bandwidth-dw(9999999), bandwidth-bi(19999998) sla_map=0x1
    Seq(6 HUB1-VPN3): state(alive), packet-loss(0.000%) latency(1.419), jitter(1.513), mos(4.402), bandwidth-up(9999999), bandwidth-dw(9999999), bandwidth-bi(19999998) sla_map=0x1
    ```

    !!! note

        Note that VPN1 and VPN1_0 are out of SLA and have **sla_map=0x0**

1. Get the SD-WAN rule information

    ```
    diagnose sys sdwan service4
    ```

    ``` title="diagnose sys sdwan service4"
    Service(1): Address Mode(IPV4) flags=0x4200 use-shortcut-sla use-shortcut
    Tie break: cfg
    Shortcut priority: 2
    Gen(14), TOS(0x0/0x0), Protocol(0): src(1->65535):dst(1->65535), Mode(sla), sla-compare-order
    Member sub interface(4): 
        4: seq_num(4), interface(HUB1-VPN1):
        1: HUB1-VPN1_0(32)
    Members(4): 
        1: Seq_num(5 HUB1-VPN2 HUB1), alive, sla(0x1), gid(0), cfg_order(1), local cost(0), selected
        2: Seq_num(6 HUB1-VPN3 HUB1), alive, sla(0x1), gid(0), cfg_order(2), local cost(0), selected
        3: Seq_num(4 HUB1-VPN1_0 HUB1), alive, sla(0x0), gid(0), cfg_order(0), local cost(0), selected
        4: Seq_num(4 HUB1-VPN1 HUB1), alive, sla(0x0), gid(0), cfg_order(0), local cost(0), selected
    Src address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255

    Dst address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255
    ...
    Service(4): Address Mode(IPV4) flags=0x4200 use-shortcut-sla use-shortcut
    Tie break: cfg
    Shortcut priority: 2
    Gen(1), TOS(0x0/0x0), Protocol(0): src(1->65535):dst(1->65535), Mode(manual)
    Members(2): 
        1: Seq_num(1 port1 WAN1), alive, selected
        2: Seq_num(2 port2 WAN2), alive, selected
    Application Control(2): Salesforce(16920,0) Microsoft.Office.365(33182,0) 
    Src address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255


    Service(3): Address Mode(IPV4) flags=0x4200 use-shortcut-sla use-shortcut
    Tie break: cfg
    Shortcut priority: 2
    Gen(5), TOS(0x0/0x0), Protocol(0): src(1->65535):dst(1->65535), Mode(priority), link-cost-factor(latency), link-cost-threshold(10), heath-check(Internet)
    Members(2): 
        1: Seq_num(2 port2 WAN2), alive, latency: 5.501, selected
        2: Seq_num(1 port1 WAN1), alive, latency: 415.633, selected
    Src address(3): 
            192.168.0.0-192.168.255.255
            172.16.0.0-172.31.255.255
            10.0.0.0-10.255.255.255

    Dst address(1): 
            0.0.0.0-255.255.255.255
    ```

    !!! note

        Notice the members on **Service (1)** now start with *Seq_num(5 **HUB1-VPN2** HUB1)* ...

    !!! question
        Take a look at **Service (3)** and **Service (4)**

        - What is the preferred interface for Service (3) and why?
        - What is the preferred interface for Service (4) and why?

    ??? tip "Answer"

        - The preferred interface for Service (3) is WAN2 because this SD-WAN rule strategy is SLA and WAN1 is out of SLA.
        - The preferred interface for Service (4) is WAN1 because this SD-WAN rule strategy is *Manual* which doesn't take into account the SLA of the interface, it will only change to WAN2 when WAN1 goes down.

    ???+ tip "Answer (SSH Session Stopped)"

        The problem is that the ssh session was taking the shortcut tunnel HUB1-VPN1_0 established before with the ping, so the hub was not aware at all of that session.
    
        We need to add two parameters to the HUBs policy to address this two scenarios:
    
             - set anti-replay disable (to disable tcp seq check for the session)
             - set tcp-session-without-syn all (to allow a new session that the first packet seen by the firewall is not a tcp syn)

        We also need **tcp-session-without-syn** to be enabled at **system -> settings** on HUB devices.

1. Navigate to **Device Manager** -> **Device & Groups** -> **site1-H1** -> **CLI Configuration** -> **System** -> **settings** and enable *tcp-session-without-syn* for **site1-H1** and **site1-H2**.

    ![IMG](../images/sdwan/nav_device_cli_tcp_syn_01.png){ width="1000" }

1. Navigate to **Policy & Objects** -> **Policy Packages** -> **HUBs-LAT_PP/Firewall Policy** then Edit the **ADVPN** Policy, scroll down to **Advanced** set

    - **anti-replay** *(disabled)*
    - **tcp-session-without-syn**: *all* 

    ![IMG](../images/sdwan/policy_advpn_01.png){ width="1000" }
    ![IMG](../images/sdwan/policy_advpn_02.png){ width="1000" }

1. Install the Policy Package

1. Get the latency down to 0 again in wan simulator, do the ssh again and repeat the [test](sd-wan-latam.md#sd-wan-fail-over) to check that now the ssh session works after the path change.

    !!! note 

        This time the SSH should not stop and the interface must have moved to HUB1-VPN2_0

    ![IMG](../images/sdwan/sdwan-test-wansla.png){ width="1000" }

1. Get the latency down to 0 again, cancel the ping and close the SSH session to continue with the other labs.

### 4.8. Logs

1. Navigate to **Log View** -> **Traffic** and search for any log of **Sub Type**=*forward* (if not found generate some from the clients), take a look at the SD-WAN values.

    ![IMG](../images/sdwan/nav_log_traffic_01-e.png){ width="1000" }

    !!! question

        Read your logs and answer the questions

        - What policy is this traffic using?
        - Is it RIA or DIA?
        - What interface is using and why?
        - What SD-Wan rule is using?
        - What's the health of the SD-WAN when this traffic passed?
  
1. Navigate to **Log View** -> **Event** -> **SD-WAN** and check those logs out, notice there are many of type **Health Check SLA status.**, filter them out and check the other logs, there is some valuable information there.

    ![IMG](../images/sdwan/nav_log_events_01-e.png){ width="1000" }

    !!! question

        Some questions you might find the answers in here

        - Did any member changed state? Why?
        - Has any Health Check failed? Why?
        - What's the current health status for Internet HC?
  
### 4.9. FortiAnalyzer

1. Navigate to **FortiView** -> **SD-WAN** and check out the **Secure SD-WAN Monitor** and **SD-WAN Summary** dashboards, these are Dashboards from FortiAnalyer which are different from the FortiManager **Monitor** dashboard we have being checking.

    ![IMG](../images/sdwan/nav-faz-view-sdw-e.png){ width="1000" }

    !!! question

        What is the main difference between **FortiView** -> **SD-WAN** and the **Device Manager** -> **Monitor** -> **SD-WAN Monitor**

    ??? tip "Answer"

        FortiAnalyzer Monitors are generated from logs.
