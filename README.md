# /IOTCONNECT Enablement Directory

Welcome to the **/IOTCONNECT** enablement directory! This top-level page helps you quickly navigate our repositories, examples, and SDKs. We’ve grouped everything by **Language** and by **/IOTCONNECT Enabled Hardware Examples**. Additionally, we leverage **GitHub Topics** to make finding relevant projects even easier.

---

## Table of Contents

1. [Quick Links](#quick-links)  
2. [Languages](#languages)  
   - [C / C++](#c--c)  
   - [Python](#python)  
   - [C# / .NET](#c--net)  
   - [Node.js](#nodejs)  
   - [Swift (iOS)](#swift)  
   - [Java / Kotlin (Android)](#java)  
3. [/IOTCONNECT Enabled Hardware Examples](#iotconnect-enabled-hardware-examples)  
4. [Searching / Filtering by Tags](#searching--filtering-by-tags)  
5. [Additional Resources](#additional-resources)  
6. [Contributing](#contributing)  
7. [Need Help?](#need-help)  
8. [Revision Info](#revision-info)

---

## Quick Links

- **[/IOTCONNECT Docs](https://docs.iotconnect.io/)**  
  Deep dives into /IOTCONNECT features like device management, OTA, rule engines, and more.

- **[SDK Overview & Workflow](https://docs.iotconnect.io/iotconnect/sdk/sdk-understanding-and-workflow/)**  
  Understand how each SDK works, from device registration and telemetry to commands and cloud configuration.

- **[SDK Flavors](https://docs.iotconnect.io/iotconnect/sdk/sdk-flavors/)**  
  Explore different /IOTCONNECT SDK editions for various performance and footprint requirements.

---

## Languages

### C / C++<img src="https://www.kindpng.com/picc/m/403-4039227_c-language-logo-png-transparent-png.png" height="50" alt="C / C++" style="vertical-align: middle; margin-left: 8px;" />

#### [iotc-c-lib](https://github.com/avnet-iotconnect/iotc-c-lib)
- **Description**: The core C library forming the foundation for /IOTCONNECT in C.  
- **Use Cases**: Start here if you’re integrating /IOTCONNECT directly into your C/C++ application.  
- **Topics**:  <!-- START:iotc-c-lib-topics --> iotconnect, iot, mqtt <!-- END:iotc-c-lib-topics -->

#### [iotc-generic-c-sdk](https://github.com/avnet-iotconnect/iotc-generic-c-sdk)
- **Description**: Generic C SDK providing a reference implementation of /IOTCONNECT client functionality.  
- **Use Cases**: Easily adapt or extend for different C-based platforms and hardware.  
- **Topics**:  <!-- START:iotc-generic-c-sdk-topics --> iotconnect-sdk, aws, azure <!-- END:iotc-generic-c-sdk-topics -->

#### [iotc-yocto-c-sdk](https://github.com/avnet-iotconnect/iotc-yocto-c-sdk)
- **Description**: A Yocto-compatible C SDK for /IOTCONNECT, integrating easily into embedded Linux builds.  
- **Use Cases**: Automated builds for IoT devices running Yocto-based Linux.  
- **Topics**:  <!-- START:iotc-yocto-c-sdk-topics --> aws, azure, iotconnect-sdk <!-- END:iotc-yocto-c-sdk-topics -->

---

### Python<img src="https://www.python.org/static/img/python-logo.png" height="50" alt="Python" style="vertical-align: middle; margin-left: 8px;" />

#### [iotc-python-sdk](https://github.com/avnet-iotconnect/iotc-python-sdk)
- **Description**: Full-featured Python SDK for /IOTCONNECT.  
- **Use Cases**: Desktop, server, or embedded Linux for straightforward device-to-cloud integrations.  
- **Topics**:  <!-- START:iotc-python-sdk-topics --> sw, aws, azure, iotconnect-sdk <!-- END:iotc-python-sdk-topics -->

#### [iotc-python-lite-sdk](https://github.com/avnet-iotconnect/iotc-python-lite-sdk)
- **Description**: Lite/minimalist Python SDK for resource-constrained environments.  
- **Use Cases**: IoT devices with limited memory or CPU resources.  
- **Topics**:  <!-- START:iotc-python-lite-sdk-topics --> None <!-- END:iotc-python-lite-sdk-topics -->

#### [meta-iotc-sdk-lite](https://github.com/avnet-iotconnect/meta-iotc-sdk-lite)
- **Description**: Meta-layer integration of the “lite” Python SDK for Yocto-based Linux.  
- **Use Cases**: Building images for embedded platforms via Yocto, pre-integrated with /IOTCONNECT.  
- **Topics**:  <!-- START:meta-iotc-sdk-lite-topics --> None <!-- END:meta-iotc-sdk-lite-topics -->

#### [iotc-yocto-python-sdk](https://github.com/avnet-iotconnect/iotc-yocto-python-sdk)
- **Description**: A Yocto-compatible Python SDK for /IOTCONNECT, integrating easily into embedded Linux builds.  
- **Use Cases**: Automated Python-based builds for devices running Yocto.  
- **Topics**:  <!-- START:iotc-yocto-python-sdk-topics --> aws, azure, iotconnect-sdk <!-- END:iotc-yocto-python-sdk-topics -->

---

### C# / .NET<img src="https://learn.microsoft.com/en-us/dotnet/media/logo_csharp.png" height="50" alt="C# / .NET" style="vertical-align: middle; margin-left: 8px;" />

#### [iotc-dotnet-sdk](https://github.com/avnet-iotconnect/iotc-dotnet-sdk/tree/master-21)
- **Description**: .NET SDK enabling /IOTCONNECT capabilities primarily via C#.  
- **Use Cases**: Windows or Linux .NET environments, Azure Sphere, etc.  
  - *(Note: .NET can interface with C++/CLI, but this repo is mainly intended for C# use.)*  
- **Topics**:  <!-- START:iotc-dotnet-sdk-topics --> sw, aws, azure, iotconnect-sdk <!-- END:iotc-dotnet-sdk-topics -->

---

### Node.js<img src="https://nodejs.org/static/logos/nodejsDark.svg" height="50" alt="Node.js" style="vertical-align: middle; margin-left: 8px;" />

#### [iotc-node-sdk](https://github.com/avnet-iotconnect/iotc-node-sdk/tree/master-std-21)
- **Description**: Official Node.js SDK for /IOTCONNECT.  
- **Use Cases**: Server-side or embedded JS runtimes on Linux, Windows, etc.  
- **Topics**:  <!-- START:iotc-node-sdk-topics --> sw, aws, azure, iotconnect-sdk <!-- END:iotc-node-sdk-topics -->

---

### Swift<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Swift_logo.svg/300px-Swift_logo.svg.png" height="50" alt="Swift (iOS)" style="vertical-align: middle; margin-left: 8px;" />

#### [iotc-ios-swift-sdk](https://github.com/avnet-iotconnect/iotc-ios-swift-sdk/tree/release/2.0.0)
- **Description**: Swift SDK to integrate /IOTCONNECT features on iOS devices.  
- **Use Cases**: iPhone or iPad applications requiring IoT telemetry, device provisioning, etc.  
- **Topics**:  <!-- START:iotc-ios-swift-sdk-topics --> mobile-app, ble-gateway <!-- END:iotc-ios-swift-sdk-topics -->

---

### Java<img src="https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Java_programming_language_logo.svg/182px-Java_programming_language_logo.svg.png" height="50" alt="Java / Kotlin (Android)" style="vertical-align: middle; margin-left: 8px;" />

#### [iotc-android-sdk](https://github.com/avnet-iotconnect/iotc-android-sdk)
- **Description**: Android SDK (Java/Kotlin) for /IOTCONNECT.  
- **Use Cases**: Mobile or IoT Edge devices running Android, collecting telemetry and interacting with /IOTCONNECT.  
- **Topics**:  <!-- START:iotc-android-sdk-topics --> aws, azure, mpu <!-- END:iotc-android-sdk-topics -->

---

## /IOTCONNECT Enabled Hardware Examples

The GitHub links below list hardware that has software available, working with **/IOTCONNECT** “out of the box.” You can expect to find:

- **QuickStart Guides**: Step-by-step instructions on board bring-up through cloud connectivity without writing code!  
- **Developer Guides**: Similar, but with more details on compiling from source.  
- **Demos**: Specific use-case/application demos.  
- **References**: Webinars, blog posts, or additional learning material.

**/IOTCONNECT is compatible with most ALL MPUs and MCUs by leveraging our various SDKs. If the specific product you're interested in is not listed, please see our [SDK Flavors](https://docs.iotconnect.io/iotconnect/sdk/sdk-flavors/) for instructions on how to integrate.**

<table>
  <thead>
    <tr>
      <td><a href="/partners/infineon/">Infineon</a></td>
      <td><a href="/partners/microchip/">Microchip</a></td>
      <td><a href="/partners/nxp/">NXP</a></td>
      <td><a href="/partners/renesas/">Renesas</a></td>
      <td><a href="/partners/st/">STMicroelectronics</a></td>
    </tr>
  </thead>
  <tr>
    <td><a href="/partners/infineon/"><img src="/partners/infineon/infineon-logo.png" height="60" alt="Infineon Logo"></a></td>
    <td><a href="/partners/microchip/"><img src="/partners/microchip/microchip-logo.png" height="60" alt="Microchip Logo"></a></td>
    <td><a href="/partners/nxp/"><img src="/partners/nxp/nxp-logo.png" height="60" alt="NXP Logo"></a></td>
    <td><a href="/partners/renesas/"><img src="/partners/renesas/renesas-logo.png" height="60" alt="Renesas Logo"></a></td>
    <td><a href="/partners/st/"><img src="/partners/st/st-logo.png" height="60" alt="ST Logo"></a></td>
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

- **[/IOTCONNECT Docs](https://docs.iotconnect.io/)**  
  In-depth guides for device management, OTA updates, rule engines, etc.

- **[/IOTCONNECT Portal](https://portal.iotconnect.io/)**  
  Configure, monitor, and manage all your connected devices from the cloud.

- **[SDK Flavors](https://docs.iotconnect.io/iotconnect/sdk/sdk-flavors/)**
  Compare different /IOTCONNECT SDK editions to match your performance or memory constraints.

---

## Contributing

We welcome contributions to expand or refine /IOTCONNECT enablement. To contribute:

1. **Fork** the relevant repo under [avnet-iotconnect](https://github.com/avnet-iotconnect).  
2. **Create** a new branch for your feature or fix.  
3. **Submit** a Pull Request with a clear explanation of your changes.

---

## Need Help?

- **Support**: [support@iotconnect.io](mailto:support@iotconnect.io)  
- **Docs & FAQ**: [docs.iotconnect.io](https://docs.iotconnect.io/)

> **Note**: /IOTCONNECT is designed to support **all device types**. These listings are simply starting points; if you don’t see your exact device or OS, you can adapt any of these SDKs or use our REST/MQTT APIs directly to get connected.

---

## Revision Info

![GitHub last commit](https://img.shields.io/github/last-commit/avnet-iotconnect/iotc-stm32-n6-demos?label=Last%20Commit)  

- View change to this repository: [Commit History](https://github.com/avnet-iotconnect/iotc-stm32-n6-demos/commits/main)  
- View changes to this document: [QUICKSTART.md](https://github.com/avnet-iotconnect/iotc-stm32-n6-demos/commits/main/doc/QUICKSTART.md)
