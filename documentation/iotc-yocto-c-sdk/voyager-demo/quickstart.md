# **Maaxboard Demo**
The demo consists of a website scraper that will scrape [NASA Voyager data](https://voyager.jpl.nasa.gov/mission/status/) every 10s or so & a pre-compiled basic-sample that takes a path to a configuration json file as it’s only argument. Once running the demo will send data to your specified device on iotc-azure. e.g.

![](Aspose.Words.8f9adb12-92a3-45af-8249-a8f179cbeea7.001.png) 
# **Setting Up Your MaaXBoard**
1. Download the SD Card images from [here](https://files.witekio.com/fxi_interface/ha6e7059ed9b126c0453fd669663e780/list.php?dir=%2FMaaXBoard+Demo%2F)
1. If zstd isn't installed, install it.

sudo apt install zstd

1. Decompress the archive

zstd -d core-image-minimal-maaxboard.wic.zst

1. Insert the SD Card
1. Ensure it’s not mounted

lsblk /dev/mmcblk0

NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT

mmcblk0     179:0    0   3.7G  0 disk

├─mmcblk0p1 179:1    0  83.2M  0 part

└─mmcblk0p2 179:2    0 819.9M  0 part

1. Write the .wic file to the sd card using dd

sudo dd if=core-image-minimal-maaxboard.wic of=/dev/mmcblk0 bs=1M conv=fsync status=progress

[sudo] password for user: 

915+1 records in

915+1 records out

960334848 bytes (960 MB, 916 MiB) copied, 174.202 s, 5.5 MB/s

1. Extract the SD Card once finished, insert into MaaxBoard & power board on.
   *The board is up & running if LED0 is on constantly & LED1 is flashing. Should neither of these conditions are true try power-cycling the board.*
1. Find the IP of the MaaxBoard using nmap

nmap --open -p22 10.42.0.1/24

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

1. Sign in over SSH as the root user

ssh root@10.42.0.10

1. Start the basic-sample program with your preferred configuration

root@maaxboard:~# basic-sample /home/config-x509.json 
# **Changing what Device the Data gets sent to**
There are a couple of json config files included on in the /home/ directory to serve as examples. Users have the option to create their own config files or edit the ones already present on the board. Creating and editing files on the SD Card can be achieved by either “in-situ” editing over terminal (cp, mv & vi for editing) or removing the SD Card & editing its contents on a PC. E.g.

mmcblk0                 179:0    0   3.7G  0 disk  

├─mmcblk0p1             179:1    0  83.2M  0 part  /media/user/boot

└─mmcblk0p2             179:2    0 819.9M  0 part  /media/user/root

With the SD Card inserted & mounted config jsons & new certificates could be uploaded to /media/user/root/home
## **Config json contents**
Below is the contents of the example config-x509.json:

{

`  `"duid": "CSDKYoctoVladSelfSigned",

`  `"cpid": "avtds",

`  `"env": "avnetpoc",

`  `"auth\_type": "IOTC\_AT\_X509",

`  `"x509\_certs": {

`    `"client\_key": "/home/client1-key.pem",

`    `"client\_cert": "/home/client1.pem"

`  `},

`  `"sensor": {

`    `"name": "Voyager-Sensor",

`    `"path": "/tmp/voy2\_kms"

`  `}

}

“Duid”, “cpid”, “env “& “auth\_type” should all be familiar from use of the SDK.

“x509\_certs” contains the requisite paths to certificates stored on the SD Card. When it’s time for the user to utilise their own certificates, edit this path.

“sensor” contains the name of a sensor & the path to where it’s sensor data can be accessed. At the time of writing the path is the output of the website scraper which is in the format of a comma separated large number. basic-sample parses the number at the path it’s given & sends it as telemetry data E.g.

![](Aspose.Words.8f9adb12-92a3-45af-8249-a8f179cbeea7.002.png) 

The number sent from basic-sample, 12494925803 corresponds to the 12,494,952,933 mi Voyager 2 is from the Sun (the website updates much quicker than the scraper)
