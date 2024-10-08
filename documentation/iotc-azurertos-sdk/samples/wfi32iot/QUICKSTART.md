## 1. Introduction

This document provides instructions on how to quickly connect the [WFI32-IoT](https://www.microchip.com/en-us/development-tool/ev36w50a) development board to Avnet's [IoTConnect](https://www.avnet.com/wps/portal/us/solutions/iot/iotconnect) platform without the need to compile any code from source. The guide further leverages [MikroE](https://www.mikroe.com/) click boards featuring [TE Connectivity](https://www.te.com/en/products/sensors.html) sensors. 
### Key Features:
* The built-in ATECC608 secure element is utilized to enable a secure connection to IoTConnect.
* The Temperature and Light Sensor telemetry are supported.
* Device-to-cloud commands are supported using the on-board switches (SW1 & SW2).
* Althought not required, further telemetry can be visualized by adding Click boards (see below).

The Click board interface makes it possible to make use of hundreds of different Click boards from MikroE.
The following boards are directly supported and send sensor readings directly to IoTConnect:  
* [VAV Press Click](https://www.mikroe.com/vav-press-click)
* [Ultra-Low Press Click](https://www.mikroe.com/ultra-low-press-click)
* [PHT Click](https://www.mikroe.com/pht-click)
* [TEMP&HUM 14 click](https://www.mikroe.com/temphum-14-click)
* [Air Quality 7 click](https://www.mikroe.com/air-quality-7-click)
* [Altitude 4 Click](https://www.mikroe.com/altitude-4-click)
* [Altitude 2 Click](https://www.mikroe.com/altitude-2-click)
* [Telaire T6713 CO2 Sensor Module](https://www.amphenol-sensors.com/en/telaire/co2/525-co2-sensor-modules/3399-t6713) on the [PROTO Click](https://www.mikroe.com/proto-click)
* [Telaire T9602 IP67 Harsh Environment Humidity & Temperature Sensor](https://www.amphenol-sensors.com/en/telaire/humidity/527-humidity-sensors/3224-t9602) on the [Terminal 2 Click](https://www.mikroe.com/terminal-2-click)

## 2. Hardware Setup

### Setup Clicks  
> [!NOTE]
> The MikroE Click hardware is not required to complete this guide, so if none are present, skip this section.

* Plug a Click board into onto Click interface on the WFI32-IoT board ensuring that the pin labels match the header markings.
* To connect up to 4 Click boards at the same time, purchase the [Shuttle Click](https://www.mikroe.com/shuttle-click) adapter.

### Setup WFI32-IoT Board  
* Connect the WFI32-IoT board to a USB port on your PC via the Micro USB cable.
* Once the board boots up, driver installation for a Mass Storage USB device may appear. 
  * Optionally, connect a terminal program (like TeraTerm) to one of the two COM ports
which is named "USB Serial". Use defaults for 115200 baud: 8 bits, 1 stop bit, no flow control or parity. Firmware logs will be available on that COM port. 
  * After a short time, a new removable drive will appear in the Windows Explorer.

## 3. Programming the Firmware

* Download and install **v6.05** of the [MPLAB X IDE package](https://www.microchip.com/en-us/tools-resources/archives/mplab-ecosystem) (Newer versions have not been tested and may not be compatible).
  * "MPLAB IPE" and "32-bit device support" are the only required options during the installation.
* Download the firmware binary package [iotconnect-demo-wfi32-042423.zip](https://saleshosted.z13.web.core.windows.net/sdk/AzureRTOS/iotconnect-demo-wfi32-042423.zip)
* Extract the iotconnect-demo.X.production.hex file and take note of the location
* Open the Microchip IPE application to program the firmware: 
  * In the **Device** entry box, select "WFI32E01"
  * In the **Tool** entry box, select "Curiosity/Starter Kits (PKBO4)"
  * Click the **Connect** button
  * Wait for any updates to complete and ignore any DFP related warnings in the output.
  * After the device is connected, updated, and verified (as reported in the output), click the **Browse** button next to the **Hex file** field and select the iotconnect-demo.X.production.hex file that was extracted previously.
  * Click the **Program** button.
  * The screenshot below shows an example of what the IPE displays if the device has been programmed successfully:

![IPE Screenshot](assets/ipe.png "IPE Screenshot")

## 4. IoTConnect Account Setup
An IoTConnect account is required.  If you need to create an account, a free trial subscription is available:

* [IoTConnect Trial (Azure version)](https://subscription.iotconnect.io/subscribe?cloud=azure)  
![IoTConnect on Azure](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/subscription/media/iotc-azure.png)
> [!NOTE]
> Be sure to check any SPAM folder for the temporary password after registering.

See the IoTConnect [Subscription Information](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/subscription/subscription.md) for more details on the trial.

## 5. IoTConnect Device Template Setup
A Device Template with Self Signed authentication type will need to be imported.
* Download the premade device template [wfi32iot_device_template.JSON](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotc-azurertos-sdk/samples/wfi32iot/templates/device/wfi32iot_device_template.JSON?raw=1) (**MUST** Right-Click and "Save-As" to get the raw json file)
* Import the template into your IoTConnect instance. (A guide on [Importing a Device Template](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/import_device_template.md) is available or for more information, please see the [IoTConnect Documentation](https://docs.iotconnect.io/iotconnect/) website.)

## 6. IoTConnect Device Setup
* Create a new device in the IoTConnect portal. (Follow the [Create a New Device](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/create_new_device.md) guide for a detailed walkthrough.)
* Select the template from the dropdown box that was just imported (or provided to you).
* Navigate to the Mass Storage Device (WFI32-IOT) in the Windows Explorer under "This PC"
* Locate the device certificate file named "snXXXXXX_device.pem" and copy the "snXXXXXXXX" portion (do not include the "__device.pem").  Enter this value into the *Unique ID* field and enter a descriptive *Display Name* of your choice.
* Select an *Entity* in the drop-down (on new/trial accounts, there will only be one option)
* In the "Device Certificate" section, click the **"Browse"** link and navigate back to and select the "snXXXXXX_device.pem" file.
* Click "Save & View"

## 7. Configuration
To configure the WiFi Credentials and IoTConnect Account environment information, two files on the USB Mass Storage Device need to be editited.

### Configure the WiFi Credentials
* The WiFi Credentials are configred in the WIFI.CFG file located on the MSD. Open the file in a text editor and input the WiFi credentials using one of the
following templates per the network configuration:
   - Open Unsecured Network (no password protection)
        ```bash
        CMD:SEND_UART=wifi MY_SSID,,1
        ```
    - Wi-Fi Protected Access 2 (WPA2) [Most Common]
        ```bash
        CMD:SEND_UART=wifi MY_SSID,MY_PSWD,2
        ```
    - Wired Equivalent Privacy (WEP)
        ```bash
        CMD:SEND_UART=wifi MY_SSID,MY_PSWD,3
        ```
    - Wi-Fi Protected Access 3 (WPA3)
        ```bash
        CMD:SEND_UART=wifi MY_SSID,MY_PSWD,4
        ```
* Save the file when done.

### Configure the IoTConnect Account
* Open the CLOUD.CFG file in a text editor. If the contents of CLOUD.CFG do not have text like CPID and ENV, 
delete the file, eject the drive, reset the board and re-open the file as resetting will populate the defaults.
* Set the CPID and Environment per your IoTConnect account settings, which can be found in Settings -> Key Vault in the IoTConnect portal.
* The DUID and SYMMETERIC_KEY can be let empty.
* Save the file and reset the board.
* The device should connect to the specified IoTConnect account and publish sensor data periodically.

## 8. Visualization
The telemetry can be visualized by using the Dynamic Dashboard feature of IoTConnect. Some preconfigured dashboards templates are available download:
* [Microchip Centric Dashboard](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotc-azurertos-sdk/samples/wfi32iot/templates/dashboards/wfi32iot_quickstart_dashboard_export.json?raw=1) (**MUST** Right-Click and "Save-As" to get the raw json file).
* [TE Sensor Centric Dashboard](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotc-azurertos-sdk/samples/wfi32iot/templates/dashboards/TE_Sensors_Dashboard.json?raw=1) (**MUST** Right-Click and "Save-As" to get the raw json file).
* Once downloaded, select "Create Dashboard" from the top of the IoTConnect GUI and then choose the "Import Dashboard" option and select the template and device name used previously in this guide.

## 9. Sending Commands
* The board has 3 LEDs that can be toggled on and off by using the "on" or "off" parameter in conjunction with one of the LED commands.
* The board also has two buttons (across from the RST button) which increment a counter when pressed.  The counters can be reset by using the "reset-counters" command with a parameter of "1".
![Send Commands](assets/send_commands.png)
