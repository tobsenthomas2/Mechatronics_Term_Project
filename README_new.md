# Term Project

ME-405-03-2232 term project

--> WHAT WE NEED: An introduction to your project. What is the purpose of the device you have created? For whose use is it intended?
An overview of the hardware design.  We need to know about the hardware on which the software in your repository will operate.
An overview of the software design. This should be brief and general, with a link to your Doxygen pages -- the pages describe the details of the software, so there's no need to repeat that here.
A discussion of the results. How did you test your system?  How well has your system performed in these tests?
A brief discussion of what you've learned about the project and recommendations for anyone who would like to build upon your work. This does not mean a discussion of what you learned about mechatronics in general; that belongs in other places. It is a discussion of what worked well and what didn't for this device.
Links to additional files as appropriate.  For example, if you have a directory containing CAD drawings, you might provide a link here.


# Instruction/Overview:

The goal of this project is to conduct a duel. This duel will be conducted with a "launcher" or a nerf gun that we have added attachments to to fit our specific needs. The duel is conducted by shooting an opponent opposite to the launcher, with points awarded for a hit and subtracted for a miss. Upon running the code, the launcher will be turned on, and rotate 180 degrees to start. From there, it will take data from a thermal camera. Based on where the thermal camera picks up the highest heat concentration, the program will run to move the launcher to the position of this heat concentration which is represented as an "X" in an 8x8 grid of the entire output of the thermal camera. Based on the dimensions of the table that we are "dueling" on, we calculated the 8 pitch positions and 8 yaw positions that the launcher may need to move to based on where the opponent is standing which are stored as radians in two lists. We added two pulley systems with two DC motors to control the pitch and yaw of the launcher. This is what we are using to control the positioning and to move the launcher to the position that was output by the thermal camera. 

We created a task function and utilized a scheduler that would trigger different tasks to run at varied set intervals. We adjusted these intervals to find the optimal interval that would give us a clean response and take up the least amount of processing time. For example, our motors run at 20ms with the yaw motor (motor 1) having task priority 1 and the pitch motor (motor 2) having priority 2. Mastermind, the main hub for our motor launching capabilities has a priority of 1 and period of 200ms. The camera functions have a priority of 4 with a period of 500ms. Using our thermal camera data, we adjusted the KP and KI values to get us within a range that is close enough to hit the target with our launcher. 

Launcher Overall:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/IMG_2658.heic)


# Testing:

We plotted our response intitally with a generalized PID controller that simulated the dynamics of our system. After we built the launcher, we plotted the data from the response. Our overshoot and discontinuity was minimized using a KI value of 0.005 and KP value of 0.025 and the best period we had was 20 ms.

We tried differing values for the KP and KI gain values, however when we increased KI too large, we found that we overshot too much, and similarly with the KP value.

Failed Test Trial:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/BadTest.MOV)

Launcher Testing:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/IMG_2624.MOV)

Launcher Testing:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/IMG_2658.mov)

# Software Overview:

We utilized cotask and task share in our code. Cotask is a multitasking real-time software from cotask.py. For communication between our tasks, we used interrupt service routines and cooperatively scheduled "regular" tasks as found in task_share.py. We also used the "time" library for timing functionality and referenced GPIO pins as well as PWM. We used i2c to send and recieve data between different components. 

# Hardware Overview:

We ran our MicroPython on the Nucleo-64 boards from ST Microelectronics with a simple custom board called the Shoe of Brian which sits below the Nucleo and houses a USB OTG connector. The specific board is a Nucleo-L476RG board.

We used two AMETEK/PITTMAN PG6712A077-R3 6665 motors, one SMRAZA SG90 micro servo motor, and one MLX9040 thermal camera. We ran these on the nucleo at 12 VDC with 0.5 A.

Motor Drawing:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/MotorSpecs.jpeg)

Nucleo Pins:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/NucleoPins.png)

Thermal Camera:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/ThermalCamera.png)

Micro Servo Motor:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/MicroServo.png)


Our design utilizes two pulley systems to steer our launcher, with a servo motor that triggers the launcher itself. The design implements laser cut and 3d printed pieces, along with one purchased piece from HomeDepot. 

The piece from HomeDepot consists of essentially ball bearings between two plates that allows for rotation. We can spin this piece to change the yaw of the launcher.

A picture is shown here:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/HomeDepotLazySusan.png)

The lasercut pieces are made from 0.25 inch plywood. These are the base plates that the NERF gun sits on, as well as the main base plate, and the other base plates.

The individual CAD files are shown here:

Base Plate:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/BasePlate.png)

Rotating Base Plate:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/BasePlate.png)

Nerf Gun Mounting Plate:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/GunBasePlate.png)

Vertical Motor Mounting Connector Piece:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/MotorMounting.png)

The 3D printed pieces are 4 gears, 2 motor mountings, a NERF rail mounting and gun body mounting, as well as a mounting piece for one of the rotating plates and two stands for the rotating pitch plate. The gear ratios were 1:8.33 for yaw pulley mechanism and 1:8 for the pitch pulley mechanism

The individual CAD files are shown here:

Motor Mountings:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/MotorHolder.png)

Nerf Gun Mount:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/NerfMounting.png)

Nerf Rail Mount:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/NerfRailMount.png)

Spur Gear(s):
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/SpurGear.png)

Pitch Gear:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/RotatingBigPitchGear.png)

Yaw Gear:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/BaseBigGear.png)

Rotating Mount:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/RotatingMount.png)

Nerf Mounting Plate Connector:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/SmallMount.png)

The overall assembly is shown here:
![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/Assembly.png)


# How to use the programs:

To use this motor controller for our two motors, first set up the thermal camera to face the area that you want to target. Place the launcher 180 degrees away from the target. Now, plug in the micro controller and run the main function. 

To plot the response, run the readAndPlotOnPC.py program, with your computer attached to the ST-LINK on the microcontroller. Ensure that the port is set to the correct USB terminal on your computer. This is in addition to the cable you have set up to run micropython on the microcontroller. Now run the main program and wait for the motion to stop. The plot should appear in the window of your read and plot program. 

# Conclusion:

We can go up to period = 100, but we have an overshoot of 10%, which is too high for the upcoming project.
We will be using a period of 60 for the future as that only has an overshoot of 2.5%, which should be good enough for our applications. As this is also 6 times slower than the original 10 ms interval it gives us plenty of processing time.

In terms of what worked well, the actual PI controller was good for the level of accuracy we needed. We were able to get it accurate enough to hit the target without being completely "dead-on". If there is a need for it to be quite precise, the controller would need to be tuned more. 

The base itself worked well for out needs, but was quite "clunky". There were many issues with screws that would get in the way of the rotating mechanisms that we did not account for. Because of this, we had to reprint and recut pieces or add "buffer" like pieces to provide a gap for clearance for the screws. The motion itself was a bit jerky, but again, it was precise enough so that did not matter to us.

The belt and pulley system worked quite well, but we had to staple the belt together. It would likely be better to buy a standard belt that comes assembled, so that there is not a need to put it together as it might rip over time.

For those using this, it is important that the positions are set for one's specific range that their thermal sensor can detect and that they want to aim in. 
