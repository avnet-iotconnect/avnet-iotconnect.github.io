# Workshop: Bring AI to life with Arduino UNO Q on /IOTCONNECT

## 1. Introduction
This workshop guide provides step-by-step instructions to set up the Arduino Uno Q hardware and integrate it with /IOTCONNECT,
Avnet's robust IoT platform to run IoT-connected Arduino App Lab demos.

## 2. Requirements
This guide has been written and tested to work on a Windows 10/11 PC to reach the widest audience.
* Arduino Uno Q hardware [Buy Now]()
* Arduino App Lab Software [Download](https://www.arduino.cc/en/software/#app-lab-section)
* USB-C cable for to connection to PC
* 2.4GHz Wifi network credentials 

## 3. Environment Setup

1. Install Arduino App Lab
2. Connect the Arduino UNO Q to your PC with a USB cable when prompted:
<br><img src="images/app-lab-connect.png" alt="Connect to board" width="300"><br>
3. Enter your Wi-Fi credentials
<br><img src="images/app-lab-2-network.png" alt="Enter network credentials" width="300"><br>
4. If prompted, update the board
<br><img src="images/app-lab-4-install-updates.png" alt="Install updates" width="300"><br>
5. Restart the board.
6. After restarting, in the **App Lab**, open **Examples** to view all available apps.
7. Open the **App Lab terminal** (used to access the Uno Q terminal).
<br><img src="images/app-lab-8-openterminal.png" alt="Open terminal" width="400"><br>


## 4. Clone the Arduino UNO Q /IOTCONNECT repository to your device

Cloning the repository to your Arduino will provide access to the automation scripts and App Lab code used in this workshop. 

> [!TIP]
> Users can paste into the Arduino App Lab terminal using **RIGHT-CLICK**. Using CTRL+V is not supported in the App Lab Terminal.

```bash
cd /home/arduino

git clone https://github.com/avnet-iotconnect/iotc-arduino-uno-q-workshop.git
cd iotc-arduino-uno-q-workshop

chmod +x scripts/*.sh
```

## 5. /IOTCONNECT: Cloud Account Setup
An /IOTCONNECT account with an AWS backend is required.  If you need to create an account, a free trial subscription is available.
The free subscription may be obtained directly from [iotconnect.io](https://iotconnect.io) or through the AWS Marketplace.

* Option #1 (Recommended) /IOTCONNECT via [AWS Marketplace](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/subscription/iotconnect_aws_marketplace.md) - 60 day trial; AWS account creation required
* Option #2 /IOTCONNECT via [iotconnect.io](https://subscription.iotconnect.io/subscribe?cloud=aws) - 30 day trial; no credit card required

> [!NOTE]
> Be sure to check any SPAM folder for the temporary password after registering.

## 6. /IOTCONNECT: Import the Device Template
1. Download the pre-made Device Template: [arduino-app-lab-template.json](https://raw.githubusercontent.com/avnet-iotconnect/iotc-arduino-uno-q-workshop/refs/heads/main/app-configs/arduino-app-lab-template.json) 
> [!IMPORTANT]
> Ensure that the template file saves as a `.json` file-type. Some browsers will default to a `.txt` file-type
> which is not supported by the /IOTCONNECT template import feature.
2. Log into your /IOTCONNECT account at [console.iotconnect.io](https://console.iotconnect.io/login)
3. Using the Sidebar menu in /IOTCONNECT, navigate to *Device -> Greengrass Device -> Template (bottom menu)*
<br><img width="1017" alt="click_templates" src="https://github.com/user-attachments/assets/e20ee569-38a1-4da6-bce1-08c66169774a" /><br>
4. Click on the **Create Template** button and then the **Import** button and browse to select the device template `arduino-app-lab-template.json` file.
<br><img width="326" height="227" alt="click_create_template" src="https://github.com/user-attachments/assets/6c6c3e4d-49fb-4cef-83ef-4a9a46f7adeb" /><br>

## 7. /IOTCONNECT: Create the Device

1. Click on the **Devices** tab of the blue toolbar at the bottom of the screen.
2. In the resulting page, click on the **Create Device** button in the top-right of the screen.
3. Enter `ArduinoUnoQ` in both the **Unique ID** and **Device Name** fields.
4. Select an available **Entity** from the dropdown (only for organization, does not affect connectivity).
5. Select `arduino` from the **Template** dropdown.
6. In the resulting **Device Certificate** field, select `Use my certificate`. (This will be populated later.)
7. Return to the terminal of your Arduino in the App Lab and navigate to the `scripts` directory by using this command: 
```
cd /home/arduino/iotc-arduino-uno-q-workshop/scripts
```
8. Execute the automated device credential generation script with this command:  
```
bash ./credentials.sh
```
8. When prompted, press ENTER to have the script print out the generated device certificate.
9. Copy **(using CTRL+C)** the device certificate text (including BEGIN and END lines) and paste the text into the 
certificate box in the /IOTCONNECT device creation page.
10. Click the **Save and View** button to go to the page for your new device.
11. Now viewing the device page, click on the black/white/green "paper-and-cog" icon in the top-right of the device page (just above "Connection Info") to download your device's configuration file.
12. Open the configuration file in a text editor and copy its entirety to your clipboard.
13. Return to the terminal in the App Lab and **Paste (using RIGHT-CLICK, because CTRL+V does not work in the App Lab Terminal)** the contents (of the configuration file from your clipboard as instructed by the next step of the script, and then press ENTER.

The onboarding process is now complete. 

## 8. Set Up /IOTCONNECT SDK and Relay Service

Return to the terminal windows and run the following commands to install the /IOTCONNECT Python Lite SDK and then download and configure the /IOTCONNECT Relay Service. 
```bash
cd /home/arduino/iotc-arduino-uno-q-workshop
sudo ./scripts/unoq_setup.sh --demo-dir /opt/demo
```

>[!NOTE]
> If during the setup script a pop-up appears asking if you would like to restart select device services, simply press 
> ENTER.

## 9. Choose a Lab Example, Clone It, and Copy the corresponding /IOTCONNECT Files

In Arduino App Lab:
1. Browse the example applications after clicking **Examples** in the vertical toolbar on the left.
2. Click on the `System Resources Logger` example application
3. Click on "Copy and edit app" in the top-right corner
4. Remove the `Copy of ` from the name
5. Copy the /IOTCONNECT-enabled python files and relay client from the workshop repo into the app.  

Let's start with an example that requires no additional hardware, **system-resources-logger**.
```bash
cp /home/arduino/iotc-arduino-uno-q-workshop/app-configs/system-resources-logger/python/* /home/arduino/ArduinoApps/system-resources-logger/python/
cp /opt/demo/iotc_relay_client.py /home/arduino/ArduinoApps/system-resources-logger/python/
```

### Examples Index

Use these /IOTCONNECT-specific guides:

- [air-quality-monitoring](app-configs/air-quality-monitoring/README.md)
- [anomaly-detection](app-configs/anomaly-detection/README.md)
- [audio-classification](app-configs/audio-classification/README.md)
- [bedtime-story-teller](app-configs/bedtime-story-teller/README.md)
- [blink](app-configs/blink/README.md)
- [blink-with-ui](app-configs/blink-with-ui/README.md)
- [cloud-blink](app-configs/cloud-blink/README.md)
- [code-detector](app-configs/code-detector/README.md)
- [home-climate-monitoring-and-storage](app-configs/home-climate-monitoring-and-storage/README.md)
- [image-classification](app-configs/image-classification/README.md)
- [keyword-spotting](app-configs/keyword-spotting/README.md)
- [led-matrix-painter](app-configs/led-matrix-painter/README.md)
- [mascot-jump-game](app-configs/mascot-jump-game/README.md)
- [object-detection](app-configs/object-detection/README.md)
- [object-hunting](app-configs/object-hunting/README.md)
- [real-time-accelerometer](app-configs/real-time-accelerometer/README.md)
- [system-resources-logger](app-configs/system-resources-logger/README.md)
- [theremin](app-configs/theremin/README.md)
- [unoq-pin-toggle](app-configs/unoq-pin-toggle/README.md)
- [vibration-anomaly-detection](app-configs/vibration-anomaly-detection/README.md)
- [video-face-detection](app-configs/video-face-detection/README.md)
- [video-generic-object-detection](app-configs/video-generic-object-detection/README.md)
- [video-person-classification](app-configs/video-person-classification/README.md)
- [weather-forecast](app-configs/weather-forecast/README.md)

---

## 6. Run the App and Confirm Telemetry

1) Run the app in App Lab.
2) Confirm telemetry appears in /IOTCONNECT.
3) If you enabled commands, test a command from /IOTCONNECT and verify the app receives it.

Expected result: the selected App Lab example runs on the UNO Q and publishes telemetry to /IOTCONNECT.

> [!TIP]
> You can manually manage the /IOTCONNECT Relay Service on your device.
>
> To disconnect your device from /IOTCONNECT, stop the relay service:
> ```bash
> sudo systemctl stop iotc-relay
> ```
>
> To start it again:
> ```bash
> sudo systemctl start iotc-relay
> ```
>
> To restart:
> ```bash
> sudo systemctl restart iotc-relay
> ```
