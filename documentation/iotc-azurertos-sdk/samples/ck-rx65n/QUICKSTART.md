# Renesas CK-RX65N (blue PCB) Quick Start Guide

***NOTE:*** this guide assumes you have E2 Studio installed. If you didn't - please follow instructions to install if from [here](DEVELOPER_GUIDE.md)

## Download binaries

Download the QuickStart ELF (Executable and Linking Format) file which contains the pre-built binary:  
[ck-rx65n-qs/ck-rx65n-basic-sample-cli.elf](https://saleshosted.z13.web.core.windows.net/sdk/renesas/ck-rx65n-qs/ck-rx65n-basic-sample-cli.elf)

## Open E2 Studio

## Importing binaries

### Close Welcome view

<img style="width:75%; height:auto" src="./assets/quickstart/close_welcome.png"/> 

### Import C/C++ project

<img style="width:75%; height:auto" src="./assets/quickstart/Import_project.png"/>
<img style="width:75%; height:auto" src="./assets/quickstart/c_cpp_project_import.png"/>


### Click "Browse" button and provide path to downloaded binaries and proceed.

<img style="width:75%; height:auto" src="./assets/quickstart/browse_and_next.png"/>

### Click "Finish"

<img style="width:75%; height:auto" src="./assets/quickstart/finish_import.png"/>

### Close opened window

<img style="width:75%; height:auto" src="./assets/quickstart/close_import.png"/>

## Setup the CK-RX65N board

[Setup the CK-RX65N](https://www.renesas.com/us/en/products/microcontrollers-microprocessors/rx-32-bit-performance-efficiency-mcus/ck-rx65n-cloud-kit-based-rx65n-mcu-group).

Connect the two USB-micro leads and the ethernet cable:
***Note:*** both USB-to-USB_micro must be data transfer cables.

<img style="width:45%; height:auto" src="./assets/ck-rx65n/IMG_20230303_093310710-crop.jpg"/>

The power LED should be lit. The power LED forms the "-" in the CK-RX65N on the silk-screen on the board, above the fingerprint reader.

<img style="width:45%; height:auto" src="./assets/ck-rx65n/IMG_20230316_120246661-crop-power.jpg"/>

### Setup a terminal connection

Install
[termite](https://www.virtual-serial-port.org/articles/alternative-to-termite-terminal/), or
[Tera Term](https://ttssh2.osdn.jp/index.html.en), or
[picocom](https://linux.die.net/man/8/picocom), 
or a similar terminal application.

The terminal settings to connect are:

- Chose appropriate COM port. Note: In Linux the terminal may enumerate as
  `/dev/ttyACM0`.
- 115200 baud rate
- 8-bit data
- No parity

## Creating Debugging Setup and Flashing the board

Right click on your project in Project Explorer Tab (typically on your left side)-> Debug As -> Debug Configurations... 

<img style="width:75%; height:auto" src="./assets/quickstart/Debug_as.png"/>

Double click Renesas GDB Hardware Debugging -> it should create new debug setup instance.

In newly created debug instance check that:

In "GDB settings" tab:
- "Debug Hardware" is set to "E2 Lite (RX)";
- "Target Device" is set to "R5F565NE" (for ck-rx65n (blueboard));

<details> <summary> Click to see screenshot of setup </summary>
<img style="width:75%; height:auto" src="./assets/quickstart/debug_setup1.png"/>
</details>

In "Connection Settings" tab:

"Connection type" is set to "Fine".

Apply -> Debug

<details> <summary> Click to see screenshot of setup </summary>
<img style="width:75%; height:auto" src="./assets/quickstart/debug_setup2.png"/>
</details>

It should start flashing the board.

**If it started successfuly you should be able to see this:**
<img style="width:75%; height:auto" src="./assets/quickstart/flashing.png"/>

Switch to the debug perspective when prompted.

<img style="width:75%; height:auto" src="./assets/quickstart/perspective_switch.png"/>

</details>

The build will have two default breakpoints already enabled, so presume the
Resume button (green "left-pointing triangle") in the middle of e<sup>2</sup>
studio twice to enable to code to execute past those two breakpoints.

<img style="width:75%; height:auto" src="./assets/quickstart/resume_button.png"/>

Output should be visible in any attached terminal now.

When finished press the Terminate button (red "square") next to the Resume
button.

To debug again, press the debug button.

To return to C/C++ development, select the "Window", then "Perspective", then
"Open perspective", then "C/C++ project".

To return to debugging/running, select the "Window", then "Perspective", then
"Open perspective", then "Debug".

## Using CLI

After successful boot and network configuration (automatic process) you will be prompted to enter IoTConnect connection details

<details><summary> Click here if you do not have a device on IoTConnect to enter details of </summary>

## Create a sequence of 16-64 random bytes that are Base64 encoded - for use as a Symmetric Key

To create a random symmetric "key" we will generate a random 32 byte sequence
and then Base64 encode it – so that the binary values can be shared easily.

Run this command in a shell, e.g. in Git for Windows Bash, Cygwin, etc.:

    dd if=/dev/urandom bs=16 count=1 status=none | base64

A symmetric key is used to both encode and decode - so the same key is used on
the IoT device and on the IoTConnect server.

<img style="width:28.63%; height:auto" src="./assets/quickstart/VirtualBox_WinDev2301Eval_21_02_2023_10_04_32.png"/>

Make a note of this output, as it will be used to setup the IoTConnect template
for the device on the IoTConnect dashboard – and in the application use. 
This is important as isn’t possible to recover key information once
added to the IoTConnect dashboard.

In this case the symmetric key is:

    YzlgdRbYcreYW1fhjwxO4b3X7hBlDY3OVuw6q9wDbAo=

## IoTConnect device

For further information, please consult the [Knowledge Base](https://help.iotconnect.io) which can be found
on the left side of the IoTConnect dashboard in the "Resources" section.

<img style="width:75%; height:auto" src="./assets/quickstart/VirtualBox_WinDev2301Eval_17_02_2023_13_41_11.png"/>

<details> <summary> Click to see template creation </summary>

### Create IoTConnect template

Log into your IoTConnect account and open the appropriate Device page which can
be found on the left side of the IoTConnect dashboard.

The template page can be selected by using the "Templates" tab at the bottom of
the page.

<img style="width:75%; height:auto" src="./assets/quickstart/VirtualBox_WinDev2301Eval_20_02_2023_14_15_26.png"/>

Press "Create Template" at the top right corner of the page to create a new
template.

When creating the template choose a unique name for the "Template Code" (which
is a maximum of 10 characters and must start with a letter) and a useful
description in the "Template Name".  Choose "Symmetric Key" for the
"Authentication Type" and choose "2.1" for the "Device Message Version".

<img style="width:75%; height:auto" src="./assets/quickstart/VirtualBox_WinDev2301Eval_20_02_2023_14_40_52.png"/>

When the template is saved, we can add attributes – "measurements" (and types)
– for values that will be sent by the ck-rx65n board.

<img style="width:75%; height:auto" src="./assets/quickstart/VirtualBox_WinDev2301Eval_20_02_2023_14_41_51.png"/>

Click "Attributes (0)" and add a "version" attribute with STRING type and "Save" it.

<img style="width:75%; height:auto" src="./assets/quickstart/VirtualBox_WinDev2301Eval_20_02_2023_14_49_29.png"/>

Add a second "button" attribute with BOOLEAN type, a third "temperature" attribute with
DECIMAL type, and a fourth "humidity" attribute with DECIMAL type.

<img style="width:75%; height:auto" src="./assets/ck-rx65n/VirtualBox_WinDev2301Eval_29_03_2023_13_53_25.png"/>

Note: in the ck-rx65n basic-sample the attribute values are sent using
`iotcl_telemetry_set_xxx()` style commands.

Make a note of the template name, as this will be used as the "Template" to
create the IoTConnect device in the next step – but it will be visible in the
drop-down list.

</details>

### Create IoTConnect device

Log into your IoTConnect account and open the appropriate Device page which can
be found on the left side of the IoTConnect dashboard.

The device page can be selected by using the "Devices" tab at the bottom of the
page.

<img style="width:75%; height:auto" src="./assets/quickstart/VirtualBox_WinDev2301Eval_21_02_2023_09_56_06.png"/>

- Chose a "Unique Id" for your device – this will be asked to be entered as `DUID`
  built/compiled in the device later.
- Chose a "Display Name" for your device.
- Select an appropriate "Entity" – this is a pre-populated menu item.
- Select the "Template" display name that was created in the previous step or was already defined –
  this will require filling in extra fields "Primary Key" and "Secondary Key".
- Use the symmetric key that was generated previously, including any trailing
  "=" signs, e.g. `YzlgdRbYcreYW1fhjwxO4b3X7hBlDY3OVuw6q9wDbAo=` as the value
  for the "Primary Key" and the "Secondary Key".

<img style="width:75%; height:auto" src="./assets/quickstart/VirtualBox_WinDev2301Eval_21_02_2023_09_57_43.png"/>

When I created the template I pasted the same value in both the
"Primary Key" and the "Secondary Key" and included the trailing "=" equals
sign.

</details>

<details> <summary> Acquire CPID and ENV parameters </summary>

`CPID` and `ENV`- can be aquired by going to IoTConnect Dashboard -> Settings -> Key Vault
You should be able to see `CPID` and `Environment` fields in the top part of the screen:
<img style="width:75%; height:auto" src="./assets/quickstart/cpid_and_env.png"/>

</details>

`SYMMETRIC_KEY` is the key you've saved when you were creating new device on IoTConnect dashboard. Should be entered fully (with trailing "=" signs)

`DUID` - Unique ID used in creation of device on IoTConnect dashboard

***Please note:*** current version (07/09/2023) does not allow erasing whatever was typed in, so be careful. If typo was made - you'll need to reboot the board and start anew.

Example expected behaviour:

<img style="width:75%; height:auto" src="./assets/quickstart/cli_example.png"/>
