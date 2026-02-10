# Lab: AI Vision Demo on STM32MP1 Devices with AWS IoT greengrass nucleus lite

## 1. Overview
In this Lab we will setup an AI Vision Demo on an STM32MP1 device by using Avnet's /IOTCONNECT platform to simplify the process.  
The AI Vision Demo software is contained within an AWS greengrass component that will be deployed to the AWS Greengrass nucleus lite running on the device via the Avnet /IOTCONNECT platform.  

## 2. Prerequisites
This guide assumes that you already have a device running the AWS Greengrass nucleus lite, an /IOTCONNECT account and the hardware and software outlined in the QuickStart guide (below).  

If not, please follow the [STM32MP157F-DK2](https://github.com/avnet-iotconnect/iotc-python-greengrass-demos/tree/main/stm32mp157f-dk2) or [STM32MP135F-DK](https://github.com/avnet-iotconnect/iotc-python-greengrass-demos/tree/main/stm32mp157f-dk2) Greengrass nucleus lite QuickStart through to the section on component deployment then return to this guide.

> [!NOTE]
> Topics covered in the QuickStart guides, above:
> 1. Create an /IOTCONNECT account
> 2. Import an example **Device Template** in /IOTCONNECT
> 3. Create a **Greengrass Device** in /IOTCONNECT
> 4. Setup **nucleus lite** on the target device

In addition to the Hardware and Software requirements in the QuickStart guide, you will also need a **UVC-Compliant USB Camera** such as [this one](https://www.amazon.com/ALPCAM-Distortion-Compliant-Embedded-Industrial/dp/B0B1WTV1KB?th=1).

## 3. Deploy the Vision AI Greengrass Component
To deploy the Vision AI greengrass component, we'll use /IOTCONNECT to create a deployment package that contains the artifact file and a recipe.
* **Download** and **Extract** the *Vision AI Demo Component*: [iotc-gg-component-st-ai-vision-1.0.0.zip](https://downloads.iotconnect.io/greengrass/components/iotc-gg-component-st-ai-vision-1.0.0.zip)

### Load the Recipe
1. In the /IOTCONNECT platform, click **Package** at the bottom of the screen, then click **Components** at the top.

<img width="1015" height="84" alt="click_package" src="https://github.com/user-attachments/assets/da800a4d-f5cf-4cd6-9438-ccefb5056501" />

<img width="570" height="211" alt="click_components" src="https://github.com/user-attachments/assets/1ea5ae9d-c9e7-4abd-815b-6e4e6572a0d1" />

2. In the "Create Component" box, browse for the recipe file ("recipe.yaml") from the previously extracted component archive here:  `<your working directory>\iotc-gg-component-st-ai-vision-1.0.0\st-ai-vision\greengrass-build\recipes\recipe.yaml`

### Load the Artifact 
1. Click the icon to the right of "dhm-demo.zip" and navigate to the dhm-demo.zip from the previously extracted archive here: `<your working directory>\iotc-gg-component-st-ai-vision-1.0.0\st-ai-vision\greengrass-build\artifacts\io.iotconnect.example.IotConnectStAiVision\1.0.0\st-ai-vision.zip`
2. Click **Save**

### Create Package
1. Verify the component is now list and at the top-right, click **Package**

<img width="390" height="167" alt="create_package" src="https://github.com/user-attachments/assets/ac41c5ae-0d45-444b-8357-72d1c41f01e6" />

2. Enter a *Name* such as `VisionAIdemo`
3. Select the `ggsdkdemo` Template
4. Select the **Custom Component** in the drop-down

5. Click **Save**

### Deploy Package
1. **Click** **Deploy**

<img width="567" height="155" alt="click_deploy" src="https://github.com/user-attachments/assets/1b321aa8-9351-4b3d-b841-dfc12c91233f" />

2. Add a *Name* and select each item in the drop-downs (there will only be one option for each)
3. Ensure you tick the box under "Components" and pick the version `1.0.0`
4. **Click** *Deploy*

The package with the component is now being deployed to the device.

This process can take 5 min or more, so wait until you see "Success" in the Deployment History.

## 4. Import a Dynamic Dashboard
/IOTCONNECT Dynamic Dashboards are an easy way to visualize data and interact with edge devices.  
* Download the *Vision AI Demo* dashboard: [greengrass-nucleus-lite-dashboard.json](../greengrass-nucleus-lite-dashboard.json)

* Switch back to the /IOTCONNECT browser window and verify the device status is displaying as `Connected`
* **Click** `Create Dashboard` from the top of the page
* **Select** the `Import Dashboard` option and **Click** *Browse* to select the dashboard template previously downloaded.
* **Select** the *Template* ("ggsdkdemo") and your *Device Name*
* **Enter** a name (such as `My STM32MP1 Greengrass Dashboard`) and **Click** *Save* the finalize the import


## 5. Resources
* [Purchase the STM32MP135F-DK](https://www.newark.com/stmicroelectronics/stm32mp135f-dk/discovery-kit-32bit-arm-cortex/dp/68AK9977)
* [Purchase the STM32MP157F-DK2](https://www.newark.com/stmicroelectronics/stm32mp157f-dk2/discovery-kit-arm-cortex-a7-cortex/dp/14AJ2731)
* Try out the other available [greengrass lite components](https://github.com/avnet-iotconnect/iotc-python-greengrass-sdk/tree/main/examples)
* Learn more and develop your own components: [iotc-python-greengrass-sdk](https://github.com/avnet-iotconnect/iotc-python-greengrass-sdk)
* [More /IOTCONNECT ST Guides](https://avnet-iotconnect.github.io/partners/st/)
* [/IOTCONNECT Overview](https://www.iotconnect.io/)
* [/IOTCONNECT Knowledgebase](https://help.iotconnect.io/)