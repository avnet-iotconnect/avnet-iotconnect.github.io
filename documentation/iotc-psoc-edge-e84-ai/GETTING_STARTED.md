# Getting Started: PSOC Edge E84 AI Kit with /IOTCONNECT 
![psoc-edge-e84-ai-kit.png](./media/psoc-edge-e84-ai-kit.png)

## 1. Introduction

This guide will walk through the steps of setting up the Infineon PSOC™ Edge E84 AI Kit 
for connecting to Avnet's /IOTCONNECT platform and demonstrating the "Hand Gesture" [DEEPCRAFT™ Ready Model](https://www.infineon.com/design-resources/embedded-software/deepcraft-edge-ai-solutions/deepcraft-ready-models).

## 2. Prerequisites
* **PSOC™ Edge E84 AI Kit** ([Buy Now](https://www.newark.com/infineon/kitpse84aitobo1/ai-eval-kit-32bit-arm-cortex-m55f/dp/49AM4459))
* PC with Windows 10/11
* USB-C data cable
* 2.4GHz WiFi Network
* A serial terminal application such as [Tera Term](https://ttssh2.osdn.jp/index.html.en) or a browser-based application like [Google Chrome Labs Serial Terminal](https://googlechromelabs.github.io/serial-terminal/)
* A registered [myInfineon Account](https://www.infineon.com/sec/login)

## 3. Create /IOTCONNECT Account
An /IOTCONNECT account with an AWS backend is required.  If you need to create an account, a free trial subscription is available.
The free subscription may be obtained directly from [iotconnect.io](https://iotconnect.io) or through the AWS Marketplace.

* Option #1 **(Recommended)**   
/IOTCONNECT via [AWS Marketplace](https://github.com/avnet-iotconnect/avnet-iotconnect.github.io/blob/main/documentation/iotconnect/subscription/iotconnect_aws_marketplace.md) - 60 day trial; AWS account creation required  


* Option #2  
/IOTCONNECT via [iotconnect.io](https://subscription.iotconnect.io/subscribe?cloud=aws) - 30 day trial; no credit card required

> [!NOTE]
> Be sure to check any SPAM folder for the temporary password after registering.

Login to the platform by navigating to [console.iotconnect.io](https://console.iotconnect.io)

## 4. Import Device Template

* Download the pre-made [Device Template](https://github.com/avnet-iotconnect/avnet-iotc-mtb-psoc-edge-rm/blob/main/files/device-template.json) for the Edge E84 AI Kit.

1. From the navigation panel on the left, select the **Devices** icon and the **Device** sub-menu.<br>![menu-devices-device.png](../iotconnect/media/menu-devices-device.png)  
2. At the bottom of the page, select the **Templates** icon from the toolbar.<br>![menu-templates.png](../iotconnect/media/menu-templates.png)  
3. At the top-right of the page, select the **Create Template** button.<br>![button-create-template.png](../iotconnect/media/button-create-template.png)  
4. At the top-right of the page, select the **Import" button**.<br>![button-import.png](../iotconnect/media/button-import.png)  
5. Click the **Browse** button, navigate to and select the downloaded template `device-template.json`
6. Click **Save**

## 5. Create a Device
In this step, we will create a **Device** associated with the previously imported **Device Template**

1. In the ribbon at the bottom of the screen, click the **Devices**
2. At the top-right, click **Create Device**  
![button-create-device.png](../iotconnect/media/button-create-device.png)
3. Enter a custom device **Unique ID** (also called a **DUID**) and **Device Name** such as `PSOCEdgeE84`
4. Select the **Entity** to associate the device (For new accounts, there is only one option)  
5. Select the previously imported template `pedgerm` 
6. Under **Device Certificate** select **Auto-generated**
7. Click **Save & View**
8. Download the **Device Configuration Information** by clicking the icon in the upper right of the device page  
![icon-device-configuration-information.png](../iotconnect/media/icon-device-configuration-information.png)
 
## 6. Obtain Certificates
In this step we will locate and download the **device certificates**.

1. Just below the Device Configuration Information icon, click the `Connection Info` link.<br>![connection-info.png](../iotconnect/media/connection-info.png)
2. Click on the **Certificates** icon in the top-right and save the file to your working directory.<br>![icon-certificates.png](../iotconnect/media/icon-certificates.png)
3. Extract the contents of the `*-certificates.zip` file for use in the next section. 
## 7. Setup Development Environment

1. Download and Install [Microsoft Visual Studio Code](https://code.visualstudio.com/Download) v1.105.0 or newer.
2. Launch VSCode and **Install** the following extensions:<br>![vscode-extensions.png](./media/vscode-extensions.png)
3. Download [ModusToolbox&trade; software](https://www.infineon.com/cms/en/design-support/tools/sdk/modustoolbox-software/). Install the ***ModusToolbox&trade; Setup*** software. The software may require you to log into your Infineon account. In ***ModusToolbox&trade; Setup*** software, download & install the items below:
   * ModusToolbox&trade; Tools Package 3.6.
   * ModusToolbox&trade; Edge Protect Security Suite 1.6.0.
   * ModusToolbox&trade; Programming Tools 1.6.0.
   * Arm GNU Toolchain (GCC) 14.2.1.
   * Microsoft Visual Studio Code (Should be checked by default)

4. Launch **ModusToolbox&trade; Dashboard** and select Target IDE `Microsoft Visual Studio Code` from the dropdown on top-right.<br>![mtb-ide-select.png](./media/mtb-ide-select.png)
5. Click **Launch Project Creator**.  
6. Select the `PSOC Edge E84 AI Kit` and click **Next**.
7. For the Application(s) Root Path, specify or browse to a directory where the application will be created.
8. Ensure that the **Target IDE** is `Microsoft Visual Studio Code`.
9. Type `avnet` in the **Template Applications** search box and add a checkmark next to `Avnet PSOC Edge DEEPCRAFT Ready Models`<br>![mtb-project-creator.png](./media/mtb-project-creator.png)
10. Click **Create**.
11. After the project is created successfully, close the Project Creator.

## 8. Configure and Build Software
Launch `Visual Studio Code`, and Select **File -> Open Workspace from File**, navigate to the location of the application that was just
created, select the workspace file, and click **Open**.
> [!IMPORTANT]
> Depending on your settings in VS Code, you may see a message about trusting the authors. If so, click **Yes, I trust the authors**.

### Configure Device
* In the project tree, expand `proj_cm33_ns` open `app_config.h` and update the following lines using the `iotcDeviceConfig.json` downloaded previously.
```
12 #define IOTCONNECT_CONNECTION_TYPE IOTC_CT_AWS
13 #define IOTCONNECT_CPID "<cpid>"
14 #define IOTCONNECT_ENV  "<env>"

17 #define IOTCONNECT_DUID "<uid>"
```
>[!CAUTION] 
> The cert and key must be properly formatted when being entered.

Use an LLM like ChatGPT to format the certificate and key by using the following prompt and then pasting in your certificate and key:
```
Format the following certificate and key for inclusion in a .h file as #define IOTCONNECT_DEVICE_CERT and #define IOTCONNECT_DEVICE_KEY
```

Use the resultant outputs to replace the following lines:

```
#define IOTCONNECT_DEVICE_CERT "<insert cert>"
#define IOTCONNECT_DEVICE_KEY "<insert key>"
```

<details><summary>Expand for an Example</summary>
<pre><code>
#define IOTCONNECT_DEVICE_CERT \
"-----BEGIN CERTIFICATE-----\n" \
"MIIDWTCCAkGgAwIBAgIUSbMqOMg8VRUTNUWXYE/LQEYus00wDQYJKoZIhvcNAQEL\n" \
"BQAwTTFLMEkGA1UECwxCQW1hem9uIFdlYiBTZXJ2aWNlcyBPPUFtYXpvbi5jb20g\n" \
"SW5jLiBMPVNlYXR0bGUgU1Q9V2FzaGluZ3RvbiBDPVVTMB4XDTI1MTAyNDE3MDMw\n" \
"MloXDTQ5MTIzMTIzNTk1OVowHjEcMBoGA1UEAwwTQVdTIElvVCBDZXJ0aWZpY2F0\n" \
"ZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOJ1gnw81gtXTDqcCFHN\n" \
"nH5GhUtemPisY8IOiAOQOvttAcesE5PBTcForGYRMPwBfXIYIQWq+sPsKOIiaxps\n" \
"XuwNfQhTjw2DlsR1fRVftcj1V70eI0qucZTPJ83en93mhXi0Aja3wkzhUKr/YjXg\n" \
"61cLDFUhwRwE7TyIg8stFS+SwEu4nAxnWZxjLII5DTjmFgpQwJPR74YXgasUqWDH\n" \
"C34fpufAHZZcYAKRylLVd5BJLrFSGkuZoBmwA2mRKoYz+DpkKhsIxdU/1EHqpBtf\n" \
"ZVVO4ETd1RGadZm6pezIhI33HF2zbn4QOkk88LIMLv8kP+FCu0JZUV50t2vO46/s\n" \
"sp0CAwEAAaNgMF4wHwYDVR0jBBgwFoAUgEZbxS9CKqZ4t3llAjuNjo7KXD8wHQYD\n" \
"VR0OBBYEFHjA9aP2CjvTGx+pdBLIlDmAaCAzMAwGA1UdEwEB/wQCMAAwDgYDVR0P\n" \
"AQH/BAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQBks7fvcImw15wnX15b8gw525vP\n" \
"6uhY9jd30h9urUH/4ErZjq9PBxKESCOsrQUyoz5rer6OWoGNqp4HQ6meE9+iZ5h+\n" \
"qVfiPe2j7QrHbWDMTMoqNtbaab1jmEpexoVv+TL/w3/kYjSgP0J0059P3dVTRl4F\n" \
"I5SNu0x+/7AHyzTZfG487IqADS9SyXDrQPB2GSSY0ozFU1Z1Q7nEA6a9t8VRln4Q\n" \
"OQJUuLHFm5jjRyIfMAHSjexF/Q58vrDUYfKYvGe1cGjXoFgvufFVx2DkARLqz4Ru\n" \
"VV6uYAMqvdkwFZC+Fp4MaVH3Pj7C7UOY1CpdEgiXwv9wMihIcoh6daWYFuR/\n" \
"-----END CERTIFICATE-----\n"

#define IOTCONNECT_DEVICE_KEY \
"-----BEGIN RSA PRIVATE KEY-----\n" \
"MIIEowIBAAKCAQEA4nWCfDzWC1dMOpwIUc2cfkaFS16Y+Kxjwg6IA5A6+20Bx6wT\n" \
"k8FNwWisZhEw/AF9chghBar6w+wo4iJrGmxe7A19CFOPDYOWxHV9FV+1yPVXvR4j\n" \
"Sq5xlM8nzd6f3eaFeLQCNrfCTOFQqv9iNeDrVwsMVSHBHATtPIiDyy0VL5LAS7ic\n" \
"DGdZnGMsgjkNOOYWClDAk9HvhheBqxSpYMcLfh+m58AdllxgApHKUtV3kEkusVIa\n" \
"S5mgGbADaZEqhjP4OmQqGwjF1T/UQeqkG19lVU7gRN3VEZp1mbql7MiEjfccXbNu\n" \
"fhA6STzwsgwu/yQ/4UK7QllRXnS3a87jr+yynQIDAQABAoIBAFq8gLrs2UqUAOwe\n" \
"5sp4GvMRqIjpb1t8H0B6+A6NdMSXCbaKgRGby17qZOFElB71LeFQP7L4rh9geYUa\n" \
"C1X8BBCK2wVCDbh5eChhduvgfIL3ot8Yu0VKHiJk2msHf4C2w9X4MkbgXA7X3K2X\n" \
"RC+YXlNzDs7xhmGGq9OsUzpOZwW3Azg+pSa2HDgUHz3+Bg0XoqxuEW7o3kIe0Aul\n" \
"tg+hN4ZNUS+WbO9vweUSdvLE0xAwNls7Gx5QalOIP3JahugLhm+tGNgobJSRoYoI\n" \
"sFMQZaVo4PAZChbqrYu7s1LrtOopeFeKki02MD3NwXGqpfKCN4UNsfGMbwkfGpRt\n" \
"bGAEdRUCgYEA8ai8sFbMbTt7/QOpcqIoGP3kpl0K8n1tx3he+H5g+F6/hlCXiyeV\n" \
"Zlewfigfx5GW1LKbKeoQgd8Y2QM6xU4chHRikGQse5RqdMLG0/20+0tbTY1PKn8B\n" \
"QH0mJHhl29NXyTsqtusjWoZzzamL41lc4Y/l+mGqQ4V1L/rmI+463msCgYEA7+Xa\n" \
"oje5GOkJCnJpOzGAXfkLMEQ6YFtugBRfgyX3c2sjBnvEeTkaHx/95Cls0Kdwqr3v\n" \
"/ygM0kPOt0H7y4eZvlKIj6GdX0+t4O2aoXgZuMijNVnIERqNEz1OIvX9Ilv5lg/b\n" \
"Eekfax0cTbDdu+p9CB+6VaBJqIy65hRcjNBH5RcCgYAUnqk7Aqz+xQyXUjCrL1rs\n" \
"hv1zlIzSlBFB6+tumJn9l1gQReAoZ4A/80uD+Dh99tY/392NfgNakYa1PalOHJQi\n" \
"WSvv1hxVjxxmShhdDlDbAFsSCvSuU5fvwL34bq2CTE45RWsnoHiryL0o10awZ3ed\n" \
"Z4HgE2VLzZ9qMKZienlbcQKBgCta2vxeHbGGy/97VdFAzPYuv/rlGbe4TmwPQoOt\n" \
"JN9TCW1uiL9vtmzRl0zYv7WlzRLOaMUwM8D8SCuOXTcXNo3S1KNAjfRfrgjsZ/mu\n" \
"fteKSxSlOSb+KWjEt45R7oF7Jcwc6XZ/LxJonGjeAfSoGBiTw1UeNrGjXVOfcmpw\n" \
"ac3ZAoGBAOoSIqLSUN5fL5+k5J040YiNMpOJtJ0pEfiOgO716Xfl6VgjDAccpKSu\n" \
"DR6XRHCcfI/UceXp7wmfJQ/CcmpqaKe3taPg5VaHS+SDR0ka/hZFkOeVvdgq4kAs\n" \
"Rw6/f7e9xvBWCQKghZIPvueEK6IwW3cwFMEIe4g+I5VEygUzEbrb\n" \
"-----END RSA PRIVATE KEY-----\n"
</code></pre>
</details>

### Configure WiFi
1. Open `wifi_config.h` from the project tree
2. Modify the following lines, using your network name (WIFI_SSID) and password (WIFI_PASSWORD):
```
#define WIFI_SSID                        "<SSID>"
#define WIFI_PASSWORD                    "<password>"
```

### Select the Ready Model
1. Open `common.mk` from the project tree
2. Modify the following line to select the Gesture Ready Model

```
MODEL_SELECTION = GESTURE_MODEL
```

### Build
1. Click **File -> Save**
2. Click **Terminal -> Run Task**
3. Select **Build** from the dropdown

Continue on to the **Hardware Setup** while waiting for the build to complete. 

## 9. Hardware Setup
1. Connect the USB-C port from the board to your PC. Ensure you use the port identified in the image below.<br>![image](./media/debug-usb-port.png)
2. Connect the board's debug port to a USB port on your PC. A new USB device should be detected. Firmware logs will be available on that COM port.
3. Open the Serial Terminal application and configure as shown below:
   * Port: (Select the COM port with the device)
   * Speed: `115200`
   * Data: `8 bits`
   * Parity: `none`
   * Stop Bits: `1`
   * Flow Control: `none`

## 10. Program Board
1. Select **Terminal -> Run Task**
2. Select **Program** from the dropdown

## 11. Verify Data
* Check in the serial terminal application that various gestures are detected:
```
>: {"d":[{"d":{"version":"?-1.1.1","random":77,"class_id":2,"class":"SwipeDown","event_detected":true}}]}
```

* Return to /IOTCONNECT and verify the device is reported as **CONNECTED** and that **Live Data** is visible.

## 12. Import Dynamic Dashboard

## 13. Resources
* Learn more about [/IOTONNECT integration of Infineon DEEPCRAFT Ready Models](https://github.com/avnet-iotconnect/avnet-iotc-mtb-psoc-edge-rm)
* [Purchase the Infineon PSOC Edge E84 AI Kit](https://www.newark.com/infineon/kitpse84aitobo1/ai-eval-kit-32bit-arm-cortex-m55f/dp/49AM4459)
* [More /IOTCONNECT Infineon Guides](https://avnet-iotconnect.github.io/partners/infineon/)
* [/IOTCONNECT Overview](https://www.iotconnect.io/)
* [/IOTCONNECT Knowledgebase](https://help.iotconnect.io/)
