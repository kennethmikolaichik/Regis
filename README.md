# Regis Quadruped Robot
![Regis Looking Cool](https://github.com/kennethmikolaichik/Regis/blob/main/Progress%20Pictures/the_readme_pic.jpg)



https://github.com/kennethmikolaichik/Regis/blob/main/Progress%20Pictures/Showcase.mp4


- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Inspiration and General Description
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
This project started out as a desire to bring to life a teachable basic robot.

The robot is a basic mobile quadrupedal chassis, power source, and two axis camera head designed loosely around a spider. Although battery life is limited due to the power requirements of the Raspberry Pi and SSD, it can easily run plugged in on a tabletop.

Long live Regis!

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Technical Specifications
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Computer: Raspberry pi 4B 2GB Ram

Camera: Raspberry Pi Cam Version 2.1

Fan: 50 x 50 x 10mm (5V)

Hard Drive: Kingston mSATA SSD (recommend 128GB or greater)

HD Converter: Eluteng mSATA to usb3.0 adapter

Battery: DC 12300 - DC12V Rechargeable 3000mAh lithium-ion Battery

Servos: 14 x MG90S

Power Converter: UCTRONICS DC 6V-24V to DC 5V 5A Buck Converter Module, 9-36V Step Down to USB 5V Transformer Dual Output Voltage Regulator Board

Screws:

M2.5 for MG90S mounting


M4 for structure

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Chassis
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

![Chassis Cad Model](https://github.com/kennethmikolaichik/Regis/blob/main/Progress%20Pictures/8.25.2025.png)

Use Regis > CAD & .stl files > Version 0.0
All structural pieces are 3D printed using PLA or ABS filament. Recommend high percentage to solid infill.

CAD files have been created in FreeCAD Version 0.19 - (.FCStd) filetype. 

Freecad: https://www.freecad.org/ 

The robots "shoes" have been constructed from rubber stoppers from the hardware store. They are necessary for any sort of traction on smooth surfaces. Purchase 1/2 inch stoppers and drill halfway through with a 7/64" or 1/4" drill bit. Clean out the holes and slide on the ends of the legs.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Power Distribution Board
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
The power distribution board for the 14 motors is a necessity. For this, purchase a header set and a small piece of protoboard (~5 inches). The protoboard can be easily cut with a box cutter. Score one side and snap against a hard, clean edged surface. solder the positive, negative, and signal traces like so:

![PDP Pic](https://github.com/kennethmikolaichik/Regis/blob/Branch-1/Wiring%20Diagrams/Power%20Distribution%20Board.jpg)

\"- - - - - - - - - - - - - - -"•  ← negative lead from power converter\
\" + + + + + + + + + +"•  ← positive lead from power converter\
s1 s2 s3 s4 s5 s6 ...... s14   ← signal wire IN from motor  
s1 s2 s3 s4 s5 s6 ...... s14   ← signal wire OUT to Pi


Solder all positive pins together. Solder all negative pins together. Solder the pairs of signal pins together.
This way the 3-pin connector for each leg can be bundled together and a motor easily removed if needed. You may want to create some extra slots if you plan on connecting more motors or other 5V equipment. See pictures.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Method of Assembly
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
The legs for this project are assembled with the screws that come with the MG90 Servos. They are 2.5mm. The battery case is assembled with M4 machine screws. The raspberry pi is installed in the case and held to the upper surface of the battery/case with double sided tape. The fan is attached to the upper portion of the raspberry pi case with some oversized wood screws. The SSD is attached with double sided tape, electrical tape is used to shield the IC's. Twist ties are employed throughout the robot for wire control and routing.

For wiring: You will need to 1) Plug the battery into the power converter. 2) Wire the power distribution board to the power converter. 3) Route and plug in all motors to the power distribution board. 4) Connect all signal wires to their proper Raspberry Pi GPIO pin. 5) Connect the fan to the power converter output (this way it will always be on when the battery is on) 6) plug in the SSD/mSATA to USB adapter and then into pi. The camera requires a ribbon cable.

See Diagrams

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Interface
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#### Download the Pi Image here: https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2023-05-03/2023-05-03-raspios-bullseye-armhf-full.img.xz

For advanced users you may want to set up SSH to dial into your spider.
Otherwise connect a monitor (or tv) to the micro HDMI port.
Connect a mouse and keyboard to the Raspberry Pi USB ports. I highly recommend a wireless keyboard and mouse combo. Currently running the official raspberry pi GUI, 32 bit for reliability reasons.

You will now need to install some packages and programs. Make sure to use Python 3 as some of the camera software will not work correctly with Python 2 and below. From the terminal/command line, install the following packages. 

	sudo apt-get install -y \
	  python3 python3-pip python3-numpy python3-pygame python3-pigpio \
	  pigpio espeak-ng espeak-ng-data libespeak-ng1 build-essential python3-dev

	python3 -m pip install playsound pyttsx3 --break-system-packages

This is necessary in order for the python packages to be imported sucessfully when the Robot control script is run in the next section.

You may want to install some computer vision software. (not necessary)

To install openCV, https://opencv.org/get-started/
    
    pip3 install opencv-python

Also follow this video and documentation to install Tensorflow Lite, https://www.youtube.com/watch?v=Lyh84KMqUPI

https://www.tensorflow.org/lite/guide/python

    python3 -m pip install tflite-runtime

A Note about Software:
The servo PWM timing is written with the aid of the PiGPIO library:
https://abyz.me.uk/rpi/pigpio/

![Look Up](https://github.com/kennethmikolaichik/Regis/blob/main/Progress%20Pictures/Head%20to%20Chassis%20incorporation!.jpg)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Using Your Spider
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Now that your very own 'Regis' robot is up and running. Download "Initialize.py" to your robot’s local directory.

1). First, update everything. Open the command terminal and type:

    sudo apt update && sudo apt upgrade -y

The files in the directory 'Code_Bits/Old_Programs' Can be run to control the legs and head. 

2). Now type: 

    sudo pigpiod

Hit enter. This will engage the PiGPIO daemon to run in the background. This will allow the motor controller to run.

3). Now, run the folowing program from the command line of your pi to control the robots movment and camera. This file is the main interface I have created for controlling the robot:

   
    python3 Initialize.py
