# Secure SDWAN Laboratory 03

## Use Case: SD-WAN Dual HUB (Traffic steering, routing, firewall policies)

| Info | Result |
| ---- | ---- |
| Time to Complete | 30 Minutes |
| Dependencies | Use Case: SDWAN Laboratory 02 |

!!! note "About this Use Case"

    In this use case you will create and SD-WAN configuration with 2 HUBs in Primary - Secondary mode using the SDWAN Overlay Template to simplify the configuration.

### SD-WAN Rules

1. Navigate to **Device Manager -> Provisioning Templates-> SD-WAN**

    Select **SDW-LAT** then Click **Edit**

    ![IMG](../images/06/img63.jpeg){ width="600" }

    !!! note

        Notice that our Overlay template have created some configuration at this previously created SD-WAN Template, we are going to tweak a few things.

1. At **SD-WAN Zones** Click **+ Create New** -> **SD-WAN Zone**

    ![IMG](../images/sdwan/sdw-zones-01-e.png){ width="600" }

1. Set

    - **Name**: *Internet-Underlays*
    - **Interface Members**: 
         - *port1* 
         - *port2*

    ![IMG](../images/sdwan/sdw-zones-02-e.png){ width="600" }

    Click **OK**

1. Select the empty **WAN1** & **WAN2** Zones and click **Delete**

    Final result should look like this

    ![IMG](../images/sdwan/sdw-zones-03-e.png){ width="600" }
    ![IMG](../images/sdwan/sdw-zones-04-e.png){ width="600" }

1. Scroll down to **Performance SLA**

    Click **Create New**

    ![IMG](../images/06/img64.jpeg){ width="600" }

1. Set

    - **Name:** *Internet*
    - **Server:** *8.8.8.8*

    Click **Specify**

    ![IMG](../images/06/img65.jpeg){ width="800" }

1. Select ports **port1** and **port2**

    ![IMG](../images/06/img66.jpeg){ width="800" }

    Click **OK**

1. Scroll down to **SLA Target**

    Click **Add Target**

    ![IMG](../images/06/img67.jpeg){ width="800" }

1. Disable **Jitter** and **Packet Loss**

    Set

    - **Latency:** *255*
    - **Jitter Threshold** *Toggle off*
    - **Packet Loss Threshold** *Toggle off*
    - **Update Static Route** *Toggle off*
    - **Cascade interfaces** *Toggle off*

    ![IMG](../images/06/img68.jpeg){ width="800" }

    Scroll Down then Click **Advanced Options**

1. Set

    - **sla-fail-log-period**: *10*
    - **set sla-pass-log-period**: *10*

    ![IMG](../images/06/img69.jpeg){ width="800" }

    Click **OK**

    ???+ tip

        Performance SLA can be monitored by setting the **set sla-fail-log-period** and **set sla-pass-log-period**. This configuration is necessary for FortiAnalyzer to show information about SLA status in SD-WAN dashboards.

1. Scroll up to **SD-WAN Rules**

    Click **Create New**

    ![IMG](../images/06/img70.jpeg){ width="600" }

1. Set

    - **Name:** *Corporate-HUB1*
    - **Source Address:** *RFC1918-GRP*
    - **Destination -> Address:** *RFC1918-GRP*

    ![IMG](../images/06/img71.jpeg){ width="600" }

1. Scroll Down to **Outgoing Interfaces** and Set

    - **Strategy:** *Lowest Cost (SLA)*
    - **Interface Preference:**
         - *HUB1-VPN1*
         - *HUB1-VPN2*
         - *HUB1-VPN3*
    - **Required SLA Target:** *HUB1_HC#1*

    ![IMG](../images/06/img72.jpeg){ width="600" }

    Click **OK**

1. Clone **Corporate-HUB1** to create the rule for HUB2

1. Set / Change

    - **Name:** *Corporate-HUB2*
    - **Interface Preference:**
         - *HUB2-VPN1*
         - *HUB2-VPN2*
         - *HUB2-VPN3*
    - **Required SLA Target:** *HUB2_HC#1*

    Click **OK**

    ![IMG](../images/06/img73.jpeg){ width="600" }

