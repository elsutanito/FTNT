#!/usr/bin/env bash

# Requirements: expect and yq installed
#   sudo apt-get install expect yq

INVENTORY="inventory.yaml"
USER=$(yq -r '.fgt_user' "$INVENTORY")
PASS=$(yq -r '.fgt_password' "$INVENTORY")

# Hosts list (skip zz_ext)
HOSTS=("site1-1" "site1-2" "site1-H1" "site1-H2" "site2-1" "site2-H1")

# Output CSV header
echo "Serial Number,Device Blueprint,Name,vm_interface_number,hostname,loopback,region,isp1_intf,isp2_intf,mpls_intf,lan_intf,lan_ip"
echo "Serial Number,Device Blueprint,Name,vm_interface_number,hostname,loopback,region,isp1_intf,isp2_intf,mpls_intf,lan_intf,lan_ip" > fgt_inventory.csv

for host in "${HOSTS[@]}"; do
  IP=$(yq -r ".sites.\"$host\".ip" "$INVENTORY")

  # If device have password use fast sshpass to get serial number
  SERIAL=$(sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$USER@$IP" \
    "get system status | grep 'Serial-Number'" \
    | awk -F ':' '{print $2}' | tr -d '\r' | xargs)

  if [[ -z "$SERIAL" ]]; then
    echo "[$host] sshpass login failed, trying expect..."
    # --- Fallback to expect (handles fresh FortiGates with no password set) ---
    SERIAL=$(
      expect <<EOF
        log_user 1
        spawn ssh -o StrictHostKeyChecking=no $USER@$IP
        expect {
          "assword:" {
            send "$PASS\r"
            exp_continue
          }
          "No password is configured for admin." {
            expect "New Password:"
            send "$PASS\r"
            expect "Confirm Password:"
            send "$PASS\r"
          }
        }
        expect "#"
        send "get system status\r"
        expect "#"
        send "exit\r"
        expect eof
EOF
    )
    SERIAL=$(echo "$SERIAL" | grep -i "Serial-Number" | awk -F ':' '{print $2}' | tr -d '\r' | xargs)
  fi

  if [[ -z "$SERIAL" ]]; then
    echo "$host,LOGIN_FAILED"
  else
    # CSV Generation
    blueprint=$(yq -r ".sites.\"$host\".blueprint" "$INVENTORY")
    loopback=$(yq -r ".sites.\"$host\".loopback" "$INVENTORY")
    region=$(yq -r ".sites.\"$host\".region" "$INVENTORY")
    isp1_intf=$(yq -r ".sites.\"$host\".isp1_intf" "$INVENTORY")
    isp2_intf=$(yq -r ".sites.\"$host\".isp2_intf" "$INVENTORY")
    mpls_intf=$(yq -r ".sites.\"$host\".mpls_intf" "$INVENTORY")
    mpls_intf=${mpls_intf/null/}
    lan_intf=$(yq -r ".sites.\"$host\".lan_intf" "$INVENTORY")
    lan_ip=$(yq -r ".sites.\"$host\".lan_ip" "$INVENTORY")

    echo "$SERIAL,$blueprint,$host,10,$host,$loopback,$region,$isp1_intf,$isp2_intf,$mpls_intf,$lan_intf,$lan_ip"
    echo "$SERIAL,$blueprint,$host,10,$host,$loopback,$region,$isp1_intf,$isp2_intf,$mpls_intf,$lan_intf,$lan_ip" >> fgt_inventory.csv
  fi
done

echo -e "\n\nFinished, copy fgt_inventory.csv to FortiManager and import it there, you can also copy/paste the output below\n\n"
cat fgt_inventory.csv
rm /root/.ssh/known_hosts
