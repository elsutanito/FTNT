#!/usr/bin/env python3

import csv, io
from paramiko import SSHClient, AutoAddPolicy, ssh_exception
from contextlib import redirect_stdout
from paramiko_expect import SSHClientInteraction

fgt_user="admin"
fgt_password="fortinet"

csv_model = """sn,device blueprint,name,vm_interface_number,hostname,loopback,region,isp1_intf,isp2_intf,mpls_intf,lan_intf,lan_ip,lan2_intf,lan2_ip
{{ sn_site1_1 }},SPKs-LAT-NOLA,site1-1,10,site1-1,10.200.1.1,Latam,port1,port2,port4,port5,10.0.1.1/24,port6,10.0.101.1/24
{{ sn_site1_2 }},SPKs-LAT-SOLA,site1-2,10,site1-2,10.200.1.2,Latam,port1,port2,port4,port5,10.0.2.1/24,,
{{ sn_site1_H1 }},HUBs-LATAM,site1-H1,10,site1-H1,10.200.1.253,Latam,port1,port2,port4,port5,10.1.0.1/24,,
{{ sn_site1_H2 }},HUBs-LATAM,site1-H2,10,site1-H2,10.200.1.254,Latam,port1,port2,port4,port5,10.2.0.1/24,,
{{ sn_site2_H1 }},HUBs-CANADA,site2-H1,10,site2-H1,10.200.2.253,Canada,port1,port2,,port5,10.4.0.1/24,,"""
{{ sn_site2_1 }},SPKs-CANADA,site2-1,10,site2-1,10.200.2.1,Canada,port1,port2,,port5,10.4.1.1/24,,"""

FGTs = {
  "site1-1": "192.168.0.31",
  "site1-2": "192.168.0.32",
  "site2-1": "192.168.0.33",
  "site1-H1": "192.168.0.41",
  "site1-H2": "192.168.0.42",
  "site2-H1": "192.168.0.43"
}

def setNewPassword(client, fgt_ip):
    print(f"Connecting to {fgt_ip} with {fgt_user} and trying to set the new password to {fgt_password}")
    client.connect(
        fgt_ip,
        port = 22,
        username = fgt_user,
        password = ""
    )
    interact = SSHClientInteraction(client, display=True, timeout=5)
    interact.expect('.*')
    if 'New Password' in interact.current_output:
        interact.send(fgt_password)
        interact.expect('Confirm Password: ')
        interact.send(fgt_password)
        interact.expect('.*')
    else:
        interact.send("config system admin")
        interact.expect('.*')
        interact.send("edit admin")
        interact.expect('.*')
        interact.send("set password "+fgt_password+"")
        interact.expect('.*')
        interact.send("end")
        interact.expect('.*')

def __doGetSN(client, fgt_ip):
    client.connect(
        fgt_ip,
        port = 22,
        username = fgt_user,
        password = fgt_password
    )
    stdin, stdout, stderr = client.exec_command('get system status')
    return next(l.split(': ')[1].strip() for l in stdout.readlines() if ("Serial-Number" in l))

def getSN(fgt_ip):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        sn = __doGetSN(client, fgt_ip)
    except ssh_exception.AuthenticationException as e:
        setNewPassword(client, fgt_ip)
        sn = __doGetSN(client, fgt_ip)
    finally:
        client.close()

    return sn


def printInventory():
    s = io.StringIO()
    csvIn = csv.DictReader(io.StringIO(csv_model))
    csvOut = csv.DictWriter(s, csvIn.fieldnames)
    csvOut.writeheader()
    for d in csvIn:
        d['sn'] = getSN(FGTs[d['name']])
        csvOut.writerow(d)
    print(s.getvalue())
    print("\n=======================")
    print("spk_canada.csv")
    print("=======================")
    s = io.StringIO()
    csvIn = csv.DictReader(io.StringIO(csv_spk_canada))
    csvOut = csv.DictWriter(s, csvIn.fieldnames)
    csvOut.writeheader()
    for d in csvIn:
        d['sn'] = getSN(FGTs[d['name']])
        csvOut.writerow(d)
    print(s.getvalue())

def main():
    print()
    print("=======================")
    print("inventory.csv")
    print("=======================")
    printInventory()
    print("\n=======================")


if __name__ == "__main__":
    main()
