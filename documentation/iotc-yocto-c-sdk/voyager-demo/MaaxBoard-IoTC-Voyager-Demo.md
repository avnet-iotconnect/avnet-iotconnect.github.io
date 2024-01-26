# Maaxboard Demo

This demo is an example implementation of the IoTConnect C SDK implemented on the Avnet MaaxBoard running Yocto Linux.  
The application will scrape [NASA Voyager data](https://voyager.jpl.nasa.gov/mission/status/) every few seconds send the data to a specific device on IoTConnect.  This is achieved using a pre-compiled binary ("basic-sample") and a user configurable JSON file.  
![](https://saleshosted.z13.web.core.windows.net/media/nxp/jpl/qs-img1.png) 
* Information from the following guides were used in creating this document and will provide helpful troubleshooting information
[Getting Started with MaaXBoard - Headless Setup](https://www.hackster.io/monica/getting-started-with-maaxboard-headless-setup-24102b)
[Getting Started with MaaXBoard](https://community.element14.com/products/devtools/single-board-computers/b/blog/posts/getting-started-with-maaxboard)

# Prerequisites

* Avnet MaaXBoard p/n: [AES-MC-SBC-IMX8M-G]([https://www.avnet.com/wps/portal/us/products/avnet-boards/avnet-board-families/maaxboard/maaxboard])
* microSD Card between 8 and 64GB
* Ethernet Cable with Internet Access
* (optional) USB to TTL Serial Converter Cable 5V

# IoTConnect Account Setup
This guide requires an IoTConnect account on Azure.

>**NOTE:**  
> If you have already created an IoTConnect account on Azure, or were provided an account as part of a training or workshop, skip this section.

If you need to create an account, a free 2-month subscription is available.
Please follow the 
[Creating a New IoTConnect Account](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/subscription/subscription.md)
guide and ensure to select the [Azure version](https://subscription.iotconnect.io/subscribe?cloud=azure) during registration:

![IoTConnect on Azure](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/subscription/media/iotc-azure.png)

# IoTConnect Device Template Setup

> **Note:**
> If you are following this guide as part of a training or workshop, a device template may have already been created and this section can be skipped. Check if a template called "Voyager Sensors" already exists in the template tab of the "Device" section.

A Device Template with need to be imported:
* Download the premade [Voyager Sensors](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotc-yocto-c-sdk/voyager-demo/templates/device/Voyager%20Sensors_template.JSON) Device Template.  
* Import the template into your IoTConnect instance. (A guide on [Importing a Device Template](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/import_device_template.md) is available or for more information on [Template Management](https://docs.iotconnect.io/iotconnect/user-manuals/devices/template-management/), please see the [IoTConnect Documentation](https://iotconnect.io) website.)

# Create Device in IoTConnect

* From the navigation panel on the left, select the Device icon and the "Device" sub-menu.  
![image](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/assets/40640041/fc84a59a-1317-4f25-bebf-1d07d1e535bf)

* At the top-right, click on the "Create Device" button.  
![image](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/assets/40640041/1882296f-a3dc-44d0-936c-79ed15a874e2)

* Enter a *Unique ID* and descriptive *Display Name* of your choice.
	* This Unique ID is your "DUID".  Please make note of it.
* Select the device template identified or created earlier in this guide. 
* Select the appropriate Entity for this device to reside.
* Use the following for the Primary Thumbprint field:
  ```
  37c8c74eca7f885ec5286e30c650ae1c7c6a69f8
  ```
* Click **Save**

# Setting Up the MaaXBoard

1. Download and extract the SD Card image: [core-image-minimal-maaxboard-20231020233139.rootfs.wic.gz](https://saleshosted.z13.web.core.windows.net/sdk/nxp/voyager/core-image-minimal-maaxboard-20231020233139.rootfs.wic.gz)
2. Insert the SD Card into your PC and write it to the SD card using one of the following options:
<details><summary><b>Option 1: Linux Command Line</b></summary>
  
* Ensure the sd card is not mounted

  ```ruby
  lsblk /dev/mmcblk0
  ```

  ```ruby
  NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
  mmcblk0     179:0    0   3.7G  0 disk
  ├─mmcblk0p1 179:1    0  83.2M  0 part
  └─mmcblk0p2 179:2    0 819.9M  0 part
  ```

* Write the .wic file to the sd card using dd
  ```ruby
  sudo dd if=core-image-minimal-maaxboard.wic of=/dev/mmcblk0 bs=1M conv=fsync status=progress
  ```
  ```ruby
  [sudo] password for user:
  915+1 records in
  915+1 records out
  960334848 bytes (960 MB, 916 MiB) copied, 174.202 s, 5.5 MB/s
  ```
  
</details>
<details><summary><b>Option 2: Image File Utility (PC/MAC)</b></summary>
  
  * Download and install [Balena Etcher](https://etcher.balena.io/)
  * Open Balena Etcher (may required elevated privileges based on your computer user account)
  * Select your image and flash it to an SD card
    
  ![](https://saleshosted.z13.web.core.windows.net/media/nxp/jpl/balenaetcher.JPG) 
  </details>

3. Remove the SD Card once finished, insert into MaaXBoard, power board on and connect the Ethernet port to the Internet.

> **Note:**
> The board is up & running if LED0 is on constantly & LED1 is flashing. If neither of these conditions are true, try power-cycling the board.

# Connecting to the MaaXBoard

<details><summary><b>Option 1: SSH to the MaaXBoard</b></summary>

1. Determine your host machine's IP address and subnet.
	* On Linux or macOS, Type "ifconfig"
		  * Look for entries like eth0 (wired connection) or wlan0 (wireless connection). Your IP address will be listed as inet (IPv4).
	* On Windows, Type "ipconfig"
		  * Look for the section Ethernet adapter (for wired connections) or Wireless LAN adapter (for wireless connections). Your IP address will be listed as IPv4 Address.
2. Determine your scan range
	* Based on your subnet mask, you can determine the range. For instance, if your IP is `10.42.0.100` and the subnet mask is `255.255.255.0` (or `/24` in CIDR notation), you can scan the range `10.42.0.1/24` to cover all devices in your local network.

3. Find the IP of the MaaXBoard using nmap

  ```ruby
  nmap --open -p22 10.42.0.1/24
  ```
  ```ruby  
  Starting Nmap 7.80 ( https://nmap.org  ) at 2023-09-13 17:31 BST
  Nmap scan report for pyNixTop (10.42.0.1)
  Host is up (0.000092s latency).
  PORT   STATE SERVICE
  22/tcp open  ssh
  Nmap scan report for 10.42.0.180
  Host is up (0.00094s latency).
  PORT   STATE SERVICE
  22/tcp open  ssh
  Nmap done: 256 IP addresses (2 hosts up) scanned in 3.19 seconds
  ```
  *  Sign in over SSH
  ```ruby
	  ssh root@10.42.0.10
  ```
</details>
  
<details><summary><b>Option 2: UART/Serial (requires USB to TTL Serial Cable)</b></summary>

1. Install [CoolTerm](https://freeware.the-meiers.org/) (or another SSH client, like [Tera Term](https://ttssh2.osdn.jp/index.html.en), [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/) or [Cyberduck](https://www.ssh.com/ssh/cyberduck))
2. Connect the board to your USB-to-TTL cable. Connect pin 6 (the 3rd from the edge) to GND, pin 7 to RX (the white wire in this case) and pin 8 to TX (the green wire in this case).

![](https://hackster.imgix.net/uploads/attachments/1097620/ttl_HLcYgi3dxk.png?auto=compress%2Cformat&w=740&h=555&fit=max)

3. Connect to your MaaXBoard via serial using your SSH client. Baudrate should be 115200, data bits are 8, and stop bits are 1.

4. Connect the USB-C to power

> **NOTE:** If you use a USB-C cable to power your board, don't plug it into your computer's USB ports, since it may draw more power than your USB ports can supply. You can also purchase the recommended 5V 3A power supply for the board [here](https://www.avnet.com/shop/us/products/avnet-engineering-services/aes-acc-maax-pwrul-3074457345642357173/).

Connect via CoolTerm

Open CoolTerm and configure your settings. Baud rate should be 115200, data bits 8, and stop bits 1. I like to set the terminal mode to "line mode" and "filter ASCII Escape sequences" to reduce the gibberish.

![Baud rate should be 115200](https://hackster.imgix.net/uploads/attachments/1096739/screen_shot_2020-04-04_at_2_26_46_pm_PIzvz5OmWr.png?auto=compress%2Cformat&w=740&h=555&fit=max)

Baud rate should be 115200

Click "Connect" in CoolTerm.

You should see all the log messages while booting like in the picture below with the AVNET logo and the login prompt:

![](https://hackster.imgix.net/uploads/attachments/1096736/screen_shot_2020-04-05_at_10_25_31_am_lzhd2noxV8.png?auto=compress%2Cformat&w=740&h=555&fit=max)

At this point you can log into the board with the default credentials:
User: **root**
Pass: <none>

</details>		

# Update Configuration

* Open the `config.json` file for editing:
	 ```ruby
	vi /usr/local/iotc/config.json
	```
* Press `i` and use the arrow keys to navigate to line 3
* Enter the **Device ID** created earlier as the value for DUID
* Press `ESC` then `:wq` to write and quit

# Start the Demo Application

Type the following command to restart the service with the new Device ID
```ruby
systemctl start iotc-c-telemetry-demo
```
Check to ensure the service started properly:
```ruby
systemctl status iotc-c-telemetry-demo
```

# Verification

At this point the board will be sending telemetry to the IoTConnect portal. This can be verified by checking the "Live Data" feed.
* Return to the *Devices* page and click on the newly created Device ID.
* On the left sub-menu, click *Live Data* and after a few seconds, data will be displayed.  
![](https://github.com/avnet-iotconnect/iotc-azurertos-sdk/assets/40640041/21d25bbb-71d0-4a9d-9e74-e2acf0983183)

# Visualization

The data can be visualized by using the Dynamic Dashboard feature of IoTConnect.  A sample dashboard that is preconfigured to display the Voyager Mission's telemetry is available for download [here](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotc-yocto-c-sdk/voyager-demo/templates/dashboard/MaaXBoard%20Voyager%20Demo_dashboard_export.json).  

Once downloaded, select "Create Dashboard" from the top of the IoTConnect portal and then choose the "Import Dashboard" option and select the template and device name used previously in this guide.

Congratulations, your sample dashboard should look similar to the one below.


<img src="https://saleshosted.z13.web.core.windows.net/media/nxp/jpl/voydash.png" width="300">


# Other Information

<details><summary>Generating the certificate fingerprint</summary>
This demo uses an X.509 certificate to authenticate itself to IoTConnect.  
For the purpose of this demo, this certificates have been pre-generated and provided with the demo package.  
To walkthough how the fingerprint is generated, follow the steps below.  
This same process can be used to use your own certificate.  

1. Download the package: <a href="https://saleshosted.z13.web.core.windows.net/sdk/nxp/voyager/my-iotc-devices.tgz">my-iot-devices.tgz</a>
2. Extract the TGZ, then the TAR, and finally the ZIP.
3. Open the DeviceCertificate.pem in a text editor and copy the Device Certificate including the BEGIN and END lines.
4. Generate the device fingerprint from the certificate.
	* Paste the certficate information into the "X.509 cert" field on <a href="https://www.samltool.com/fingerprint.php"> this site</a>  
	* Leave the "Algorithm" selection at the default SHA1, press "Calculate Fingerprint" and copy/save the Fingerprint field for later use.
</details>
