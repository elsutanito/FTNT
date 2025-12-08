# Secure SDWAN Laboratory 01

## Use Case: Smart Provisioning with FortiManager

| Info | Result |
| ---- | ---- |
| Time to Complete | 30 Minutes |
| Dependencies | N/A |

!!! note "About this Use Case"

    In this Use Case you will explore how to create a FortiManager base to connect FortiGates.

### ADOM Creation

1. Open FortiManager (fmg),

    Login with admin/fortinet

    ![IMG](../images/05/img1.jpeg){ width="500" }

    ???+ warning

        If you get a prompt to upgrade, please do not upgrade.

1. Click **Create New ADOM**

    ![IMG](../images/05/img2.jpeg){ width="600" }

1. Set the following parameters

    - **Name**: *XPerts25*
    - **Central Management:** *Disable* **FortiAP** and **FortiSwitch**

    ![IMG](../images/05/img3.jpeg){ width="600" }

    Click **OK**

    ???+ warning

        You might receive an ADOM disk quota warning, this is because FAZ features are enabled and disk is allocated to the different ADOMs, no need to worry about this because we are not using much disk.

1. After the ADOM Creation log into the new ADOM

    ![IMG](../images/05/fmg_xperts_adom.png){ width="600" }

### Group Structure

1. Go to **Device Manager -> Device & Groups** then right click on **Managed FortiGate(0)** -> **+Create New Group**

    ![IMG](../images/05/img5.jpeg){ width="600" }

    ???+ info

        You will create the following Group Structure

        - HUBs
             - HUBs-CAN
             - HUBs-LAT

        - SPKs
             - SPKs-CAN
             - SPKs-LAT
                  - SPKs-LAT-NOLA
                  - SPKs-LAT-SOLA

        See below tip for efficiency!

1. Set a **Group Name** *HUBs-LAT* then Click **OK**

    ![IMG](../images/05/img6.jpeg){ width="600" }

    ???+ tip

        Start with the Groups lower on the tree then create the higher group, while creating the higher add the lower at the creation screen.

        You can use this order of creation 
        
        For HUBS: HUBs-LAT -> HUBs-CAN -> HUBs (add the HUBs-LAT and HUBs-CAN to the HUBs group)

        For Spokes: SPKs-LAT-SOLA -> SPKs-LAT-NOLA -> SPKs-LAT (add SPKs-LAT-SOLA & SPKs-LAT-NOLA) -> SPKs-CAN -> SPKs (add SPKs-CAN & SPKs-LAT)

1. Final result should look like this.

    ![IMG](../images/05/img8.jpeg){ width="600" }

### Device Blueprint

1. Click on the **Down Arrow** then **Device Blueprint**

    ![IMG](../images/05/img9.jpeg){ width="600" }

1. Click **Create New**

    ![IMG](../images/05/img10.jpeg){ width="600" }

1. Set

    - **Name:** *SPKs-LAT-SOLA*
    - **Device Model:** *FortiGate-VM64-KVM*
    - **Port Provisioning:** *10*
    - **Add to Device Group:** *SPKs-LAT-SOLA (related to name)*

    ![IMG](../images/05/img11.jpeg){ width="600" }

    Click **OK**.

    ???+ note

        Please create the following Blueprints, make sure names are exact as they will need to match the import template later.

        SPKs-LAT-NOLA / SPKs-LAT-NOLA

        SPKs-CANADA / SPKs-CAN

        HUBs-LATAM / HUBs-LAT

        HUBs-CANADA / HUBs-CAN

    ???+ tip

        For quick configuration you can clone the Device Blueprint.  Change the **Name** and **Add to Device Group**.

1. Final result should look like this.

    ![IMG](../images/05/img13.jpeg){ width="600" }

    Click **Close**

### ZTP Inventory

1. We have automated the device on-boarding process for faster lab times, this time you won't have to connect to FortiGates to add to the FortiManager, we will leverage on ZTP configuration to make it quicker.

    ???+ tip
        You can use your own SSH client with ssh root@\<lab url\> -p 11019

        usr: root

        pwd: fortinet

