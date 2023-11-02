# 1. Introduction

This document provides a step-by-step-guide to program and evaluate the 
[B-U585I-IOT02A STM32U5 Discovery kit for IoT](https://www.st.com/en/evaluation-tools/b-u585i-iot02a.html) board 
with Trusted Firmware-M support on IoTConnect.

This guide currently only supports Windows 64-bit.

# 2. Required Software

* Download and install the [STM32CubeProgrammer for STM32](https://www.st.com/en/development-tools/stm32cubeprog.html) with the following notes:
  * Select version `2.10` (Other version are untested and not supported by this guide.)
  * Select the 64-bit version
  * Install to the default directory "C:\Program Files\\" (The config uses some .bat files which reference this location.)
* A serial console application, such as [Tera Term](https://ttssh2.osdn.jp/index.html.en), 
 or a browser application like [Google Chrome Labs Serial Terminal](https://googlechromelabs.github.io/serial-terminal/) configured per the screenshot below:  

![Tera Term Serial Settings](media/teraterm-settings.png "Tera Term Serial Settings")

# 3. Cloud Account Setup
**NOTE: If you have already created an IoTConnect Account, or were provided an account as part of a training or workshop, skip this section.**

If you need to create an account, a free 2-month subscription is available.
Please follow the 
[Creating a New IoTConnect Account](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/subscription/subscription.md)
guide and return to this guide once complete.

# 4. Firmware Setup

* Download one of the following firmware packages:
  * [WiFi 1.1.1](https://saleshosted.z13.web.core.windows.net/sdk/AzureRTOS/stm32u5-tfm-package-1.1.1.zip) - For connection to a WiFi network (Most Common)
  * [BG96 1.1.1](https://saleshosted.z13.web.core.windows.net/sdk/AzureRTOS/stm32u5-tfm-package-bg96-1.1.1.zip) - For connecting to a cellular network with the addition of a BG96 daughter board. (Follow the [BG96 Guide](BG96.md))
* Extract the package in a location that meets the following requirements to ensure compatibility with Windows batch files:
  * File path should not contain any spaces
  * File path should only contain alphanumeric characters and hyphens
  * File path should not be part of a synchronized location (e.g., OneDrive)
* Connect a USB cable to the Micro USB slot of the board.
* Execute the *trust-zone-enable.bat* batch script included in the package to enable the TrustZone feature which is required to run the next step.
Running this script will make it so that only TrustZone enabled applications are authorized to run on the board. This only needs to be run once per board.
* Execute the *tfm-update.bat* batch script included in the package to setup TFM on the board along with the IoTConnect firmware.
* Remove the USB cable from the board for a few seconds and reconnect to perform a hard reset.

# 5. Device Configuration
* Ensure the serial terminal application is running.
* Press the RST button on the board and look for the "X-CUBE-AZURE" title block. This may take 1 or two presses of the button. (The reset button is the black button labled "RST" next to the only blue button on the top of the board.)
* In your terminal application enter "y" when prompted to set device configuration. You will only need to set values 1-4.
  * Configure your WiFi SSID (Network Name) by pressing 1 (if running the WiFi version)
  * Configure your WiFi Password by pressing 2 (if running the WiFi version)
  * Set the values for your CPID and Environment by pressing 3 and 4 respectively. These values can be located 
in the IoTConnect WebUI on the *Key Vault* page. 
Navigate there using the image below:<br>
![Key Vault](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/assets/key_vault.png "Key Vault")
  * The DUID value should be left unset. A DUID unique to your device will be generated and displayed on the console during startup
  * The Symmetric key should be left unset. This will allow for authentication using STSAFE with x509 authentication
  * Press '0' to write the configuration. This option will also reset the board.
* After configuring the device settings, monitor the serial terminal for information similar to the screenshot below. You may have to scroll up in the terminal.<br>
![Certificate and DUID Screemshot](media/duid-and-certifciate-console.png "Certificate and DUID Screemshot") 
* A device fingerprint needs to be generated from the certificate.
  * Copy the Device Certificate from the console, including the BEGIN and END lines.
  * Paste the contents into the X509 Cert field at [this web site](https://www.samltool.com/fingerprint.php). (Optionally you can use openssl to print the device fingerprint, but this is outside the scope of this guide.)
  * Leave the "Algorithm" selection at the default SHA1, press "Calculate Fingerprint" and copy/save the Fingerprint field for later use.
* Copy the generated DUID displayed and save for later use.

# 6. IoTConnect Device Template Setup
**NOTE: If you are following this guide as part of a training or workshop, a device template may have already been created and this section can be skipped. Check if a template called "stm32u5ss" already exists in the template tab of the "Device" section.**

A Device Template with Self Signed authentication type will need to be imported or created.
* Download the premade [Device Template with Self-Signed Auth](templates/device/stm32u5self_signed_template.JSON).
* Import the template into your IoTConnect instance. (A guide on [Importing a Device Template](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/import_device_template.md) is available or for more information on [Template Management](https://docs.iotconnect.io/iotconnect/user-manuals/devices/template-management/), please see the [IoTConnect Documentation](https://iotconnect.io) website.)

# 7. IoTConnect Device Setup
* Create a new device in the IoTConnect portal. (Follow the [Create a New Device](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/create_new_device.md) guide for a detailed walkthrough.)
* Enter the DUID saved from earlier into the *Unique ID* field and enter a descriptive *Display Name* of your choice.
* Select the template from the dropdown box that was just imported.
* Enter the Fingerprint calculated in the "Device Configuration" step into the Thumbprint field.
* Click Save and press the Reset button.

# 8. Verification
At this point the board should be sending telemetry to the IoTConnect portal. We can verify by checking the "Live Data" feed.
* Return to the *Devices* page and click on the newly created Device ID.
* On the left sub-menu, click "Live Data" and after a few seconds, data should be shown. See below:<br>![image](https://github.com/avnet-iotconnect/iotc-azurertos-sdk/assets/40640041/21d25bbb-71d0-4a9d-9e74-e2acf0983183)

# 9. Visualization
The telemetry can be visualized by using the Dynamic Dashboard feature of IoTConnect.  A sample dashboard that is preconfigured to display some telemtery from the STM32U5 IoT Discovery Kit is available for download [here](templates/dashboards/stm32u5_quickstart_dashboard_export.json).  Once downloaded, select "Create Dashboard" from the top of the IoTConnect portal and then choose the "Import Dashboard" option and select the template and device name used previously in this guide.

# 10. Troubleshooting
Using the serial terminal is the best way to identify issues. Common issues can be resolved by verifying the following items:
* Output stopping with a message about "IP Address":  Ensure valid WiFI credentials are used and that the network has an operational DHCP server.
* Output stopping before data is sent:  Verify CPID and Environment names.
* Output stopping with "No Device Found":  Ensure a new device was created in the portal and that the DUID matches the Device ID
* When flashing the board for the first time, you may encounter an error *Error while initializing the security counter*. In that case, reset the board. 
* A firmware update with *tfm-update.bat* may fail with an error *[ERR] Unable to find bootable image* during startup. Running *tfm-update.bat* and then *trust-zone-enable.bat* again should clear the error.
* After an update, you may see an error in the log *[ERR] Error while initializing the security counter*. Simply resetting the board should clear the error.
* A blank screen may appear after flashing. The following steps may recover the board:
  * Erase the board using the full chip erase option using the STM32CubeProgrammer GUI.
  * Run *trust-zone-disable.bat* and then *trust-zone-enable.bat* again.
  * Flash the board again with *tfm-update.bat*.
