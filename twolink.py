"""
quote from pythonrobotics

this is only test file
"""

import matplotlib.pyplot as plt
import numpy as np
import joyps4con
import time
import sys

# Similation parameters
Kp = 15
dt = 0.01

# Link lengths
l1 = l2 = 1

# Set initial goal position to the initial end-effector position
#x = 1
#y = 0

show_animation = True

if show_animation:
    plt.ion()


def two_joint_arm(GOAL_TH=0.0, theta1=0.0, theta2=0.0,x=0.5,y=0.5):
    """
    Computes the inverse kinematics for a planar 2DOF arm
    """

    while True:
        try:
            theta2_goal = np.arccos(
                (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2))
            theta1_goal = np.math.atan2(y, x) - np.math.atan2(l2 *
                                                              np.sin(theta2_goal), (l1 + l2 * np.cos(theta2_goal)))

            if theta1_goal < 0:
                theta2_goal = -theta2_goal
                theta1_goal = np.math.atan2(
                    y, x) - np.math.atan2(l2 * np.sin(theta2_goal), (l1 + l2 * np.cos(theta2_goal)))

            theta1 = theta1 + Kp * ang_diff(theta1_goal, theta1) * dt
            theta2 = theta2 + Kp * ang_diff(theta2_goal, theta2) * dt
        except ValueError as e:
            print("Unreachable goal")

        wrist = plot_arm(theta1, theta2, x, y)

        
        d2goal = np.math.sqrt((wrist[0] - x)**2 + (wrist[1] - y)**2)
        dx,dy = joyps4con.main()
        x+=dx*0.1
        y-=dy*0.1
        print(dx,dy)
        
        # check goal
        if abs(d2goal) < GOAL_TH and x is not None:
            return theta1, theta2


def plot_arm(theta1, theta2, x, y):  # pragma: no cover
    shoulder = np.array([0, 0])
    elbow = shoulder + np.array([l1 * np.cos(theta1), l1 * np.sin(theta1)])
    wrist = elbow + \
        np.array([l2 * np.cos(theta1 + theta2), l2 * np.sin(theta1 + theta2)])

    if show_animation:
        plt.cla()

        plt.plot([shoulder[0], elbow[0]], [shoulder[1], elbow[1]], 'k-')
        plt.plot([elbow[0], wrist[0]], [elbow[1], wrist[1]], 'k-')

        plt.plot(shoulder[0], shoulder[1], 'ro')
        plt.plot(elbow[0], elbow[1], 'ro')
        plt.plot(wrist[0], wrist[1], 'ro')

        plt.plot([wrist[0], x], [wrist[1], y], 'g--')
        plt.plot(x, y, 'g*')

        plt.xlim(-2, 2)
        plt.ylim(-2, 2)

        plt.show()
        plt.pause(dt)

    return wrist


def ang_diff(theta1, theta2):
    # Returns the difference between two angles in the range -pi to +pi
    return (theta1 - theta2 + np.pi) % (2 * np.pi) - np.pi


def click(event):  # pragma: no cover
    #global x, y
    #x = event.xdata
    #y = event.ydata
    print("sleep5")
    time.sleep(5)


def animation():
    from random import random
    global x, y
    theta1 = theta2 = 0.0
    for i in range(5):
        x = 2.0 * random() - 1.0
        y = 2.0 * random() - 1.0
        theta1, theta2 = two_joint_arm(
            GOAL_TH=0.01, theta1=theta1, theta2=theta2)

def main():  # pragma: no cover
    fig = plt.figure()
    fig.canvas.mpl_connect("button_press_event", click)
    two_joint_arm()


if __name__ == "__main__":
    # animation()
    main()
