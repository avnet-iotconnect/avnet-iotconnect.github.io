# IoTConnect Enablement Directory

Welcome to the **IoTConnect** enablement directory! This top-level page helps you quickly navigate our repositories, examples, and SDKs. We’ve grouped everything by **Language** and by **/IOTCONNECT Enabled Hardware Examples**. Additionally, we leverage **GitHub Topics** to make finding relevant projects even easier.

---

## Quick Links

- **[IoTConnect Docs](https://docs.iotconnect.io/)**  
  Deep dives into IoTConnect features like device management, OTA, rule engines, and more.

- **[SDK Overview & Workflow](https://docs.iotconnect.io/iotconnect/sdk/sdk-understanding-and-workflow/)**  
  Understand how each SDK works, from device registration and telemetry to commands and cloud configuration.

- **[SDK Flavors](https://docs.iotconnect.io/iotconnect/sdk/sdk-flavors/)**  
  Explore different IoTConnect SDK editions for various performance and footprint requirements.

---

## Languages

### C / C++

#### [iotc-c-lib](https://github.com/avnet-iotconnect/iotc-c-lib)
- **Description**: The core C library forming the foundation for IoTConnect in C.  
- **Use Cases**: Start here if you’re integrating IoTConnect directly into your C/C++ application.  
- **Tags**:  
  <!-- START:iotc-c-lib-topics -->
  <!-- END:iotc-c-lib-topics -->

#### [iotc-generic-c-sdk](https://github.com/avnet-iotconnect/iotc-generic-c-sdk)
- **Description**: Generic C SDK providing a reference implementation of IoTConnect client functionality.  
- **Use Cases**: Easily adapt or extend for different C-based platforms and hardware.  
- **Tags**:  
  <!-- START:iotc-generic-c-sdk-topics -->
  <!-- END:iotc-generic-c-sdk-topics -->

#### [iotc-yocto-c-sdk](https://github.com/avnet-iotconnect/iotc-yocto-c-sdk)
- **Description**: A Yocto-compatible C SDK for IoTConnect, integrating easily into embedded Linux builds.  
- **Use Cases**: Automated builds for IoT devices running Yocto-based Linux.  
- **Topics**:  <!-- START:iotc-yocto-c-sdk-topics --> <!-- END:iotc-yocto-c-sdk-topics -->

---

### Python

#### [iotc-python-sdk](https://github.com/avnet-iotconnect/iotc-python-sdk)
- **Description**: Full-featured Python SDK for IoTConnect.  
- **Use Cases**: Desktop, server, or embedded Linux for straightforward device-to-cloud integrations.  
- **Tags**:  
  <!-- START:iotc-python-sdk-topics -->
  <!-- END:iotc-python-sdk-topics -->

#### [iotc-python-lite-sdk](https://github.com/avnet-iotconnect/iotc-python-lite-sdk)
- **Description**: Lite/minimalist Python SDK for resource-constrained environments.  
- **Use Cases**: IoT devices with limited memory or CPU resources.  
- **Tags**:  
  <!-- START:iotc-python-lite-sdk-topics -->
  <!-- END:iotc-python-lite-sdk-topics -->

#### [meta-iotc-sdk-lite](https://github.com/avnet-iotconnect/meta-iotc-sdk-lite)
- **Description**: Meta-layer integration of the “lite” Python SDK for Yocto-based Linux.  
- **Use Cases**: Building images for embedded platforms via Yocto, pre-integrated with IoTConnect.  
- **Tags**:  
  <!-- START:meta-iotc-sdk-lite-topics -->
  <!-- END:meta-iotc-sdk-lite-topics -->

#### [iotc-yocto-python-sdk](https://github.com/avnet-iotconnect/iotc-yocto-python-sdk)
- **Description**: A Yocto-compatible Python SDK for IoTConnect, integrating easily into embedded Linux builds.  
- **Use Cases**: Automated Python-based builds for devices running Yocto.  
- **Tags**:  
  <!-- START:iotc-yocto-python-sdk-topics -->
  <!-- END:iotc-yocto-python-sdk-topics -->

---

### C# / .NET

#### [iotc-dotnet-sdk](https://github.com/avnet-iotconnect/iotc-dotnet-sdk/tree/master-21)
- **Description**: .NET SDK enabling IoTConnect capabilities primarily via C#.  
- **Use Cases**: Windows or Linux .NET environments, Azure Sphere, etc.  
  - *(Note: .NET can interface with C++/CLI, but this repo is mainly intended for C# use.)*  
- **Tags**:  
  <!-- START:iotc-dotnet-sdk-topics -->
  <!-- END:iotc-dotnet-sdk-topics -->

---

### Node.js

#### [iotc-node-sdk](https://github.com/avnet-iotconnect/iotc-node-sdk/tree/master-std-21)
- **Description**: Official Node.js SDK for IoTConnect.  
- **Use Cases**: Server-side or embedded JS runtimes on Linux, Windows, etc.  
- **Tags**:  
  <!-- START:iotc-node-sdk-topics -->
  <!-- END:iotc-node-sdk-topics -->

---

### Swift (iOS)

#### [iotc-ios-swift-sdk](https://github.com/avnet-iotconnect/iotc-ios-swift-sdk/tree/release/2.0.0)
- **Description**: Swift SDK to integrate IoTConnect features on iOS devices.  
- **Use Cases**: iPhone or iPad applications requiring IoT telemetry, device provisioning, etc.  
- **Tags**:  
  <!-- START:iotc-ios-swift-sdk-topics -->
  <!-- END:iotc-ios-swift-sdk-topics -->

---

### Java / Kotlin (Android)

#### [iotc-android-sdk](https://github.com/avnet-iotconnect/iotc-android-sdk)
- **Description**: Android SDK (Java/Kotlin) for IoTConnect.  
- **Use Cases**: Mobile or IoT Edge devices running Android, collecting telemetry and interacting with IoTConnect.  
- **Tags**:  
  <!-- START:iotc-android-sdk-topics -->
  <!-- END:iotc-android-sdk-topics -->

---

## /IOTCONNECT Enabled Hardware Examples

The GitHub links below list hardware that has software available, working with **/IOTCONNECT** “out of the box.” You can expect to find:

- **QuickStart Guides**: Step-by-step instructions on board bring-up through cloud connectivity without writing code!  
- **Developer Guides**: Similar, but with more details on compiling from source.  
- **Demos**: Specific use-case/application demos.  
- **References**: Webinars, blog posts, or additional learning material.

> **TIP**  
> /IOTCONNECT is compatible with **nearly all** MPUs and MCUs via our various SDKs. If your product isn’t listed, see our [SDK Flavors](https://docs.iotconnect.io/iotconnect/sdk/sdk-flavors/) to learn how to integrate.

<table>
  <thead>
    <tr>
      <td><a href="/partners/infineon/readme.md">Infineon</a></td>
      <td><a href="/partners/microchip/readme.md">Microchip</a></td>
      <td><a href="/partners/nxp/readme.md">NXP</a></td>
      <td><a href="/partners/renesas/readme.md">Renesas</a></td>
      <td><a href="/partners/st/readme.md">STMicroelectronics</a></td>
    </tr>
  </thead>
  <tr>
    <td><a href="/partners/infineon/readme.md"><img src="/partners/infineon/infineon-logo.png" width="100" alt="Infineon Logo"></a></td>
    <td><a href="/partners/microchip/readme.md"><img src="/partners/microchip/microchip-logo.png" width="100" alt="Microchip Logo"></a></td>
    <td><a href="/partners/nxp/readme.md"><img src="/partners/nxp/nxp-logo.png" width="80" alt="NXP Logo"></a></td>
    <td><a href="/partners/renesas/readme.md"><img src="/partners/renesas/renesas-logo.png" width="120" alt="Renesas Logo"></a></td>
    <td><a href="/partners/st/readme.md"><img src="/partners/st/st-logo.png" width="60" alt="ST Logo"></a></td>
  </tr>
  <tr>
    <!-- Each cell can display tags pulled from the partner's readme or topics -->
    <td>
      <!-- START:infineon-partner-tags -->
      <!-- END:infineon-partner-tags -->
    </td>
    <td>
      <!-- START:microchip-partner-tags -->
      <!-- END:microchip-partner-tags -->
    </td>
    <td>
      <!-- START:nxp-partner-tags -->
      <!-- END:nxp-partner-tags -->
    </td>
    <td>
      <!-- START:renesas-partner-tags -->
      <!-- END:renesas-partner-tags -->
    </td>
    <td>
      <!-- START:st-partner-tags -->
      <!-- END:st-partner-tags -->
    </td>
  </tr>
</table>

---

## Searching / Filtering by Tags

1. Go to [avnet-iotconnect Repositories](https://github.com/avnet-iotconnect?tab=repositories).  
2. Type `topic:[tag]` in the search field (e.g., `topic:python`).  
3. GitHub shows only those repos tagged with that topic.

Common tags:
- `python`, `c`, `c++`, `javascript`, `dotnet`, `embedded`, `windows`, `linux`, `freertos`, `yocto`, `st`, `nxp`, `esp32`, `iotconnect`, `iotc-c-lib`, etc.

---

## Additional Resources

- **[IoTConnect Docs](https://docs.iotconnect.io/)**  
  In-depth guides for device management, OTA updates, rule engines, etc.

- **[IoTConnect Portal](https://portal.iotconnect.io/)**  
  Configure, monitor, and manage all your connected devices from the cloud.

- **[SDK Flavors](https://docs.iotconnect.io/iotconnect/sdk/sdk-flavors/)**
  Compare different SDK editions to match your performance or memory constraints.

---

## Contributing

We welcome contributions to expand or refine IoTConnect enablement. To contribute:

1. **Fork** the relevant repo under [avnet-iotconnect](https://github.com/avnet-iotconnect).  
2. **Create** a new branch for your feature or fix.  
3. **Submit** a Pull Request with a clear explanation of your changes.

---

## Need Help?

- **Support**: [support@iotconnect.io](mailto:support@iotconnect.io)  
- **Docs & FAQ**: [docs.iotconnect.io](https://docs.iotconnect.io/)

> **Note**: IoTConnect is designed to support **all device types**. These listings are simply starting points; if you don’t see your exact device or OS, you can adapt any of these SDKs or use our REST/MQTT APIs directly to get connected.
