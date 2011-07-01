from ros_android import *
import time

# load needed ROS packages
import roslib
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16
from sensor_msgs.msg import Image


# callback for /mobile/say
def cb_say(data):
	rospy.loginfo("I should say: %s", data.data)
	droid.makeToast(data.data)
	droid.ttsSpeak(data.data)

# callback for /mobile/vibrate
def cb_vibrate(data):
	droid.vibrate(data.data)
	
def main():
	print "main()"

	pub = rospy.Publisher('/mobile/acceleration', String)

	rospy.init_node('android')
	rospy.Subscriber('/mobile/say', String, cb_say)
	rospy.Subscriber('/mobile/vibrate', Int16, cb_vibrate)


	droid.startSensing()

	while not rospy.is_shutdown():
		# read the accelerometer and store result
		acc = droid.sensorsReadOrientation().result
		# if new sensor values have arrived, output them
		if isinstance(acc[0], float):
			acc_str = str(acc[0])
		else:
			acc_str = "No values."
		rospy.loginfo(acc_str)
		pub.publish(String(acc_str))
		rospy.sleep(0.5)

# start-up main
main()