1. Connect to the **toolhost (SSH)**

    Use direct SSH for better results
    ```bash
    ssh root@<your lab url> -p 11019
    ```

    Change directory to /fortipoc/autodeploy

    ```bash
    cd /fortipoc/autodeploy
    ```

    Download LATAM scripts

    At Toolhost

    ```bash
    wget https://storage.googleapis.com/jmc_xperts25/XPerts25_FSASE_Scripts.zip
    unzip XPerts25_FSASE_Scripts.zip
    chmod +x generate_inventory_lat.py fix_fmg_fgtsn_postrestore.py
    ```

    Execute generate_inventory_lat.py to generate the inventory CSV

    ```bash
    ./generate_inventory_lat.py
    ```

    Inventory information will be displayed at the terminal, you will need to copy the information into a file in your computer (inventory.csv).

    ![IMG](../images/05/img14.jpeg){ width="1000" }

    ???+ tip

        We used vscode to execute the command and generate the file from the output.

    ???+ warning

        Please make sure the file you created are in plaintext and do eliminate all spaces after each lines because they will break the FortiManager import.

        Inventory information is per Lab, please do not use other Labs .csv file

    Resulting file should look something like this, notice there are no spaces after each line

    ![IMG](../images/05/inventory_csv.png){ width="1000" }

1. Go back to the FortiManager

    Click on **Add Device**

    Click **Import Model Devices from CSV File**

    ![IMG](../images/05/img15.jpeg){ width="600" }

1. Click **Add Files** then import the file **inventory.csv** you created.

    ![IMG](../images/05/img16.jpeg){ width="600" }

1. Verify Device Blueprints matches the ones you have created, then Click **Next** and **Finish.**

    ![IMG](../images/05/img17.jpeg){ width="600" }

1. The final result should look like this:

    6 new devices assigned to their corresponding groups.

    ![IMG](../images/05/img18.jpeg){ width="600" }

1. To further validate import, Right Click on site1-1 then Click **Edit Variable Mapping**, it should have the variables populated with the information.

    ![IMG](../images/05/img19.jpeg){ width="600" }

    Click **Cancel**

    ???+ info

        On our previous Lab you had to get into every device and change some configurations such as network IPs and hostname, this time we will streamline this process with a little Script.

1. Navigate to **Policy & Objects** -> **Advanced** -> **Metavariables** and take a look at the variables created from the CSV import.

    ![IMG](../images/sdwan/nav_metavar-e.png){ width="600" }

    !!! abstract "Take Action!"

        Open some variables to see their values, they will have mapping for the different devices.

### ZTP Support Scripts

!!! note "About this Lab"

    Sometimes we will need help from scripts to set thing up the way we like, in this Lab we are using a script to configure the interfaces.

1. Go to **Device Manager** -> **Provisioning Templates**

    Click on **CLI**

    ![IMG](../images/05/img20.jpeg){ width="600" }

1. Click **Create New** -> **CLI Template**

    ![IMG](../images/05/img21.jpeg){ width="600" }

1. Enter the following parameters:

    - **Name**: *KickStart*
    - **Type**: *Jinja*
    - **Script Details:**
        ```jinja title="KickStart"
        config system global
          {% if hostname is defined %}
          set hostname {{hostname}}
          {% endif %}
        end
        config system interface
          edit port1
            set mode dhcp
            set role wan
          next
          {% if isp2_intf is defined %}
            edit port2
              set mode dhcp
              set role wan
            next
          {% endif %}
          {% if mpls_intf is defined %}
          edit port4
            set mode dhcp
            set role wan
            set defaultgw disable
            next
          {% else %}
          edit port4
            unset ip
            set mode static
            set status down
            next
          {% endif %}
          edit port5
            set mode static
            set ip {{ lan_ip }}
            set role lan
          next
        end
        config system autoupdate schedule
            set status disable
        end
        ```

    ![IMG](../images/05/img22.jpeg){ width="600" }

    Click **OK**

