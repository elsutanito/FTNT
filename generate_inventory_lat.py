#!/usr/bin/env python3

import csv, io
from paramiko import SSHClient, AutoAddPolicy, ssh_exception
from paramiko_expect import SSHClientInteraction

fgt_user="admin"
fgt_password="fortinet"

# 1. Consolidamos todos los sitios en una sola variable (6 dispositivos)
csv_model = """sn,device blueprint,name,vm_interface_number,hostname,loopback,region,isp1_intf,isp2_intf,mpls_intf,lan_intf,lan_ip,lan2_intf,lan2_ip
,SPKs-LAT-NOLA,site1-1,10,site1-1,10.200.1.1,Latam,port1,port2,port4,port5,10.0.1.1/24,port6,10.0.101.1/24
,SPKs-LAT-SOLA,site1-2,10,site1-2,10.200.1.2,Latam,port1,port2,port4,port5,10.0.2.1/24,,
,HUBs-LATAM,site1-H1,10,site1-H1,10.200.1.253,Latam,port1,port2,port4,port5,10.1.0.1/24,,
,HUBs-LATAM,site1-H2,10,site1-H2,10.200.1.254,Latam,port1,port2,port4,port5,10.2.0.1/24,,
,HUBs-CANADA,site2-H1,10,site2-H1,10.200.2.253,Canada,port1,port2,,port5,10.4.0.1/24,,
,SPKs-CANADA,site2-1,10,site2-1,10.200.2.1,Canada,port1,port2,,port5,10.4.1.1/24,,"""

FGTs = {
  "site1-1": "192.168.0.31",
  "site1-2": "192.168.0.32",
  "site2-1": "192.168.0.33",
  "site1-H1": "192.168.0.41",
  "site1-H2": "192.168.0.42",
  "site2-H1": "192.168.0.43"
}

def setNewPassword(client, fgt_ip):
    # (Tu lógica original de password se mantiene igual)
    client.connect(fgt_ip, port=22, username=fgt_user, password="")
    interact = SSHClientInteraction(client, display=True, timeout=5)
    interact.expect('.*')
    if 'New Password' in interact.current_output:
        interact.send(fgt_password); interact.expect('Confirm Password: '); interact.send(fgt_password); interact.expect('.*')
    else:
        interact.send("config system admin"); interact.expect('.*')
        interact.send("edit admin"); interact.expect('.*')
        interact.send("set password "+fgt_password+""); interact.expect('.*')
        interact.send("end"); interact.expect('.*')

def __doGetSN(client, fgt_ip):
    client.connect(fgt_ip, port=22, username=fgt_user, password=fgt_password)
    stdin, stdout, stderr = client.exec_command('get system status')
    return next(l.split(': ')[1].strip() for l in stdout.readlines() if ("Serial-Number" in l))

def getSN(fgt_ip):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        sn = __doGetSN(client, fgt_ip)
    except Exception:
        try:
            setNewPassword(client, fgt_ip)
            sn = __doGetSN(client, fgt_ip)
        except:
            sn = "ERROR_CON"
    finally:
        client.close()
    return sn

def generate_inventory():
    print("\nIniciando recolección de Serial Numbers...")
    csvIn = csv.DictReader(io.StringIO(csv_model))
    
    # Creamos el archivo físico real
    with open('inventory_lat.csv', mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=csvIn.fieldnames)
        writer.writeheader()
        
        for row in csvIn:
            name = row['name']
            print(f"Obteniendo SN para {name} ({FGTs[name]})...")
            row['sn'] = getSN(FGTs[name])
            writer.writerow(row)
            
    print("\n==========================================")
    print("ÉXITO: Archivo 'inventory_lat.csv' generado.")
    print("Contenido final:")
    print("==========================================")
    with open('inventory_lat.csv', 'r') as f:
        print(f.read())

def main():
    generate_inventory()

if __name__ == "__main__":
    main()
