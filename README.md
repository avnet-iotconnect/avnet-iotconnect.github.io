# IoTConnect Enablement Directory

Welcome to the **IoTConnect** enablement directory! This top-level page helps you quickly navigate our repositories, examples, and SDKs. We’ve grouped everything into three primary categories:

1. [Language](#language)  
2. [Operating System (OS)](#operating-system)  
3. [Manufacturer / Supplier](#manufacturer)

Additionally, we leverage **tags** (GitHub topics) to make finding relevant projects even easier.

---

## Quick Links

- **[IoTConnect Docs](https://docs.iotconnect.io/)**  
  Explore official documentation for deep dives into IoTConnect features, including device management, OTA, and rule engines.

- **[SDK Overview & Workflow](https://docs.iotconnect.io/iotconnect/sdk/sdk-understanding-and-workflow/)**  
  Understand how each SDK works, from device registration and telemetry to commands and cloud configuration.

- **[SDK Flavors](https://docs.iotconnect.io/iotconnect/sdk/sdk-flavors/)**  
  Learn about different editions of IoTConnect SDKs, each tailored for specific performance or footprint requirements.

---

## 1. Language

Below are the primary repositories categorized by **programming language**. In many cases, they’re cross-platform and can run on multiple OSes, but this section focuses on the language-specific libraries and examples.

### Python

- **[iotc-py](https://github.com/avnet-iotconnect/iotc-py)**  
  - **Description**: Full-featured Python SDK for IoTConnect.  
  - **Tags**: `python`, `sdk`, `iotconnect`  
  - **Use Cases**: Desktop, server, or embedded Linux environments for straightforward device-to-cloud integrations.

- **[iotc-phyt](https://github.com/avnet-iotconnect/iotc-phyt)**  
  - **Description**: Lite/minimalist Python SDK for resource-constrained environments.  
  - **Tags**: `python`, `lightweight-sdk`, `iotconnect`  
  - **Use Cases**: IoT devices with limited memory or CPU resources.

### Node.js (JavaScript/TypeScript)

- **[iotc-npm](https://github.com/avnet-iotconnect/iotc-npm)**  
  - **Description**: Official Node.js SDK for IoTConnect, also on NPM.  
  - **Tags**: `javascript`, `typescript`, `node.js`, `sdk`  
  - **Use Cases**: Server-side or embedded JS runtimes on Linux, Windows, etc.

- **[iotc-node-labs](https://github.com/avnet-iotconnect/iotc-node-labs)**  
  - **Description**: Example projects/labs showcasing Node.js IoTConnect usage.  
  - **Tags**: `javascript`, `examples`, `iotconnect`  
  - **Use Cases**: Quick starts, proof-of-concepts, and code snippets.

### .NET (C#)

- **[iotc-dotnet-labs](https://github.com/avnet-iotconnect/iotc-dotnet-labs)**  
  - **Description**: Example .NET projects for connecting C# apps to IoTConnect.  
  - **Tags**: `c#`, `.net`, `dotnet`, `iotconnect`  
  - **Use Cases**: Windows or Linux .NET environments, Azure Sphere, etc.

### Java

- **Coming Soon**  
  - We will add a dedicated Java repository soon. In the meantime, developers can still integrate IoTConnect using our REST or MQTT APIs, or by adapting other SDKs.  
  - **Tags**: `java`, `mqtt`, `rest`, `iotconnect`

### C/C++

- **[iotc-c-lib](https://github.com/avnet-iotconnect/iotc-c-lib)**  
  - **Description**: The **core C library** forming the foundation for IoTConnect in C/C++.  
  - **Tags**: `c`, `library`, `iotconnect`  
  - **Use Cases**: Start here if you’re integrating IoTConnect directly into your C/C++ application.

- **[iotconnect-arduino](https://github.com/avnet-iotconnect/iotconnect-arduino)**  
  - **Description**: Arduino-based library and sample code.  
  - **Tags**: `arduino`, `c++`, `embedded`, `iotconnect`  
  - **Use Cases**: Quick prototyping on Arduino-compatible boards.

- **[iotc-stm](https://github.com/avnet-iotconnect/iotc-stm)**  
  - **Description**: STM microcontroller integrations/examples.  
  - **Tags**: `stm32`, `c`, `embedded`, `iotconnect`  
  - **Use Cases**: STM32-based designs leveraging the `iotc-c-lib`.

- **[iotc-nxp](https://github.com/avnet-iotconnect/iotc-nxp)**  
  - **Description**: NXP MCU/MPU enablement.  
  - **Tags**: `nxp`, `c`, `embedded`, `iotconnect`  
  - **Use Cases**: Boards built on NXP chipsets.

- **[iotc-esp32-samples](https://github.com/avnet-iotconnect/iotc-esp32-samples)**  
  - **Description**: ESP32 example projects in C/C++.  
  - **Tags**: `esp32`, `c++`, `embedded`, `iotconnect`  
  - **Use Cases**: Wi-Fi or BLE devices using Espressif’s ESP32.

- **LoRa/LoRaWAN**  
  - **[iotc-lorawan-labs / iotc-lora-labs](https://github.com/avnet-iotconnect?tab=repositories&q=lorawan)**  
    - **Description**: LoRa/LoRaWAN labs and examples.  
    - **Tags**: `lora`, `lorawan`, `c`, `iotconnect`  
    - **Use Cases**: Low-power, long-range connectivity.

---

## 2. Operating System

While many repositories above work across multiple OSes, some are specifically designed or tested for certain environments. Here are the primary OS-oriented resources:

- **Yocto Meta Layer**  
  - **[iotc-meta-avnet](https://github.com/avnet-iotconnect/iotc-meta-avnet)**  
    - **Description**: A Yocto “meta” layer embedding IoTConnect support (often via `iotc-c-lib` or Python).  
    - **Tags**: `yocto`, `meta-layer`, `linux`, `iotconnect`  
    - **Use Cases**: Customized embedded Linux builds using the Yocto Project.

- **Linux**  
  - Most of our **Python**, **Node.js**, and **C/C++** SDKs (e.g., `iotc-c-lib`) are designed to run on generic Linux distributions.  
  - **Search by Tag**: On GitHub, look for repositories tagged with `linux` or `embedded-linux`.

- **Windows**  
  - The **[iotc-dotnet-labs](https://github.com/avnet-iotconnect/iotc-dotnet-labs)** is validated on Windows systems for .NET applications.  
  - **Search by Tag**: `windows`, `.net`

- **FreeRTOS / Other Embedded OS**  
  - Repos like **iotc-stm** or **iotc-nxp** may include FreeRTOS-based examples.  
  - **Search by Tag**: `freertos`, `rtos`, `embedded`.

- **Android**  
  - While no dedicated Android repo is currently published, Node.js or Java integrations can be adapted for Android.  
  - **Search by Tag**: `android`, `java`, `typescript`

---

## 3. Manufacturer

If you’re working with a specific **supplier** or board manufacturer, you can find targeted references and support material in our **Partners** directory and related repos:

- **[Partner Directory](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/tree/main/partners)**  
  Inside, you’ll find guides, board definitions, and specialized libraries for suppliers such as:
  - **NXP**  
  - **STMicroelectronics**  
  - **Renesas**  
  - **Telit**  
  - **Azure Sphere**  
  - ...and others

In addition, many of our example repositories include manufacturer-specific naming in their titles or tags (e.g., `iotc-nxp`, `iotc-stm`, `nxp`, `st`, etc.).

---

## Using Tags

To **quickly filter** across all repositories under [avnet-iotconnect](https://github.com/avnet-iotconnect), use **tags** (also called GitHub “topics”). For example:

- Go to the [avnet-iotconnect Repositories Page](https://github.com/avnet-iotconnect?tab=repositories).  
- Click the “**Type**” dropdown, then select “**All**” or “**Public**”.  
- In the “**Search or jump to…**” field, type a topic such as `tag:python` or `tag:freertos`.  
- You’ll see only the repositories tagged accordingly.

Common tags used in our repositories:
- `python`, `c`, `c++`, `javascript`, `dotnet`, `embedded`, `windows`, `linux`, `freertos`, `yocto`, `st`, `nxp`, `esp32`, `iotconnect`, `iotc-c-lib`, etc.

---

## Additional Resources

- **[IoTConnect Docs](https://docs.iotconnect.io/)**  
  In-depth guides and references for device management, OTA updates, rule engines, and more.

- **[SDK Flavors](https://docs.iotconnect.io/iotconnect/sdk/sdk-flavors/)**  
  Compare different SDK editions and decide which one meets your performance or memory constraints.

- **[IoTConnect Portal](https://portal.iotconnect.io/)**  
  The cloud interface for configuring, monitoring, and managing all your connected IoT devices.

---

## Contributing

We welcome contributions to help expand or refine IoTConnect enablement. To contribute:

1. **Fork** the relevant repo under [avnet-iotconnect](https://github.com/avnet-iotconnect).  
2. **Create** a new branch for your feature or fix.  
3. **Submit** a Pull Request and include a clear explanation of your changes.

---

## Need Help?

- **Support**: [support@iotconnect.io](mailto:support@iotconnect.io)  
- **Docs & FAQ**: [docs.iotconnect.io](https://docs.iotconnect.io/)

> **Note**: IoTConnect is designed to support **all device types**. The listings here are starting points; if you don’t see your exact device or OS, you can adapt any of these SDKs or utilize our REST/MQTT APIs directly to get connected.
