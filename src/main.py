"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2.
    
    Rename basic_tasks.py as main.py. Use the example of a
    task function in main.py and what you’ve learned in lecture
    to write a task which runs the closed-loop motor controller
    you have previously written. Hook up a motor from
    your tub and run this task using the cotask.py scheduler
    with its task timing at around 10 ms.
    
    Run the motor task on a motor with a flywheel, printing results and plotting
        step response graphs as you did in the previous exercise. Run the task at a
        slower and slower rate until the controller’s performance
        is noticeably worsened as shown on a step response plot. Record the slowest
        rate at which the performance is not significantly worse than when running
        the controller at a fast rate; this will help you choose a good run rate for
        the motor control task – it should be a bit faster than the slowest rate which
        works for a factor of safety. Save copies of the step response plots for the
        slowest rate at which the response is good and for a rate at which the
        response isn’t as good. Optional: Plot several responses on one set of axes,
        with a legend showing the task run rate of each.

Make two tasks which run two motors under closed-loop control at the same time.
Write a test program which moves your motors simultaneously through different
distances and holds them at the desired positions, and use it to test your code
as thoroughly as possible.
"""

import gc
import pyb
import cotask
import task_share
import pyb, time
import motor1
import motor2
#import trigger
import CameraRaw
import MasterMind



"""!This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
"""
if __name__ == "__main__":	
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    updatemotor = task_share.Share('B', thread_protect=False, name="Update_Motor")
    ready = task_share.Share('B', thread_protect=False, name="Ready")
    fired = task_share.Share('B', thread_protect=False, name="Fired")
    aim = task_share.Share('B', thread_protect=False, name="Aim")
    fire = task_share.Share('B', thread_protect=False, name="Fire")
    theta1 = task_share.Share('f', thread_protect=False, name="thetayaw")
    theta2 = task_share.Share('f', thread_protect=False, name="thetapitch")
    cameraon = task_share.Share('B', thread_protect=False, name="Cameraon")
    updateang = task_share.Share('B', thread_protect=False, name="updateang")
    position = task_share.Share('B', thread_protect=False, name="Position")
    KP = task_share.Share('f', thread_protect=False, name="KP")
    KI = task_share.Share('f', thread_protect=False, name="KI")
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    # task10 = cotask.Task(AIMINGFN, name="Aiming", priority=1, period=60,
    #                    profile=True, trace=False, shares=(aimingReady, q0))
    task1 = cotask.Task(motor1.Motor1, name="Motor_Yaw", priority=1, period=20,
                        profile=True, trace=False, shares=(updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI))
    task2 = cotask.Task(motor2.Motor2, name="Motor_Pitch", priority=2, period=20,
                        profile=True, trace=False, shares=(updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI))
    #task3 = cotask.Task(trigger.Trigger, name="Motor_Servo", priority=3, period=60,
                        #profile=True, trace=False, shares=(updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI))
    task4 = cotask.Task(MasterMind.mastermind, name="Master_Mind", priority=1, period=200,
                        profile=True, trace=False, shares=(updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI))
    task5 = cotask.Task(CameraRaw.cameraFN, name="Camera", priority=4, period=500,
                        profile=True, trace=False, shares=(updatemotor, ready, fired, fire, theta1, theta2, cameraon, updateang, position, aim, KP, KI))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    #cotask.task_list.append(task3)
    cotask.task_list.append(task4)
    cotask.task_list.append(task5)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
