# Workshop: Bring AI to life with Arduino UNO Q on /IOTCONNECT

## 1. Introduction
This workshop guide provides step-by-step instructions to set up the Arduino Uno Q hardware and integrate it with /IOTCONNECT,
Avnet's robust IoT platform, to run an Arduino App Lab demo for AI Object Detection. With some simple changes, a variety of other App Lab Demo can be used as well.

## 2. Requirements
This guide has been written and tested to work on a Windows 10/11 PC to reach the widest audience.
* Arduino Uno Q hardware [Buy Now](https://www.newark.com/arduino/abx00162/uno-q-sbc-2gb-arm-cortex-a53-m33f/dp/59AM1209)
* Arduino App Lab Software [Download](https://www.arduino.cc/en/software/#app-lab-section)
* USB-C cable for to connection to PC
* 2.4GHz WiFi network credentials 

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

> [!WARNING]
> Using CTRL+v to paste does not work in the App Lab Terminal. Use **RIGHT-CLICK** to paste.

```bash
sudo mkdir -p /opt/demo && sudo chown $USER /opt/demo && \
git clone https://github.com/avnet-iotconnect/iotc-arduino-uno-q-workshop.git /home/arduino/iotc-arduino-uno-q-workshop && \
chmod +x /home/arduino/iotc-arduino-uno-q-workshop/scripts/*.sh
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
6. In the resulting **Device Certificate** field, select `Use my certificate`. Continue to the next step to get the certificate...
7. Return to the **Terminal Window** an xxecute the automated device credential generation script with this command:
```
/home/arduino/iotc-arduino-uno-q-workshop/scripts/credentials.sh
```
8. When prompted, press ENTER to have the script print out the generated device certificate.
9. Highlight the certificate text (including BEGIN and END lines) and **Copy (using CTRL+C)**
10. Return to the /IOTCONNECT page and paste the text into the **Certificate Text** box
11. Click the **Save and View** button to go to the page for your new device.
12. Now viewing the device page, click on the black/white/green "paper-and-cog" icon in the top-right of the device page (just above "Connection Info") to download your device's configuration file.
13. Open the configuration file in a text editor and copy its entirety to your clipboard.
14. Return to the terminal in the App Lab and **Paste (using RIGHT-CLICK, because CTRL+V does not work in the App Lab Terminal)** the contents (of the configuration file from your clipboard as instructed by the next step of the script, and then press ENTER.

The onboarding process is now complete. 

## 8. Set Up /IOTCONNECT SDK and Relay Service
Run the following commands to install the /IOTCONNECT Python Lite SDK and then download and configure the /IOTCONNECT Relay Service. 
```bash
sudo /home/arduino/iotc-arduino-uno-q-workshop/scripts/unoq_setup.sh
```

>[!NOTE]
> If during the setup script a pop-up appears asking if you would like to restart select device services, simply press 
> ENTER.

## 9. Clone and Copy the Example App and /IOTCONNECT Files
In Arduino App Lab:
1. Browse the example applications after clicking **Examples** in the vertical toolbar on the left.
2. Click on the **Detect objects on images** example application
3. Click on "Copy and edit app" in the top-right corner
4. Remove the `Copy of ` from the name and click **Create new**
5. Copy the /IOTCONNECT-enabled python files and relay client from the workshop repo into the app.  
```bash
cp /home/arduino/iotc-arduino-uno-q-workshop/app-configs/object-detection/python/* /home/arduino/ArduinoApps/detect-objects-on-images/python/ && \
cp /opt/demo/iotc_relay_client.py /home/arduino/ArduinoApps/detect-objects-on-images/python/
```

## 10. Run the App and Confirm Telemetry
1) Return to the Arduino App Lab  and Click **Run** in the top-right
2) Confirm the App starts sucessfully in the Arduino App Lab output window:
```bash
Starting app "Detect objects on images"
python provisioning
python downloading
Network detect-objects-on-images_default  Creating
Network detect-objects-on-images_default  Created
Container detect-objects-on-images-ei-obj-detection-runner-1  Creating
Container detect-objects-on-images-ei-obj-detection-runner-1  Created
Container detect-objects-on-images-main-1  Creating
Container detect-objects-on-images-main-1  Created
Container detect-objects-on-images-ei-obj-detection-runner-1  Starting
Container detect-objects-on-images-ei-obj-detection-runner-1  Started
Container detect-objects-on-images-ei-obj-detection-runner-1  Waiting
Container detect-objects-on-images-ei-obj-detection-runner-1  Healthy
Container detect-objects-on-images-main-1  Starting
Container detect-objects-on-images-main-1  Started
```
3) After a few seconds you should also see a new browser windows/tab appear. This can be closed as we will use the /IOTCONNECT interface.

## 11. Import a Dynamic Dashboard
1. Download the Dashboard Template: [obj-det-dashboard-template.json](https://github.com/avnet-iotconnect/iotc-arduino-uno-q-app-lab/blob/main/app-configs/object-detection/obj-det-dashboard-template.json)
2. Open /IOTCONNECT and click **Create Dashboard** at the top of the page
3. Click **Import Dashboard** and upload the JSON file linked above.
4. Select the `ardunio` template and your specific device name
5. Provide dashboard description such as `Object Detection` and click **Save**
6. You are now in the Dashboard Edit View.  Click **Save** once again at the top-right to view the live telemetry:
<br><img src="https://github.com/avnet-iotconnect/iotc-arduino-uno-q-app-lab/raw/main/app-configs/object-detection/unoQ-objdetimg-dashboard.jpg"/><br>

## 12. Using the Dashboard
* In the **Device Command** widget, select `detect-objects` from the drop-down
* Paste in a URL to an image with a variety of objects and click **Execute**

The application will report out objects with a confidence value over 50% (0.5). This threshold can be changed by using the `set-confidence` command and specifying a value between 0 and 1.

Example images and URLs:
<br><img width="200" src="https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/breakfast.png" />
```
https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/breakfast.png
```
<br><img width="200" src="https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/classroom.png" />
```
https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/classroom.png
```
<br><img width="200" src="https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/desk.png" />
```
https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/desk.png
```
<br><img width="200" src="https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/dog.png" />
```
https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/dog.png
```
<img width="200" src="https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/intersection_scaled.png" />
```
https://avnetpublicaccess.s3.us-east-1.amazonaws.com/object-detection-images/intersection.png
```

## 13. Summary of Attributes and Commands
### Telemetry Fields
| Field | Type |
| --- | --- |
| `UnoQdemo` | `STRING` |
| `detection_count` | `INTEGER` |
| `processing_time_ms` | `INTEGER` |
| `has_objects` | `STRING` |
| `confidence` | `DECIMAL` |
| `max_confidence` | `DECIMAL` |
| `avg_confidence` | `DECIMAL` |
| `detections_json` | `STRING` |
| `input_type` | `STRING` |
| `status` | `STRING` |
| `class_name_1` | `STRING` |
| `confidence_1` | `DECIMAL` |
| `class_name_2` | `STRING` |
| `confidence_2` | `DECIMAL` |
| `class_name_3` | `STRING` |
| `confidence_3` | `DECIMAL` |
| `class_name_4` | `STRING` |
| `confidence_4` | `DECIMAL` |

### Commands
| Command | Parameters | Description|
| --- | --- | --- |
| `set-confidence` | `confidence` | Set the default confidence (default: 0.5, Range 0-1) |
| `detect-objects` | `image_url` | URL to image for analysis |

## 14. Resources
* Purchase an Arduino Uno Q [Buy Now](https://www.newark.com/arduino/abx00162/uno-q-sbc-2gb-arm-cortex-a53-m33f/dp/59AM1209)
* Explore many more supported apps in the [iotc-arduino-uno-q-app-lab](https://github.com/avnet-iotconnect/iotc-arduino-uno-q-app-lab) repository.