1. Let's assign our Script to the Devices, Select the new CLI Template then Click on **Assign to Device/Group**

    ![IMG](../images/05/img23.jpeg){ width="600" }

1. Select all Sites then add them to **Selected Entries**

    ![IMG](../images/05/img24.jpeg){ width="600" }

1. Click **OK**

    ![IMG](../images/05/img25.jpeg){ width="600" }

1. Validate that devices are assigned to the CLI Template.

    ![IMG](../images/05/img26.jpeg){ width="600" }

1. Go Back to **Device Manager -> Device & Groups**, Select All Devices

    ![IMG](../images/05/img27.jpeg){ width="600" }

1. Right click and do a **Quick Install (Device DB)** then Click **OK.**

    Wait for the install to finish and click **Finish**

    ![IMG](../images/05/img28.jpeg){ width="600" }

1. To validate changes click **site1-1**, go to **Network: Interfaces** and check the IP port **port5** is assigned.

    ![IMG](../images/05/img29.jpeg){ width="600" }

### ZTP Onboard Devices

1. Go back to the shell on **z_toolhost** and execute

    ```bash
    cd /fortipoc/autodeploy/
    ./onboard_devices.py
    ```

    from ```/fortipoc/autodeploy/``` directory

    ![IMG](../images/05/img30.jpeg){ width="600" }

    ???+ note

        This Script will connect to all FGTs and execute the command ```execute factoryreset2 keepvmlicense```, Fortigate will do factory reset and then connect back to the FortiManager, we are using ZTP DHCP Option 240 on our Lab. 
        
        There are other ways to do ZTP (Zero Touch Provisioning) or LTP (Low Touch Provisioning) [see](https://docs.fortinet.com/document/fortigate/7.2.0/sd-wan-architecture-for-enterprise/372716/zero-touch-provisioning-ztp-using-device-blueprints)
 
        Below the example of the ZTP configuration on the Lab DHCP server

        ![IMG](../images/05/dhcp_option.png){ width="800" }

1. Go back to FortiManager **Device Manager -> Device & Groups** , wait some minutes (5 max) and you should start seeing the Devices coming online (green).

    Click on the Tasks to see the linking status.

    ![IMG](../images/05/img31.jpeg){ width="1000" }

1. Go to **System Settings --> Task Monitor** and check all Task Status is **Success**

    If you find any **Error** double click on the error to see the device that failed and manually execute a reset

    ```bash
    execute factoryreset2 keepvmlicense
    ```

    ![IMG](../images/05/img32.jpeg){ width="1000" }

1. Going Back to **Device Manager** all devices should be green & **Synchronized**

    ![IMG](../images/05/img33.jpeg){ width="1000" }

## System Template

| Info | Result |
| ---- | ---- |
| Time to Complete | 10 Minutes |
| Dependencies | N/A |

!!! note "About this Lab"

    In this Lab we are going to learn how to create a System Template to send logs to our FortiManager that have the FortiAnalyzer feature enabled.

1. Navigate to **Device Manager** -> **Provisioning Templates** -> **System Templates**

    ![IMG](../images/sdwan/nav_sys_template-e.png){ width="600" }

    Click **+ Create New** -> **Blank Template**

1. Navigate to your FortiManager **Dashboard** and copy the FortiManager **Serial Number** from the **System Information** widget, save it for later.

1. Set

    - **Name**: *SysTemplate01*
    - **Log Settings** :white_check_mark:
    - **Send Logs to FortiAnalyzer/FortiManager** :white_check_mark:
    - **Sent To**: *Specify IP Address*
         - *192.168.0.15*
    - **Specify Serial Number**: Serial number from last step.
    - **Upload Option**: *Real-time*
    - **Encrypt Log Transmission**: *High*
    - **Reliable Logging to FortiAnalyzer** :white_check_mark:
  
    ![IMG](../images/sdwan/sys-temp-faz.png){ width="600" }

    Click **OK**

    !!! note

        We need to assign the System Template to the Devices and then Install, we will skip this for the moment and do a the next lab so we don't have to double our effort once we create the Overlay Template.
