---
hide:
  - navigation
  - toc
  - footer
---

# Content

<div class="grid cards" markdown>

-   ![SD-WAN](images/SD-WAN.svg){style="width: 52.8px; vertical-align: middle;"} __[SD-WAN<br>The Evolution of the WAN Edge](workshop_01/index.md)__

    ---

    In this lab, you will use FortiManager Overlay Template to create an SD-WAN for an Active - Active Datacenter, you will also interconnect the Datacenters in a way one can use inter-dc specific connectivity to provide access to the other DC in case of full external links failure.

    At the end of the lab (if you have time) you will perform various test to see how your SD-WAN behaves under different failure scenarios, it will also be serve as learning opportunity to learn important troubleshooting commands.

    ***Products covered in this session:***

    - **FortiGate 7.6**
    - **FortiManager 7.6**
    - **FortiAnalyzer 7.6**

-   ![FortiSwitch](images/FortiSwitch.svg){style="width: 52.8px; vertical-align: middle;"} __[FortiSwitch & FortiLink<br>Secure Access Architecture](workshop_02/index.md)__

    ---

    In this workshop, students will learn how to use **FortiManager** to deploy and manage **FortiSwitch** environments in a structured and practical way. The focus is not only on getting the configuration done, but also on understanding how the topology behaves and how to validate it from the CLI.
 
    Throughout the lab, students will work with key topics such as **FortiLink**, **MC-LAG**, **FortiLink over Layer 3**,FortiLink Over a VXLAN Interface, switch templates, custom commands, and basic troubleshooting. By the end of the workshop, they should be comfortable bringing switches online, building the required configuration from FortiManager, and verifying that the design is working as expected.

    ***Products covered in this session:***

    - **FortiManager 7.6**
    - **FortiGate 7.6**
    - **FortiSwitch VM v7 build 6216**

-   ![SASE](images/FortiSASE.svg){style="width: 52.8px; vertical-align: middle;"} __[FortiSASE<br>Securing the Hybrid Workforce](workshop_03/index.md)__

    ---

    In this lab, you will build a full FortiSASE deployment by starting with strong identity foundations and endpoint posture, integrating SAML authentication and shaping how devices behave both on and off the corporate network. From there, you will enforce layered protection for internet access combining threat prevention, SSL inspection, CASB controls, and advanced DLP (including controls for modern SaaS and LLM usage) while also gaining operational visibility through logs, analytics, and endpoint telemetry.
    
    As the environment evolves, you will extend secure access to private applications by integrating SPA with SD-WAN, enabling performance monitoring, and securely connecting branch locations. You will then move into a Zero Trust model, delivering controlled access for users and contractors through both agent-based and agentless approaches, enhancing visibility with Digital Experience Monitoring, and exploring automation and centralized management. By the end, you will have translated SASE concepts into an integrated security architecture that balances access, control, and user experience.

    ***Products covered in this session:***

    - **FortiSASE v26.1.2 Feature**
    - **FortiGate 7.6**
    - **FortiManager 7.6**

-   ![Wireless](images/Wireless.svg){style="width: 52.8px; vertical-align: middle;"} __[Wireless Best Practices<br>Toward AI-Driven Network Operations](workshop_04/index.md)__

    ---

    This training material provides a comprehensive guide to wireless networking best practices and Fortinet’s advanced Wi-Fi architecture. It covers essential RF design principles, emphasizing that a strong physical design accounts for up to 80% of deployment success. The content also explores roaming mechanics, systematic troubleshooting approaches, and Wi-Fi 7 (802.11be) capabilities introduced with the new FortiAP K-Series hardware.
    It also delivers a comprehensive understanding of FortiAIOps and AI-driven ARRP. FortiAIOps leverages supervised machine learning and generative AI to transform network operations from reactive troubleshooting to proactive, self-healing assurance. The AI-ARRP feature specifically automates wireless channel optimization across FortiAPs. The AI engine evaluates and scores available channels by analyzing real-time RF conditions—such as noise levels, channel utilization, interfering APs, and spectral RSSI—combined with up to two weeks of historical data.
    Its automated four-step workflow includes continuous data collection, daily performance forecasting, strict schedule validation (including regulatory compliance and SLA checks), and the final deployment of optimized channel settings to the FortiGate controller. Ultimately, this intelligence reduces Mean Time to Resolution (MTTR) and maximizes enterprise network reliability.

    ***Products covered in this session:***

    - **FortiOS**
    - **FortiAP**
    - **FortiAIOPs**

-   ![OS8](images/FortiGate.svg){style="width: 52.8px; vertical-align: middle;"} __[FortiOS 8.0 Innovations<br>Future-Ready Security Fabric](workshop_05/index.md)__

    ---

    The security landscape is shifting faster than ever. Quantum computing is on the horizon, AI‑driven applications are flooding networks, and organizations are relying on SaaS and distributed connectivity in ways that didn’t exist a few years ago.  
 
    In this lab, you’ll step into that future. We’ll start with FortiOS’s new Post‑Quantum Cryptography capabilities—your first look at the algorithms designed to protect VPNs against tomorrow’s quantum‑enabled threats. From there, we’ll dive into the enhanced Security Profiles that bring enhanced visibility and control to GenAI and SaaS applications, helping you manage technologies that are evolving at faster than ever before.
    
    You’ll also explore the latest SD‑WAN improvements, from smarter WAN monitoring to deeper application performance insights, giving you the tools to keep distributed environments running smoothly. Then we’ll simplify secure access with the simplified ZTNA configuration and the new ZTNA Service Connector, which strengthens protection without exposing backend services.
    
    We’ll wrap up by zooming out to the bigger picture—new capabilities in FortiManager and FortiAnalyzer that streamline operations, sharpen analytics, and tie the entire Security Fabric together.

    ***Products covered in this session:***

    - **FortiGate 8.0**

    - **FortiManager 8.0**

    - **FortiAnalyzer 8.0**


-   ![Agenda](images/FortiManager.svg){style="width: 52.8px; vertical-align: middle;"} __[Agenda](#)__

    ---

    ???+ abstract "Agenda: Day 1"
        | Time               | Description                |
        | :----------------  | :------------------------- |
        | **Morning**        | SD-WAN and the Evolution of the WAN Edge            |
        | **Afternoon**      | FortiSwitch & FortiLink: Secure Access Architecture |

    ???+ abstract "Agenda: Day 2"
        | Time               | Description                |
        | :----------------  | :------------------------- |
        | **All Day**        | FortiSASE: Securing the Hybrid Workforce |

    ???+ abstract "Agenda: Day 3"
        | Time               | Description                |
        | :----------------  | :------------------------- |
        | **Morning**        | Wireless Best Practices: Toward AI-Driven Network Operations |
        | **Afternoon**      | FortiOS 8.0 Innovations: Future-Ready Security Fabric        |


-   ![Resources](images/Agreement.svg){style="width: 52.8px; vertical-align: middle;"} __[Resources](#)__

    ---

    !!! tip "Presentation Slides"
        - [SD-WAN](./files/xp26_sdwan.pdf)
        - [FortiSwitch](./files/xp26_fsw.pdf)
        - [FortiSASE](./files/xp26_sase.pdf)
        - Coming soon

    !!! example "Lab Guides"
        - Coming soon

</div>

<link rel="stylesheet" href="/landing-page.css">