1. Now let's create an SD-WAN rule for local internet breakout. Click **+ Create New** Under **SD-WAN Rules**

    <!-- ![IMG](../images/06/img74.jpeg){ width="600" } -->

1. Set

    - **Name:** *Internet*
    - **Source Address:** *RFC1918-GRP*
    - **Destination -> Address:** *all*

    ![IMG](../images/06/img75.jpeg){ width="600" }

1. Scroll Down to **Outgoing Interfaces** and Set

    - **Strategy:** *Best Quality*
    - **Interface Preference:**
         - *port1*
         - *port2*
    - **Measure SLA:** Internet
    - **Quality Criteria:** Latency

    ![IMG](../images/06/sdwr-01-e.png){ width="600" }

    Click **OK**

1. Now let's create an SD-WAN rule for critical applications to use **port1** primarily. Click **+ Create New** Under **SD-WAN Rules**

    <!-- ![IMG](../images/06/img74.jpeg){ width="600" } -->

1. Set

    - **Name:** *Critical-DIA*
    - **Source Address:** *RFC1918-GRP*
    - **Application:**
         - *Microsoft.365*
         - *Salesforce*
    - **Strategy:** *Manual*
    - **Interface Preference:** 
         - *port1* 
         - *port2*

    ![IMG](../images/sdwan/sdwr-01-e.png){ width="800" }

    Click **OK**

    !!! note

        Make sure you select port1 first then port2, SD-WAN will select depending on the order you picked the interfaces.

    !!! question

        Why there is no Required SLA in this rule?

    ??? tip "Answer"

        This is a *Manual* strategy, SD-WAN will always pick the first interface you picked no matter the performance, it will only use the next one once the main one completely fails.

1. Move **Critical-DIA** before **Internet**. Final result for SD-WAN Rules should look like this.

    ![IMG](../images/sdwan/sdw-01-e.png){ width="800" }

    Click **OK**

### Static Route Template

!!! note "About this Lab"

    You will create a Static Route Template and add it to the resulting set of Template Groups to make sure the default GW always goes to the ISP with the same weigh as other SD-WAN routes.

??? tip

    One example of the utility of this is when you receive routes from DHCP, they will usually have higher distance than the SD-WAN routes which will take them out of the RIB table when defaults are created for the tunnels.

1. Lets create a Static Route template called **Default**

1. Navigate to **Device Manager -> Provisioning Templates -> Static Route**

    ![IMG](../images/06/img20.jpeg){ width="600" }

    Click **Create New**

1. Set **Name:** *Default*

    Click **Create New -> IPv4 Static Route**

    ![IMG](../images/06/img22.jpeg){ width="600" }

1. Click **Interface** text field and type *$* then select **(isp1_intf)**

    Set **Administrative Distance**: *1*

    ![IMG](../images/06/sr-templ-01-e.png){ width="600" }

    Click **Advanced Options**

    ???+ info
        **$(isp1_intf)** is the meta field variable for **port1**, we assigned values to the metavariables when we imported the csv file.

1. Set **dynamic-gateway**: *(enabled)*

    Click **OK**

    ![IMG](../images/06/img25.jpeg){ width="600" }

1. Right-click **0.0.0.0** then Click **Clone**

    ![IMG](../images/06/img26.jpeg){ width="600" }

1. Set **Interface:** *(isp2_intf)*

    ???+ info
        This is the meta field variable of **port2**

    Click **OK**

    ![IMG](../images/06/img27.jpeg){ width="600" }

1. Final result should look like this.

    ![IMG](../images/06/img28.jpeg){ width="600" }

    Click **OK**

1. Click **+Create New** to create a New Static Route Template set **Name:** *Default_SPKs*

1. Click **+ Create New** -> **IPv4 Static Route** and Set

    - **SD-WAN:** *Enabled*
    - **SD-WAN Zone:** *Internet-Underlays*
    - Leave **Administrative Distance** with the default value.

    ![IMG](../images/sdwan/static-route-01-e.png){ width="600" }

1. It should look like this

    ![IMG](../images/sdwan/static-route-02-e.png){ width="600" }

    Click **OK**

