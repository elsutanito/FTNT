# Secure SDWAN Laboratory 02

## Use Case: SD-WAN Dual HUB (Templates, Overlays)

| Info | Result |
| ---- | ---- |
| Time to Complete | 30 Minutes |
| Dependencies | Use Case: Secure SDWAN Laboratory 01 |

!!! note "About this Use Case"

    In this use case you will create and SD-WAN configuration with 2 HUBs in Primary - Secondary mode using the SDWAN Overlay Template to simplify the configuration.

### 2.1. SD-WAN Template

!!! note "About this Lab"

    Before running the Overlay Orchestrator, we will create the SD-WAN template, hubs, and spokes policy packages to map to the overlay template.

1. Navigate to **Device Manager -> Provisioning Templates**

    ![IMG](../images/06/nav_devmgmt_provtem.png){ width="200" }

1. Click on **Feature Visibility**

    Set

    - **SD-WAN Overlay**: (enabled)
    - **BGP**: (enabled)

    ![IMG](../images/06/img2.jpeg){ width="1000" }

    Click **OK**

    ???+ info

        In this lab, we will create a blank SD-WAN Template that we will use later in the SD-WAN Overlay Template.

        **Note:** You could create it directly from the Overlay Template.

1. Navigate to **SD-WAN** then

    Click **Create New**

    ![IMG](../images/06/nav_sdwan.png){ width="600" }

1. Set

    - **Name**: *SDW-LAT*
    - **SD-WAN status**: *enabled*

    ![IMG](../images/06/img4.jpeg){ width="600" }

1. Scroll down to **Performance SLA**

    Select all of the default SLAs and Click **Delete**.

    ![IMG](../images/06/img5.jpeg){ width="600" }

    Click **OK** then **OK** to close the SD-WAN Template

    ???+ info

        In this lab, we will create blank SPKs and HUBs **Policy Packages** that we will use later in the SD-WAN Overlay Template.

### 2.2. Policy Packages

1. Navigate to **Policy & Objects -> Policy Packages**

    ![IMG](../images/06/nav_policy_package.png){ width="200" }

1. Click **Policy Package** -> **New**

    ![IMG](../images/06/img7.jpeg){ width="600" }

1. Create two policy packages, name them

    - *SPKs-LAT-PP*

    - *HUBs-LAT-PP*

    Optionally you can delete **default** policy package as we will not use it.

    ![IMG](../images/06/img8.jpeg){ width="1000" }

    Click **OK**

1. Final result should look like this.

    ![IMG](../images/06/img9.jpeg){ width="600" }

    ???+ note

        After creating the SD-WAN Template and the Policy Packages, we will create the SD-WAN Overlay Template.

### 2.3. SD-WAN Overlay

!!! note "About this Lab"

    You are now going to use the SD-WAN Overlay template creation 

1. Navigate to **Device Manager -> Provisioning Templates -> SD-WAN Overlay**

    ![IMG](../images/06/nav_provtmp_sdot.png){ width="600" }

    Click **Create New**

    ???+ info

        Overlay Orchestrator will create SD-WAN, IPSec, BPG and CLI templates to get our SD-WAN up and running, we can modify each individual script later to enhance the configuration or add custom configs.

        The SD-WAN Overlay Template will also auto-complete the configuration of your sites SD-WAN Template by auto updating its list of underlay and overlay interface members and configuring its recommended health checks.

1. Set

    - **Name:** *ACME-LAT*
    - **Select New Topology:** *Dual HUB (Primary & Secondary)*

    ![IMG](../images/06/img12.jpeg){ width="600" }

    Click **Advanced**

    !!! tip 

        You can read more about the Topologies in our 4D Document on [SD-WAN Architecture for Enterprise](https://docs.fortinet.com/document/fortigate/7.2.0/sd-wan-architecture-for-enterprise/138128/architecture-and-design)

1. Set

    - **Loopback Address:** *169.254.0.0/24*
    - **Overlay Network**: *169.254.1.0/24*
    - **BGP-AS Number**: *65005*
    - **Auto-Discovery VPN**: *Enable*

    ![IMG](../images/06/sdwot-01.png){ width="600" }

    Click **Next**

1. Set

    - **Primary HUB:** *site1-H1*
    - **Secondary HUB:** *site1-H2*
    - **Branch**: *SPKs-LAT*
    - **Automatic Branch ID Assignment:** *Enabled*

    ![IMG](../images/06/sdwot-02.png){ width="600" }

    Click **Next**

1. Fill in information for HUBs

    site1-H1

    - **WAN Underlay 1:** *port1* **Override IP**: *100.64.1.1*
    - **WAN Underlay 2:** *port2* **Override IP**: *100.64.1.9*
    - **WAN Underlay 3:** *port4* **Override IP**: *172.16.1.5*

    Click the **+** sign under **Network Advertisement**

    - **Network Advertisement:** *port5*

    ---------------------------------------------------------

    site1-H2

    - **WAN Underlay 1:** *port1* **Override IP**: *100.64.2.1*
    - **WAN Underlay 2:** *port2* **Override IP**: *100.64.2.9*
    - **WAN Underlay 3:** *port4* **Override IP**: *172.16.2.5*

    Click the **+** sign under **Network Advertisement**

    - **Network Advertisement:** *port5*

    ---------------------------------------------------------

    ![IMG](../images/06/sdwot-03-e.png){ width="600" }

    Scroll Down

    ???+ info
        Since we are using DHCP interfaces on the HUB, we need to enable **Override IP** to specify the IP address that will be used in the Spokes IPSEC config

1. For the Branches set

    - **WAN Underlay 1**: *port1*
    - **WAN Underlay 2:** *port2*
    - **WAN Underlay 3:** *port4*

    Click the **+** sign under **Network Advertisement**

    - **Network Advertisement:** *port5*

    ![IMG](../images/06/img16.jpeg){ width="600" }

    Click **Next**

1. Set the following information

    ???+ note

        We will use the previously created Policy Packages and SD-WAN Template
        
    - **Add Overlay Objects to SD-WAN Template:** *Enabled* then select *SDW-LAT*
    - **Add Overlay Interfaces and Zones:** *Enabled*
    - **Add Health Check Servers for Each HUB as Performance SLA:** *Enabled*
    - **Normalize Interfaces**: Enabled
    - **Add Health Check Firewall Policy to Hub Policy Package:** *enable* then select *HUBs-LAT-PP*
    - **Add Health Check Firewall Policy to Branch Policy Package:** *enable* then select  *SPKs-LAT-PP*

    ![IMG](../images/06/sdwot-04-e.png){ width="600" }

    Click **Next**

1. Review the configuration

    ![IMG](../images/06/img18-e.jpeg){ width="600" }

    ![IMG](../images/06/img19.jpeg){ width="600" }

    If everything is correct Click **Finish**

    ???+ info

        In this setup, DHCP has been used to learn IP addresses and default gateways on all WAN Interfaces, which means that some traffic may end up in the MPLS interface, causing sub-optimal routing.

        We are going to configure two Default-Routes over ISP1 and 2 using the Static Route Template, this configuration may resolve any sub-optimal routing.

