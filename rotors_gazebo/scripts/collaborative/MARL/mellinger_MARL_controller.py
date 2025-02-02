import rospy
# from rotors_gazebo.msg import Float64ArrayStamped
import sys
sys.path.append("/home/awesomelb/Multi-UAV_RL/src/collaborative_transportation/rotors_gazebo/scripts/collaborative")
from mellinger_without_planner import Mellinger


class MellingerMARL(Mellinger):
    def __init__(self, mav_name, index, x, y, z):
        Mellinger.__init__(self, mav_name, index, x=x, y=y, z=z)
        self.index = index
        self.name = mav_name + '_' + str(index)
        # topic_name_pos_ref = self.name + '/pos_ref'
        # topic_name_vel_ref = self.name + '/vel_ref'
        # topic_name_acc_ref = self.name + '/acc_ref'
        # topic_name_jerk_ref = self.name + '/jerk_ref'
        # topic_name_snap_ref = self.name + '/snap_ref'
        # self.sub_pos = rospy.Subscriber(topic_name_pos_ref, Float64ArrayStamped, self.cb_pos_ref)
        # self.sub_vel = rospy.Subscriber(topic_name_vel_ref, Float64ArrayStamped, self.cb_vel_ref)
        # self.sub_acc = rospy.Subscriber(topic_name_acc_ref, Float64ArrayStamped, self.cb_acc_ref)
        # self.sub_jerk = rospy.Subscriber(topic_name_jerk_ref, Float64ArrayStamped, self.cb_jerk_ref)
        # self.sub_snap = rospy.Subscriber(topic_name_snap_ref, Float64ArrayStamped, self.cb_snap_ref)

    # def cb_pos_ref(self, data):
    #     self.desired_positions = data.data

    # def cb_vel_ref(self, data):
    #     self.desired_velocities = data.data

    # def cb_acc_ref(self, data):
    #     self.desired_acceleratons = data.data

    # def cb_jerk_ref(self, data):
    #     self.desired_jerk = data.data

    # def cb_snap_ref(self, data):
    #     self.desired_snap = data.data

    def set_ref_from_action(self, action):
        self.desired_positions = action[0:3, :]
        self.desired_velocities = action[3:6, :]
        self.desired_acceleratons = action[6:9, :]
        self.desired_jerk = action[9:12, :]
        self.desired_snap = action[12:15, :]



