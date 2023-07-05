![Visitor Count](https://profile-counter.glitch.me/{kennethmikoliachik}/count.svg)

#### Working on: (5/11/2023)

• **Enabling real time face tracking, get TensorFlow to control pan/tilt motors.**
• **Finding a suitable server to host Pi Image (2.5GB+).**
• **Building reverse kinematic model and program for defining walking parameters.**
• **Training a hand signal model that Regis will respond to**

# Regis Quadruped Robot
![Regis Looking Cool](https://github.com/kennethmikolaichik/Regis/blob/main/Fun%20Progress%20Pics/the_readme_pic.jpg)

####Download the Pi Image here:  ##insert link##

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Inspiration and General Description
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
This project started out as a desire to bring to life a teachable basic droid.
I could see that the technology existed, but there seemed to only be a few entities making any real progress. This work is largely the coupling together of several other open-source projects. I have brought together an easily buildable and affordable set of hardware in hopes that this project might be used for research into AI. I believe that the decentralization of AI and its distribution to the public is an important step in an agreeable future.

Regis is a basic mobile quadrupedal chassis, power source, and two axis camera head designed loosely around a spider (although 4 legged).
He sports three degrees of freedom in his legs, and the motors easily support his light weight. Although battery life is limited due to the power requirements of the Raspberry Pi and SSD (maybe 1/2 hour), he can easily run plugged in on a tabletop due to his small size.

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

![Chassis Cad Model](https://github.com/kennethmikolaichik/Regis/blob/main/Fun%20Progress%20Pics/chassis_cad_pic.png)

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
For advanced users you may want to set up SSH to dial into your spider.
Otherwise connect a monitor (or tv) to the micro HDMI port.
Connect a mouse and keyboard to the Raspberry Pi USB ports. I highly recommend a wireless keyboard and mouse combo. I use a logitec model.
Currently running the official raspberry pi GUI, 32 bit for reliability reasons.

A Note about Software:
Make sure you have Python 3 installed as some of the camera software will not work correctly with Python 2 and below.
The servo PWM timing is written with the aid of the PiGPIO library:
https://abyz.me.uk/rpi/pigpio/

![Look Up](https://github.com/kennethmikolaichik/Regis/blob/main/Fun%20Progress%20Pics/Head%20to%20Chassis%20incorporation!.jpg)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Using Your Spider
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Now that your very own 'Regis' robot is up and running. Download all files in >Code Bits to your robot’s local directory.

1). First, update everything. Open the command terminal and type:

    sudo apt -get update

The files in the directory 'Awaken' Can be run to control the legs and head. 

2). Now type: 

    sudo pigpiod

Hit enter. This will engage the PiGPIO daemon to run in the background. This will allow the motor controller to run.

3). Move to the directory containing the motor control files, if you copied the entire directory, it will be in Code Bits > Awaken:

    cd Awaken/Old_Programs

 Now try out:

    Python3 Leg1_UP.py

The robot should lift its front right leg and the terminal should output "completed successfully"

The remaining motor control files in this folder can be run in this manner through the command line.

Now, run the folowing program from the command line of your pi to control the robots movment and camera. It is the main interface I have created for controlling the robot:

    cd Awaken
   
    python3 Initialize.py


#### I am currently in the process of setting up leg control software so that the robot can walk and run. I am investigating different Inverse Kinematic solving libraries to this end. I am also writing programs to display all of the servo motor angles and location position of each motor in real time. 5.11.2023
• 'Klampt' python library seems useful. Also see this walkthrough: https://hackaday.io/project/171456-diy-hobby-servos-quadruped-robot/log/177488-lets-talk-about-the-kinematic-model

#### I have begun the process of designing Regis V0.2, this robot will have a 10Ah battery, larger servos, and will run on Ubuntu-64x with the robot operating system(ROS) and a separate Arduino as the motor controller.

