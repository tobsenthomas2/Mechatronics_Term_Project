# Term Project

ME-405-03-2232 term project
Sydney Gothenquist, Toby Darci, Toby Thomas


# Instruction/Overview:

The goal of this project is to conduct a duel. This duel will be conducted with a "launcher" or a nerf gun that we have added attachments to to fit our specific needs. The duel is conducted by shooting an opponent opposite to the launcher, with points awarded for a hit and subtracted for a miss. Upon running the code, the launcher will be turned on, and rotate 180 degrees to start. From there, it will take data from a thermal camera. Based on where the thermal camera picks up the highest heat concentration based on 64 chucks which represent the average value of a selection of pixels, the program will run to move the launcher to the position of this heat concentration which is represented as an "X" in an 8x8 grid of the entire output of the thermal camera. Based on the dimensions of the table that we are "dueling" on, we calculated the 8 pitch positions and 8 yaw positions that the launcher may need to move to based on where the opponent is standing which are stored as radians in two lists. We added two pulley systems with two DC motors to control the pitch and yaw of the launcher. This is what we are using to control the positioning and to move the launcher to the position that was output by the thermal camera. 

We created a task function and utilized a scheduler that would trigger different tasks to run at varied set intervals. We adjusted these intervals to find the optimal interval that would give us a clean response and take up the least amount of processing time. For example, our motors run every 20ms with the yaw motor (motor 1) having task priority 1 and the pitch motor (motor 2) having priority 2. Mastermind, the main controller task, has a priority of 1 and period of 200ms. The camera functions have a priority of 4 with a period of 500ms. Using our thermal camera data, we adjusted the KP and KI values to get us within a range that is close enough to hit the target with our launcher. 

Launcher Overall:

![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/IMG_2658.png)


# Testing:

We plotted our response intitally with a generalized PID controller that simulated the dynamics of our system. For both axes, we had Kp = 30, Kd = 0.8, and Ki = 0.4. This shows the general response using an RK4 solver:

![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/CLxyPID3084.png)

After we built the launcher, we plotted the data from the response. Our overshoot and discontinuity was minimized using a KI value of 0.005 and KP value of 0.025 and the best period we had was 20 ms.

We tried differing values for the KP and KI gain values, however when we increased KI too large, we found that we overshot too much, and similarly with the KP value.

We tried with different values and made tables, so we could compare them, also we took the time. Following you can find one example tabele:
KP= 0.03
KI= 0.005

| Attempt | #1    | #2    | #1    | #2    | #1    |
| :-----: | :---: | :---: | :-----: | :---: | :---: |
| Hit | 1   | 0   | 1    | 0    | 0    | 
| Time to shoot | 1.2   | 6   | 1.01    | 3.76    | 2.01    | 

We created a matrix with all the values we wanted to compare and choose the best value for our use case. 
After we did that we saw, that only 5 attemts are too less and its not accurate enought, but we also had the feeling that the gun itself shoots random. So in the next itaration we would think more about that.


Failed Test Trial:


[![Watch the video](https://img.youtube.com/vi/YJh235cYVxw/0.jpg)](https://youtube.com/shorts/YJh235cYVxw?feature=share)

Launcher Testing:

[![Watch the video](https://img.youtube.com/vi/fPlxaU3ffSM/0.jpg)](https://youtube.com/shorts/fPlxaU3ffSM?feature=share)


Launcher Testing:

[![Watch the video](https://img.youtube.com/vi/-sAixdGBE94/0.jpg)](https://youtube.com/shorts/-sAixdGBE94?feature=share)


# Software Overview:

We utilized cotask and task share in our code. Cotask is a multitasking software from cotask.py with triggers specified tasks at regular intervals based on a specified period. Tasks have varying priority ranks, determining which task runs when both tasks attempt to run simultaneously. For communication between our tasks, we create different share objects for each variable or list needed to be referenced across tasks. For this we used the task share library which allows us to put a value to a shared variable and get a value from a shared variable across all tasks using the .put and .get functions. We also used the time library for timing functionality and referenced GPIO pins as well as PWM from the pyb library. We used i2c to recieve data from the thermal camera. 

# Hardware Overview:

We ran our MicroPython on the Nucleo-64 boards from ST Microelectronics with a simple custom board called "the Shoe of Brian" which sits below the Nucleo and houses a USB OTG connector. The specific board is a Nucleo-L476RG board.

We used two AMETEK/PITTMAN PG6712A077-R3 6665 motors, one SMRAZA SG90 micro servo motor, and one MLX9040 thermal camera. We ran these on the nucleo at 24 VDC with a 0.5 A limit.

Motor Drawing:

![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/MotorSpecs.jpeg)

Nucleo Pins:

![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/NucleoPins.png)

Thermal Camera:

![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/ThermalCamera.png)

Micro Servo Motor:

![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/MicroServo.png)


Our design utilizes two belt - pulley systems to steer our launcher, with a servo motor that triggers the launcher itself. The design implements laser cut and 3d printed pieces, along with a bearing and fasteners from Home Depot.

The bearing from Home Depot consists of essentially ball bearings between two plates that allows for rotation. We can spin this piece to change the yaw of the launcher.

A picture is shown here:

![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/HomeDepotLazySusan.png)

The lasercut pieces are made from 0.25 inch plywood. These are all of the pieces that could be created flat, as laser cutting is an extremely fast and accurate method of manufacturing but can only cut flat sheets.

The individual CAD files are shown here:

Base Plate:

![alt text](https://github.com/tobsenthomas2/Mechatronics_Term_Project/blob/main/BiggestBasePlate.png)

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

To use this motor controller for our two motors, first set up the thermal camera to face the area that you want to target. If you are setting it up exactly how we did for this project, the angles should be calibrated, if not do the following: Input the width that the camera can see at the distance it is shooting, the height of the gun relative to the bottom of the camera frame, and the height of the image into the testpitchandyawtables.py file. Run this program on your PC and copy and paste the output lists from this program into the yaw and pitch tables in MasterMind.

Rotate the launcher so it is 180 degrees away from the target. Now, plug in the micro controller and run the main function. 

# Conclusion:

We can go up to period = 100, but we have an overshoot of 10%, which is too high for the upcoming project.
We will be using a period of 60 for the future as that only has an overshoot of 2.5%, which should be good enough for our applications. As this is also 6 times slower than the original 10 ms interval it gives us plenty of processing time.

In terms of what worked well, the actual PI controller was good for the level of accuracy we needed. We were able to get it accurate enough to hit the target without being completely "dead-on". If there is a need for it to be quite precise, the controller would need to be tuned more. 

The base itself worked well for out needs, but was quite "clunky". There were many issues with screws that would get in the way of the rotating mechanisms that we did not account for. Because of this, we had to reprint and recut pieces or add "buffer" like pieces to provide a gap for clearance for the screws. The motion itself was a bit jerky, but again, it was precise enough so that did not matter to us.

The belt and pulley system worked quite well, but we had to staple the belt together. It would likely be better to buy a standard belt that comes assembled, so that there is not a need to put it together as it might rip over time.

For those using this, it is important that the positions are set for one's specific range that their thermal sensor can detect and that they want to aim in. 
