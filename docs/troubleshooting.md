# Troubleshooting

## Recovering from Backup

1. If something goes wrong we have FortiManager Backups for some Labs finished, you can download Backup from: <https://storage.googleapis.com/jmc_xperts25/AmerIntl_4D_SASE_BK_Aug9.zip>

1. Follow the following procedure to recover from Backup

1. Log into FortiManager

    ![](images/13/img1.jpeg){ width="600" }

1. Select the root ADOM

    ![](images/13/img2.jpeg){ width="600" }

1. At the Dashboard click on **Restore**

    ![](images/13/img3.jpeg){ width="600" }

1. Upload the Backup file, Set
    - **Password**: *fortinet*
    - **Overwrite current IP, routing and HA settings**: *Disable*

    ![](images/13/img4.jpeg){ width="600" }

    Click **OK**

1. Wait for FortiManager to reboot then login again, now enter the **XPerts25** ADOM

    ![](images/13/img5.jpeg){ width="600" }

1. Connect to the **toolhost (SSH)**

    Use direct SSH for better results
    ```bash
    ssh root@<your lab url> -p 11019
    ```

    Change directory to /fortipoc/autodeploy

    ```bash
    cd /fortipoc/autodeploy
    ```

    Download LATAM scripts (If you have not done it before)

    At Toolhost
    
    ```bash
    wget https://storage.googleapis.com/jmc_xperts25/XPerts25_FSASE_Scripts.zip
    unzip XPerts25_FSASE_Scripts.zip
    chmod +x generate_inventory_lat.py fix_fmg_fgtsn_postrestore.py
    ```

    Execute fix_fmg_fgtsn_postrestore.py to update the SN of the VMs to your environment

    ```bash
    ./fix_fmg_fgtsn_postrestore.py
    ```

    ![](images/13/img6.jpeg){ width="600" }

1. Output should look like this.

    ![](images/13/img7.jpeg){ width="600" }

1. Execute

    ```bash
    ./onboard_devices.py
    ```

    ![](images/13/img8.jpeg){ width="600" }

1. Go Back to FortiManager and Navigate to **System Settings -&gt; Advanced -&gt; Misc Settings**

    Set
    
    - **Offline Mode:** *disabled*

    ![](images/13/img9.jpeg){ width="1000" }

    Click **Apply**

1. Navigate to **Device Manager -&gt; Device & Groups -&gt; Managed FortiGate**

    ![](images/13/img10.jpeg){ width="600" }

1. Click on the Bell, it will tell you there are 6 devices configuration out of sync, that's because we did not restore FGTs configuration and there are far from the FMG expected configuration, click on the message.

    ![](images/13/img11.jpeg){ width="600" }

1. Select all devices

    Click **Revert**

    Click **OK** at the warning message

    Click **Close**

    ![](images/13/img12.jpeg){ width="600" }

1. Click the **Tasks**, there will be an installation Task, click on the **install config** task.

    ![](images/13/img13.jpeg){ width="600" }

1. Double click the **Install Configuration** to display progress of each task

    ![](images/13/img14.jpeg){ width="600" }

1. Notice the progress for each device.

    ![](images/13/img15.jpeg){ width="600" }

1. Navigate to **Device Manager -&gt; Device & Groups**

    ![](images/13/img16.jpeg){ width="600" }

1. Click **Install Wizard**

    ![](images/13/img17.jpeg){ width="600" }

1. Install all the Policy Packages to make sure everything is in sync.

    ![](images/13/img18.jpeg){ width="600" }

1. Check that everything is OK, depending on which lab you are recovering you can check

    - VPN Monitor
    - Connect to each FortiGate and see configurations are there
    - Do ping tests
