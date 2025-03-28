Welcome! Visitor number:
![Visitor Count](https://profile-counter.glitch.me/{kennethmikoliachik}/count.svg)

# Regis Quadruped Robot
![Regis Looking Cool](https://github.com/kennethmikolaichik/Regis/blob/main/Progress%20Pictures/the_readme_pic.jpg)



https://github.com/kennethmikolaichik/Regis/assets/14054289/5544b9f7-79c9-4541-8287-6319b5d9ae8c


- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Inspiration and General Description
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
This project started out as a desire to bring to life a teachable basic droid.
I could see that the technology existed, but there seemed to only be a few entities making any real progress. This work is largely the coupling together of several other open-source projects. I have brought together an easily buildable and affordable set of hardware in hopes that this project might be used for research into AI. I believe that the decentralization of AI and the distribution of uniquely trained models to the public is an important step in an agreeable future.

Regis is a basic mobile quadrupedal chassis, power source, and two axis camera head designed loosely around a spider (although 4 legged).
He sports three degrees of freedom in his legs, and an onboard computer running linux. Although battery life is limited due to the power requirements of the Raspberry Pi and SSD (maybe 1/2 hour), he can easily run plugged in on a tabletop due to his small size.

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

Servos: MG90S

Power Converter: UCTRONICS DC 6V-24V to DC 5V 5A Buck Converter Module, 9-36V Step Down to USB 5V Transformer Dual Output Voltage Regulator Board

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Chassis
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

![Chassis Cad Model](https://github.com/kennethmikolaichik/Regis/blob/main/Progress%20Pictures/chassis_cad_pic.png)

Use Regis > CAD FILES > Version 0.0
All structural pieces have been 3D printed using PLA and ABS filament on an Ender 3. Any G-code files will be for this setup. Recommend high percentage to solid infill.

All working CAD files have been created in FreeCAD Version 0.19 - (.FCStd) filetype. Please convert if using another program. Or fall in love with Freecad at https://www.freecad.org/ 

The robots "shoes" have been constructed from rubber stoppers from the hardware store. They are necessary for any sort of traction on smooth surfaces. Purchase 1/2 inch stoppers and drill halfway through with a 7/64" or 1//4" drill bit. Clean out the holes and slide on the ends of the legs.

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
The legs for this project are assembled with the screws that come with the MG90 Servos. They are 2.5mm. The battery case is assembled with M8 machine screws. The raspberry pi is installed in the case and held to the upper surface of the battery/case with double sided tape. The fan is attached to the upper portion of the raspberry pi case with some oversized screws that penetrate into the honeycomb skin of the raspberry pi case. The SSD is attached with double sided tape, electrical tape is used to shield the IC's from contact with the tape and prevent stray current. Twist ties are employed throughout the robot for wire control and routing. Rubber bands have been used to 'tidy up' the wires coming from the power distribution board and signal wires. 

*NOTE: This is a prototype and will be constantly changing which is why I have opted for impermanent fastening of nonstructural components.

For all wiring: SEE DIAGRAMS - You will need to 1) Plug the battery into the power converter. 2) Wire the power distribution board to the power converter. 3) Route and plug in all motors to the power distribution board. 4) Connect all signal wires to their proper Raspberry Pi GPIO pin. 5) Connect the fan to the power converter output (this way it will always be on when the battery is on) 6) plug in the SSD/mSATA to USB adapter and then into pi. The camera requires a ribbon cable.

And that’s it!

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Interface
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#### Download the Pi Image here: https://downloads.raspberrypi.org/raspios_full_armhf/images/raspios_full_armhf-2023-05-03/2023-05-03-raspios-bullseye-armhf-full.img.xz

For advanced users you may want to set up SSH to dial into your spider.
Otherwise connect a monitor (or tv) to the micro HDMI port.
Connect a mouse and keyboard to the Raspberry Pi USB ports. I highly recommend a wireless keyboard and mouse combo. I use a logitec model.
Currently running the official raspberry pi GUI, 32 bit for reliability reasons.

You will now need to install a large number of packages and programs. Make sure you have Python 3 installed as some of the camera software will not work correctly with Python 2 and below.
From the terminal/command line, install the following packages. This is necessary in order for the python packages to be imported sucessfully when the Robot Control scripts are run in the next section. First ensure that 'wheels' and 'python3' are installed. Then pip install the following python modules:  os, playsound, subprocess, math, numpy, pigpio, time, pyttsx3, and pygame.

You will need to follow the documentation to install openCV, https://opencv.org/get-started/
    
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
Now that your very own 'Regis' robot is up and running. Download all files to your robot’s local directory.

1). First, update everything. Open the command terminal and type:

    sudo apt update && sudo apt upgrade -y

The files in the directory 'Code_Bits/Old_Programs' Can be run to control the legs and head. 

2). Now type: 

    sudo pigpiod

Hit enter. This will engage the PiGPIO daemon to run in the background. This will allow the motor controller to run.

3). Move to the directory containing the motor control files, if you copied the entire directory, it will be in Code_Bits/Old_Programs:

    cd Code_Bits/Old_Programs

 Now try out:

    Python3 Leg1_UP.py

The robot should lift its front right leg and the terminal should output "completed successfully"

The remaining motor control files in this folder can be run in this manner through the command line.

Now, run the folowing program from the command line of your pi to control the robots movment and camera. This file is the main interface I have created for controlling the robot:

    cd Awaken
   
    python3 Initialize.py


"Anything is possible if you can only imagine it."

Have a wonderful day!

