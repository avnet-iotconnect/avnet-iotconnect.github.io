# Renesas CK-RX65N (blue PCB) Quick Start Guide

## 1. Prerequisites

* PC with Windows 10/11
* Internet connection for the PC
* Network cable for the Renesas board
* (2) USB-A to micro-USB cables <b>with data support</b>
* A serial terminal application such as [Tera Term](https://ttssh2.osdn.jp/index.html.en), or a browser application like [Google Chrome Labs Serial Terminal](https://googlechromelabs.github.io/serial-terminal/)

## 2. Download & Install Renesas Software

Follow the instructions to [setup the Renesas Envrionment](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotc-azurertos-sdk/samples/ck-rx65n/environment_setup.md), then return to this guide.

## 3. Download Pre-Built Binary
Download the QuickStart ELF (Executable and Linking Format) file which contains the pre-built binary:  
[ck-rx65n-basic-sample-cli.elf](https://saleshosted.z13.web.core.windows.net/sdk/renesas/ck-rx65n-qs/ck-rx65n-basic-sample-cli.elf)

## 4. IoTConnect Account Setup

> **Note:**  
> If you have already created an IoTConnect Account, or were provided an account as part of a training or workshop, skip this section.

If you need to create an account, a free 2-month subscription is available.  Please follow the [Creating a New IoTConnect Account](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/subscription/subscription.md) guide and return to this guide once complete.

## 5. IoTConnect Device Template Setup

> **Note:**  
> If you are following this guide as part of a training or workshop, a template has already been created and this section may be skipped.

An IoTConnect *Device Template* with Symmetric Key authentication type will need to be imported.
* Download the premade [Device Template with Symmetric Key Auth](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotc-azurertos-sdk/samples//ck-rx65n/templates/device/CK-RX65Nsk_template.JSON).
* Import the template into your IoTConnect instance. (A guide on [Importing a Device Template](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/import_device_template.md) is available or for more information on [Template Management](https://docs.iotconnect.io/iotconnect/user-manuals/devices/template-management/), please see the [IoTConnect Documentation](https://iotconnect.io) website.)

## 6. IoTConnect Device Creation

* Create a new device in the IoTConnect portal. (Follow the [Create a New Device](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/create_new_device.md) guide for a detailed walkthrough.)
* Enter a value for the <var>Unique ID</var> and make note of it for later
* Enter a descriptive <var>Display Name</var>
* Select the template from the dropdown box hat was just imported (or provided)
* Generate a Base64 Key
   * **Option 1:**  Use a website such as [this one](https://generate.plus/en/base64) and leave the *Byte Length* at `16`
   * **Option 2:**  Run the following command in a shell (e.g. Git for Windows Bash or Cygwin):
     ```
      dd if=/dev/urandom bs=16 count=1 status=none | base64
     ```
* Copy the generated key (including any trailing "=") and paste in both <var>Primary Key</var> and <var>Secondary Key</var> fields
* Save this key as it will be used to setup the the device later on this guide

> **Note:**  
> It is not possible to reveal the key once added to the IoTConnect dashboard so be sure to save it.
 
* Click **Save**

## 7. Import the Project

Open e2 Studio
<details><summary>Click <b>File</b> then <b>Import...</b></summary>
<img style="width:75%; height:auto" src="./assets/quickstart/Import_project.png"/>
</details>

<details><summary>Select the <b>C/C++ Executable</b> option</summary>
<img style="width:75%; height:auto" src="./assets/quickstart/c_cpp_project_import.png"/>
</details>

<details><summary>Click <b>Browse</b>, select the binary downloaded in Step 3, then click <b>Next</b></summary>
<img style="width:75%; height:auto" src="./assets/quickstart/browse_and_next.png"/>
</details>

<details><summary>Click <b>Finish</b></summary>
<img style="width:75%; height:auto" src="./assets/quickstart/finish_import.png"/>
</details>

<details><summary>Click <b>Close</b></summary>
<img style="width:75%; height:auto" src="./assets/quickstart/close_import.png"/>
</details>

## 8. Setup the CK-RX65N board

Esnure all cables (USB, Network) are removed from from the board.

<details><summary>Change Jumper to <b>DEBUG</b></summary>
<img style="width:45%; height:auto" src="./assets/quickstart/move_debug_jumper.jpg"/>
</details>

<details><summary>Connect the network and USB cables to the board</summary>
<img style="width:45%; height:auto" src="./assets/ck-rx65n/IMG_20230303_093310710-crop.jpg"/>
</details>

<details><summary>Verify the power LED (white hyphen between the "CK" and "RX65N") is illuminated</summary>
<img style="width:45%; height:auto" src="./assets/ck-rx65n/IMG_20230316_120246661-crop-power.jpg"/>
</details>

## 9. Setup the Serial Terminal
Open the serial terminal application of choice, and configure as follows:
* Select the appropriate COM port
* 115200 baud rate
* 8-bit data
* No parity

## 10. Setup Debugging and Flash the Board

<details><summary>Right click on the project and select <b>Debug As -> Debug Configurations...</b></summary>
<img style="width:75%; height:auto" src="./assets/quickstart/Debug_as.png"/>
</details>

<details><summary>Double click on <b>Renesas GDB Hardware Debugging</b></summary>
  A new debug setup instance will apear directly beneath
</details>

<details><summary>Select the <b>Debugger</b> tab and verify settings as follows:</summary>
<img style="width:75%; height:auto" src="./assets/quickstart/debug_setup1.png"/>
</details>  
 
 * <var>Debug hardware</var> is set to `E2 Lite (RX)`<br>
 * <var>Target Device</var> is set to `R5F565NE`

<details><summary>Just below, click the <b>Connection Settings</b> tab and ensure:</summary>
<img style="width:75%; height:auto" src="./assets/quickstart/debug_setup2.png"/>
</details>  

* <var>Connection Type</var> is set to `Fine`
* Click <b>Apply</b> then <b>Debug</b> to begin flashing the board.

<details><summary>Verify the download begins in the console</summary>
<img style="width:75%; height:auto" src="./assets/quickstart/flashing.png"/>
</details>

<details><summary>Switch to the debug perspective when prompted.</summary>
<img style="width:75%; height:auto" src="./assets/quickstart/perspective_switch.png"/>
</details>

The build contains <b>two</b> breakpoints that will be encountered after a short time.
<details><summary>Press the <b>Resume</b> button when the console indicates a breakpoint has been reached</summary>
<img style="width:75%; height:auto" src="./assets/quickstart/resume_button.png"/>
</details>

> **Note:**  
> It may take a few minutes to move through the breakpoints depending on the speed of the PC.

Switch over to the serial terminal application and monitor the output.  

After a mintue or two, verify the following prompt is presented before moving on:<br>
`Type the CPID:`

<details><summary>The board is now programmed. You can now disconnect the USB cables, change jumper to <b>RUN</b>, and reconnect the USB cables</summary>
<img style="width:45%; height:auto" src="./assets/quickstart/move_debug_jumper.jpg"/>
</details>

## 11. Configure IoTConnect Information

<details><summary>Acquire CPID and ENV parameters from the IoTConnect Key Vault</summary>
<img style="width:75%; height:auto" src="./assets/quickstart/cpid_and_env.png"/>
</details>

* Enter the following into the Serial Terminal as prompted:  
  * <var>CPID</var> - The Company ID aquired from the Key Vault  
  * <var>ENV</var> - The Environment aquired from the Key Vault  
  * <var>DUID</var> - This is the <var>Unique ID</var> previously entered during device created in Step 6  
  * <var>SYMMETRIC_KEY</var> - This is the key that was previously generated during device created in Step 6  

<details><summary>Verify that the board connects:</summary>
<img style="width:75%; height:auto" src="./assets/quickstart/cli_example.png"/>
</details>

## 12. Visualize the Data

The telemetry can be visualized by using the Dynamic Dashboard feature of IoTConnect.  A sample dashboard has been created to display some telemtery from the board and is avail for download [here](templates/dashboard/renesas_CK-RX65N_dashboard_export.json).  
Once downloaded, select "Create Dashboard" from the top of the IoTConnect portal and then choose the "Import Dashboard" option and select the *Template Name* and *Device Name* used previously in this guide.

## Tips / Troubleshooting

<details><summary>Change perspectives in e<sup>2</sup> Studio</summary>
To return to C/C++ development view, select "Window", then "Perspective", then
"Open perspective", then "C/C++ project".

To return to debugging/running, select the "Window", then "Perspective", then
"Open perspective", then "Debug".
</details>
<details><summary>Print this Document</summary>
To print this document with all details expanded, right-click on this document and 
select "Inspect" or "Inspect Element".  This will open the browser's developer tools. 
Go to the Console tab and paste the following code:

  ```
    document.querySelectorAll('details').forEach(el => el.open = true);
  ```
Press Enter. This will expand all images on this page. After that, use the 
browser's print functionality to print the page.
</details>