1. Now let's add the Static Route Templates to the Template Groups created by SD-WAN Overlay.

1. Navigate to **Device Manager -> Device & Groups -> Template Groups**

    ![IMG](../images/06/nav_template_groups_01-e.png){ width="600" }

    ???+ info

        Notice the Template Groups Created by SD-WAN Overlay

1. Select **ACME-LAT-HUB1** then Click **Edit**

    ![IMG](../images/06/img30.jpeg){ width="600" }

1. Click the **+** button.

    ![IMG](../images/06/img31-e.jpeg){ width="600" }

1. Set **Static Route Template (0/1) -> Default**

    Click **OK**

    ![IMG](../images/06/img32.jpeg){ width="600" }

    ???+ info

        Repeat the same steps with the remaining Template Groups.

        - Add **Static Route** / *Default* to **ACME-LAT_HUB2** 
        
        - Add **Static Route** / *Default_SPKs* to **ACME-LAT-BRANCH**

        - Add **System Template** / *SysTemplate01* to all 3 Groups.

1. Final result should look like this.

    ![IMG](../images/sdwan/sdw_templates_01-e.png){ width="800" }

### Updating IPSec Password

!!! note "About this Lab"

    The SD-WAN overlay template does not allow you to specify a Pre-shared Key during the wizard instead it will automatically create one for you (which we wont know), to know the Key we will need to modify the IPsec tunnel templates.

    This Pre-shared Key will be used in **Lab 10 SD-WAN Private Access.**

???+ info

    Let's modify ACME-LAT_HUB1_IPsec Template VPN1 and VPN2

    Pre-share Key:**Fortinet123#**

    Modify ACME-LAT_BRANCH_IPsecTemplate:

    HUB1-VPN1 and HUB1-VPN2

    Pre-share Key:**Fortinet123#**

1. Go to **Device Manager** -> **Provisioning Templates->IPsec Tunnel**

    ![IMG](../images/06/img34.jpeg){ width="600" }

1. Right-click **ACME-LAT_HUB1_IPsec** the click **Edit**.

    ![IMG](../images/06/img35.jpeg){ width="600" }

1. Right-click **VPN1** then click **Edit**

    ![IMG](../images/06/img36.jpeg){ width="600" }

1. Change the **Pre-shared Key** to *Fortinet123#*

    Click **OK**

    ![IMG](../images/06/img37.jpeg){ width="600" }

    !!! abstract "Time to Shine!"

        Repeat the same steps for

        ACME-LAT_HUB1_IPsec VPN2

        ACME-LAT_BRANCH_IPsec HUB1-VPN1 and HUB1-VPN2

        We don't need to change VPN3 nor HUB2 because FortiSASE will only connect to HUB1 VPN1 & VPN2

### BGP Tunning

!!! note "About this Lab"

    In this Lab you will fine tune BGP to some best practices, most importantly increasing the adv-additional-path to accommodate for all the routes.

1. Go to **Device Manager** -> **Provisioning Templates-> BGP**

    ![IMG](../images/06/img38.jpeg){ width="600" }

1. Right-click **ACME-LAT_HUB1_BGP** the click **Edit**.

    ![IMG](../images/06/img39.jpeg){ width="600" }

1. Click on **CLI Configurations**

    ![IMG](../images/06/img40.jpeg){ width="600" }

1. Scroll down to **neighbor-group**, right click on **VPN1** and click **Edit**

    ![IMG](../images/06/img41.jpeg){ width="600" }

1. Set **adv-additional-path**: *255*

    Click **OK**

    ![IMG](../images/06/img42.jpeg){ width="600" }

1. Repeat the same step to set **adv-additional-path** for the other 2 neighbor-groups:

    VPN2:

    - **adv-additional-path:** *255*

    VPN3:

    - **adv-additional-path:** *255*

    Click **OK** twice to get back to the BGP Provisioning Template table

    ![IMG](../images/06/img43.jpeg){ width="600" }

1. Right-click **ACME-LAT_HUB2_BGP** the click **Edit**.

    ![IMG](../images/06/img44.jpeg){ width="600" }

