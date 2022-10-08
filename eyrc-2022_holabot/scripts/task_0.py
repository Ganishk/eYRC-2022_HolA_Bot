#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (KB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:  hb#2938			[ Team-ID ]
# Author List:	Ganishk D, Srivattan S, Susmitha S, Janam Khandhelwal	[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_0.py
# Functions: linear, turn, arc
# 					[ Comma separated list of functions in this file ]
# Nodes: /turtlesim, /robot (anonymous)		    Add your publishing and subscribing node


####################### IMPORT MODULES #######################
import sys
import traceback

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
##############################################################


def callback(data):
        """
	Purpose:
	---
	This function should be used as a callback. Refer Example #1: Pub-Sub with Custom Message in the Learning Resources Section of the Learning Resources.
    You can write your logic here.
    NOTE: Radius value should be 1. Refer expected output in document and make sure that the turtle traces "same" path.

	Input Arguments:
	---
        `data`  : []
            data received by the call back function

	Returns:
	---
        May vary depending on your logic.

	Example call:
	---
        Depends on the usage of the function.
	"""
        global pose
        pose = data


def main():
        """
	Purpose:
	---
	This function will be called by the default main function given below.
    You can write your logic here.

	Input Arguments:
	---
        None

	Returns:
	---
        None

	Example call:
	---
        main()
	"""
        global vel_pub, vel_msg, pose, pose_subscriber, rate

        rospy.init_node('robot',anonymous=True)

        #Create a publisher to send velocity related instructions
        vel_pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
        vel_msg = Twist()

        #Create a susbscriber node to get the pose info
        pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, callback)
        pose = Pose()

        rate = rospy.Rate(10000)

######################################
        try:
            """
            Steps involved in drawing D are:
                1. Draw the semicircular arc of D
                2. Rotate the bot by 90 degrees so that it points downwards
                3. Move the bot to the initial position linearly
            """
            arc(1,PI)
            turn(1,PI*0.5)
            linear(4,2)
            #rospy.spin()

        except rospy.ROSInterruptException: pass
        except KeyboardInterrupt: pass
######################################
        rospy.signal_shutdown("")





################# ADD GLOBAL VARIABLES HERE #################

PI = 3.141592653589793
DEG2RAD = 0.017453292519943295 #Used to convert degrees into radians

##############################################################


################# ADD UTILITY FUNCTIONS HERE #################

def linear(vel,dist=None):
    """
    To control the linear movement of the turtle
    @params:
        Inputs: vel --> velocity to move the bot
                dist -->distance until which the bot should be moved
                        ignore to move for infinite length
        Output: None
    """
    print("Moving forward")
    vel_msg.linear.x    = vel
    vel_msg.linear.y    = 0
    vel_msg.linear.z    = 0
    vel_msg.angular.x   = 0
    vel_msg.angular.y   = 0
    vel_msg.angular.z   = 0

    t0 = rospy.Time.now().to_sec()
    c_dist = 0

    while c_dist < dist: #Run infinitely if dist not specified
        vel_pub.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        c_dist = vel*(t1-t0)
        rate.sleep()

    vel_msg.linear.x    = 0
    vel_pub.publish(vel_msg)


def turn(avel,angle=None):
    """
    To control the rotation of the turtle in the plane
    @params
    Input:
        avel --> Angular velocity of the turtle
        angle -->Angle until which the bot should turn
    Output:
        None
    """
    print("Turning")
    vel_msg.linear.x    = 0
    vel_msg.linear.y    = 0
    vel_msg.linear.z    = 0
    vel_msg.angular.x   = 0
    vel_msg.angular.y   = 0
    vel_msg.angular.z   = avel

    t0 = rospy.Time.now().to_sec() 
    c_angle = 0

    while c_angle < angle or not angle: #Run infinitely if angle is not specified
        vel_pub.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        c_angle = avel*(t1-t0)
        rate.sleep()

    vel_msg.angular.z   = 0
    vel_pub.publish(vel_msg)


def arc(vel, angle = None):
    """
    To draw the arc of specified angle
    @params
    Input:
        vel --> linear velocity of the bot which is same as angular velocity
                in unit circular motion.
    Output:
        None

    We made it as semi circular arc for unit radius for simplicity
    not made for any arbitary angles
    """
    print("Making an arc")
    vel_msg.linear.x    = vel
    vel_msg.linear.y    = 0
    vel_msg.linear.z    = 0
    vel_msg.angular.x   = 0
    vel_msg.angular.y   = 0
    vel_msg.angular.z   = vel 


    print(pose.theta)
    print("___________")

    t = pose.theta

    while t>=0:
        vel_pub.publish(vel_msg)
        t = pose.theta
        print(pose.x, pose.y, t)
        #rospy.spin()
        rate.sleep()

    vel_msg.linear.x    = 0
    vel_msg.angular.z   = 0
    vel_pub.publish(vel_msg)

##############################################################


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS PART #########
if __name__ == "__main__":
    try:
        print("------------------------------------------")
        print("         Python Script Started!!          ")
        print("------------------------------------------")
        main()

    except:
        print("------------------------------------------")
        traceback.print_exc(file=sys.stdout)
        print("------------------------------------------")
        sys.exit()

    finally:
        print("------------------------------------------")
        print("    Python Script Executed Successfully   ")
        print("------------------------------------------")
