import time

from move_joint_a_little import move_joint_a_little
from skillet.setup.maps import ACTUATOR_NAME_TO_ID
MOVE_DEGREES = 10.0

def crawling(self):
    for i in range(10):
        move_joint_a_little("right_shoulder_pitch", MOVE_DEGREES)
        move_joint_a_little("left_shoulder_pitch", MOVE_DEGREES)
        move_joint_a_little("right_elbow_yaw", MOVE_DEGREES)
        move_joint_a_little("left_elbow_yaw", MOVE_DEGREES)
        time.sleep(0.1)