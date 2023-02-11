README
2/10/2023

# Regis Quadroupled Robot


This project started out as a desire to bring to life a teachable basic droid.
I could see that the technology existed, but there seemed to only be a few entities making any real progress. This work is largely the coupling together of several other open source projects. I have brought together an easily buildable and affordable set of hardware in hopes that this project might be used for research into AI. I believe that the decentralization of AI and its distribution to the public is an important step in an agreeable future.

Regis is a basic chassis, power source, and two axis camera head designed loosely around a spider (although 4 legged).
He sports three degrees of freedom in his legs, and the motors easily support his light weight. Although battery life is limited due to the power requirements of the Raspberry Pi and SSD, he can easily run plugged in on a table top due to his small size.

Please share any and all mods and improvements! Long live Regis!

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Technical Specifications
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Computer: Raspberry pi 4B 2GB Ram

Camera: Raspberry Pi Cam Version 2.1

Fan: 50 x 50 x 10mm

Hard Drive: Kingston SSD KC600 2.5" and mSATA SSD

HD Converter: Eluteng mSATA to usb3.0 adapter

Battery: DC 12300 - DC12V Rechargeable 3000mAh lithium-ion Battery

Servos: MG90S

Power Converter: UCTRONICS DC 6V-24V to DC 5V 5A Buck Converter Module, 9-36V Step Down to USB 5V Transformer Dual Output Voltage Regulator Board

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Chassis
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
All structural pieces have been 3D printed using PLA filament on an Ender 3. Any G-code files will be for this setup.

All CAD files have been created in FreeCAD Version 0.19 - please convert the filetype if using another program.

Shoes have been constructed from rubber stoppers from the hardware store (drill halfway through and slide on legs).

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Power Distribution Board
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
The power distribution board for the 14 motors is a necessity. For this, purchase a header set and a small piece of protoboard (~5 inches). The protoboard can be easily cut with a box cutter. Score one side and snap against a hard, clean edged surface. solder the positive, negative, and signal traces like so:

https://github.com/kennethmikolaichik/Regis/blob/Branch-1/Wiring%20Diagrams/Power%20Distribution%20Board.jpg

\"+ + + + + + + + + + + + + + +"  ← positive lead from power converter\
\"- - - - - - - - - - - - - - -"  ← negative lead from power converter\
s1 s2 s3 s4 s5 s6 ...... s14   ← signal wire IN from motor  
s1 s2 s3 s4 s5 s6 ...... s14   ← signal wire OUT to Pi


Solder all positive pins together. Solder all negative pins together. Solder the pairs of signal pins together.
This way the 3-pin connector for each leg can be bundled together and a motor easily removed if need. You may want to create some extra slots if you plan on connecting more motors or other 5V equipment. See pictures.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Method of Assembly
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
The legs for this project are assembled with the screws that come with the MG90 Servos they are 2.5mm. The battery case is assembled with M8 machine screws. the raspberry pi is installed in the case and held to the upper surface of the battery/case with double sided tape. The fan is attached to the upper portion of the raspberry pi case with some oversized screws that penetrate into the honeycomb skin of the raspberry pi case. The SSD is attached with double sided tape, electrical tape is used to shield the IC's from contact with the tape and prevent stray current. Twist ties are employed throughout the robot for wire control and routing. Rubber bands have been used to 'tidy up' the wires coming from the power distribution board and signal wires. 

*NOTE: This is a prototype and will be constantly changing which is why I have opted for impermanent fastening of nonstructural components.

For all wiring: SEE DIAGRAMS - You will need to 1) Plug the battery into the power converter. 2) Wire the power distribution board to the power converter. 3) Route and plug in all motors to power distribution board. 4) Connect all signal wires to their proper Raspberry Pi GPUIO pin. 5) Connect the fan to the power converter output (this way it will always be on when the battery is on) 6) plug in the SSD/mSATA to USB adapter.

And that’s it!

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
## Interface
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
For advanced users you may want to set up SSH to dial into your spider.
Otherwise connect to the micro hdmi port
Connect a mouse and keyboard to the Raspberry Pi USB ports
I am running the official raspberry pi GUI