1. Click **CLI Configurations** then scroll down to **neighbor-group** and set:

    VPN1:

    - **adv-additional-path:** *255*

    VPN2:

    - **adv-additional-path:** *255*

    VPN3:

    - **adv-additional-path:** *255*

    Click **OK** twice to return to the BGP Provisioning Template table

### Firewall Policies

SD-WAN is not just about designing and configuring SD-WAN strategies for de Edge devices (FortiGate)

In this section, you will modify policy packages to allow branch to DC traffic and branch to branch traffic with basic ADVPN, as well as configuring some SD-WAN rules.

1. Navigate to **Policy & Objects -> Firewall Objects**

    ![IMG](../images/06/nav_policy_fwobjects_01-e.png){ width="200" }

1. Click **+Create New -> Address**

    ![IMG](../images/06/img53.jpeg){ width="600" }

1. Set

    - **Name**: *RFC-3927*
    - **IP/Netmask:** *169.254.0.0/16*

    ![IMG](../images/06/obj_new_addr-e.png){ width="600" }

    Click **OK**

1. Navigate to **Policy & Objects -> Policy Packages**

    Click **HUBs-LAT-PP -> Firewall Policy**

    ![IMG](../images/06/img55.jpeg){ width="600" }

1. Click **+Create New -> + Create New**

    ![IMG](../images/06/img56.jpeg){ width="600" }

1. Set

    - **Name:** *ADVPN*
    - **Incoming Interface:** 
         - *VPN1* 
         - *VPN2* 
         - *VPN3*
    - **Outgoing Interface:** 
         - *VPN1* 
         - *VPN2* 
         - *VPN3*

    ![IMG](../images/06/img57.jpeg){ width="600" }

    !!! bug

        If you don't see the VPN1 VPN2 and VPN3 on your interfaces refresh your browser.

1. Set **Action:** *Accept*

    ![IMG](../images/06/img58.jpeg){ width="600" }

    Click **OK**

    ???+ tip

        We will be enabling NAT in some policies.

        To expose the NAT column, execute steps below.

1. Click the "gear" icon, select NAT then Click Out.

    ![IMG](../images/06/img59.jpeg){ width="1000" }

    !!! abstract "Your time to shine!"

        Using the table in the next step follow the same steps and create the following firewall policies on the **HUBs-LAT-PP** policy package:

        - SPKs-LAT_in
        - SPKs-LAT_out
        - SPKs-LAT_in
        - Internet (DIA)
        - Internet (RIA)

        Make sure to enable NAT on the internet Policies. 

        Include the RFC-3927 and RFC1918-GRP firewall address where required

    ???+ tip "Pro Tip"

        To simplify the creation of some policies and to avoid rework you can right-click **SPK-LAT_in**, for example, and select **Clone Reverse** instead of creating **SPK-LAT_out** from scratch.

        You can also leverage **Clone** for policies that are similar and require minimal changes.

