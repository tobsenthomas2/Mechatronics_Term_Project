# Term Project
ME-405-03-2232 term project

# Instruction
The goal of this project is to conduct a duel. This duel will be conducted with a "launcher" or a nerf gun that we have added attachments to to fit our specific needs. The duel is conducted by shooting an opponent opposite to the launcher, with points awarded for a hit and subtracted for a miss. Upon running the code, the launcher will be turned on, and rotate 180 degrees to start. From there, it will take data from a thermal camera. Based on where the thermal camera picks up the highest heat concentration, the program will run to move the launcher to the position of this heat concentration which is represented as an "X" in an 8x8 grid of the entire output of the thermal camera. Based on the dimensions of the table that we are "dueling" on, we calculated the 8 pitch positions and 8 yaw positions that the launcher may need to move to based on where the opponent is standing which are stored as radians in two lists. We added two pulley systems with two DC motors to control the pitch and yaw of the launcher. This is what we are using to control the positioning and to move the launcher to the position that was output by the thermal camera. 

We created a task function and utilized a scheduler that would trigger different tasks to run at varied set intervals. We adjusted these intervals to find the optimal interval that would give us a clean response and take up the least amount of processing time. For example, our motor runs at a smaller period than the _____. Using our thermal camera data, we adjusted the KP and KI values to get us within a range that is close enough to hit the target with our launcher. 

We plotted our response intitally with a generalized PID controller that simulated the dynamics of our system. After we built the launcher, we plotted the data from the response. Our overshoot and discontinuity was minimized using a KI and KP value of _____ and the best period we had was ____ ms. 

You can see the dataset in the following plot:
![alt text](https://github.com/tobsenthomas2/lab3/blob/main/FigurePeriodsTill60.png)


We also tried different higher values to see when it starts getting really bad. After about 110ms, there starts to be noticable discontinuity, while below 110ms the main issue is the motor overshooting. You can see that in the following Plot:

![alt text](https://github.com/tobsenthomas2/lab3/blob/main/PlotPeriodsTill200.png)


# How to use the programs:

To use this motor controller for our two motors, first set up the thermal camera to face the area that you want to target. Place the launcher 180 degrees away from the target. Now, plug in the micro controller and run the main function. 

To plot the response, run the readAndPlotOnPC.py program, with your computer attached to the ST-LINK on the microcontroller. Ensure that the port is set to the correct USB terminal on your computer. This is in addition to the cable you have set up to run micropython on the microcontroller. Now run the main program and wait for the motion to stop. The plot should appear in the window of your read and plot program. 

# Conclusion:
We can go up to period=100, but we have an overshoot of 10%, which is too high for the upcoming project.
We will be using a period of 60 for the future as that only has an overshoot of 2.5%, which should be good enough for our applications. As this is also 6 times slower than the original 10 ms interval it gives us plenty of processing time.