1. Final result should look like this.

    | #   | Name               | From                  | To                            | Source                   | Destination           | Schedule | Service | Action                          | NAT      | Security Profiles               |
    |-----|--------------------|-----------------------|-------------------------------|--------------------------|-----------------------|----------|---------|---------------------------------|---------------------------------|----------|
    | 2   | ADVPN              | VPN1, VPN2, VPN3      | VPN1, VPN2, VPN3              | all                      | all                   | always   | ALL     | Accept                          | Disabled | no-inspection default (SSL)     |
    | 3   | SPKs-LAT_in        | VPN1, VPN2, VPN3      | port5                         | RFC-3927, RFC1918-GRP    | RFC-3927, RFC1918-GRP | always   | ALL     | Accept                          | Disabled | IPS protect_client |
    | 4   | SPKs-LAT_out       | port5                 | VPN1, VPN2, VPN3              | RFC-3927, RFC1918-GRP    | RFC-3927, RFC1918-GRP | always   | ALL     | Accept                          | Disabled | IPS protect_client  |
    | 5   | Internet (DIA)     | port5                 | port1, port2                  | RFC1918-GRP              | all                   | always   | ALL     | Accept                          | Enabled  | default (AV, WEB, APP-C) - SSL certificate-inspection     |
    | 6   | Internet (RIA)     | VPN1, VPN2, VPN3      | port1, port2                  | RFC-1918-GRP             | all                   | always   | ALL     | Accept                          | Enabled  | default (AV, WEB, APP-C) - SSL certificate-inspection     |


    ![IMG](../images/06/sec_policy_hub_01.png){ width="1000" }

    !!! question

        What is the difference between Internet RIA and Internet DIA?

    ??? tip "Answer"

        DIA stands for Direct Internet Access, meaning the LAN going out through the local ISP.

        RIA stands from Remote Internet Access, meaning the LAN going through the SD-WAN to use HUBs Internet Access

        See [SD-WAN Architecture for Enterprise Traffic Flow](https://docs.fortinet.com/document/fortigate/7.2.0/sd-wan-architecture-for-enterprise/626676/traffic-flow)

1. Go to **SPKs-LAT-PP** -> **Firewall Policy**

    !!! abstract "Your time to shine!"

        For the **SPKs-LAT-PP** follow the same steps and create the following firewall policies

        - Corporate_out
        - Corporate_in
        - Internet (DIA)
        - Internet (RIA)

1. Final result should look like this

    | #   | Name               | From          | To        | Source              | Destination          | Schedule | Service | Action  | NAT      | Security Profiles            |
    |-----|--------------------|---------------|-----------|---------------------|----------------------|----------|---------|---------|------------------------------|----------|
    | 2   | Corporate_out       | port5         | HUB1, HUB2| RFC-3927, RFC1918-GRP| RFC-3927, RFC1918-GRP| always   | ALL     | Accept  | Disabled | IPS protect_client   |
    | 3   | Corporate_in        | HUB1, HUB2    | port5     | RFC-3927, RFC1918-GRP| RFC-3927, RFC1918-GRP| always   | ALL     | Accept  | Disabled | IPS protect_client   |
    | 4   | Internet (DIA)      | port5         | Internet-Underlays| RFC1918-GRP         | all                  | always   | ALL     | Accept  | Enabled  | default (AV, WEB, APP-C) - SSL certificate-inspection   |
    | 5   | Internet (RIA)      | port5         | HUB1, HUB2| RFC1918-GRP         | all                  | always   | ALL     | Accept  | Disabled | default (AV, WEB, APP-C) - SSL certificate-inspection   |

    ![IMG](../images/sdwan/policy_01-e.png){ width="1000" }

    !!! tip

        Notice we are not NATing at Internet RIA, we don't need to as the HUB knows our networks, we will NAT at HUB level to go out to the Internet.

    !!! tip

        We are using *Internet-Underlays* and *HUB1/HUB2* SD-WAN Zones in our policies, when an interface is into an SD-WAN Zone we cannot use it directly into FW Policies, if instead you try port1/port2 the installation will fail.

### Install

!!! note "Time to Install!"

    Use the **Install Wizard** to Install policy packages **HUBs-LAT-PP** & **SPKs-LAT-PP**.

1. Navigate back to **Device Manager -> Device & Groups**

    ![IMG](../images/06/img45.jpeg){ width="600" }

    Click **Install Wizard**

    ???+ tip

        It's recommended to always click on **Install Preview** when using the Install Wizard to validate the configuration being pushed.

1. Set

    - **Install Policy Package & Device Settings**
    - **Policy Package**: *HUBs-LAT-PP*
    - **Create ADOM Revision:** *disabled*

    Click **Next**

    ![IMG](../images/06/install_wizard_01-e.png){ width="600" }

    Click **Next** when you see the 2 HUB devices.

    ![IMG](../images/06/install_wizard_02-e.png){ width="600" }

    Optional Click **Install Preview**, review then **Close**

    ![IMG](../images/06/install_wizard_03-e.png){ width="600" }

    Click **Install**

1. Everything should Install Successfully,  

    ![IMG](../images/06/img48-e.png){ width="600" }

    Click **Finish**

    !!! abstract "Your time to shine!"

        Repeat the **Install Wizard** to install **SPKs-LAT-PP** Policy Package

1. Make sure Config Status is **Synchronized**

    ![IMG](../images/06/img62.jpeg){ width="800" }
