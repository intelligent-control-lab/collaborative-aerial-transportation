#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty
from gazebo_msgs.msg import ODEPhysics
from gazebo_msgs.srv import SetPhysicsProperties, SetPhysicsPropertiesRequest
from std_msgs.msg import Float64
from geometry_msgs.msg import Vector3


class GazeboConnection():
    
    def __init__(self):
        
        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_world', Empty)

        # Setup the Gravity Controle system
        service_name = '/gazebo/set_physics_properties'
        print("Waiting for service " + str(service_name))
        rospy.wait_for_service(service_name)
        print("Service Found " + str(service_name))

        self.set_physics = rospy.ServiceProxy(service_name, SetPhysicsProperties)
        self.init_values()
        # We always pause the simulation, important for legged robots learning
        self.pauseSim()

    def pauseSim(self):
        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause()
        except rospy.ServiceException, e:
            print ("/gazebo/pause_physics service call failed")
        
    def unpauseSim(self):
        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause()
        except rospy.ServiceException, e:
            print ("/gazebo/unpause_physics service call failed")
        
    def resetSim(self):
        rospy.wait_for_service('/gazebo/reset_simulation')
        try:
            self.reset_proxy()
        except rospy.ServiceException, e:
            print ("/gazebo/reset_simulation service call failed")

    def resetWorld(self):
        print "reseting world"
        rospy.wait_for_service('/gazebo/reset_world')
        try:
            self.reset_proxy()
        except rospy.ServiceException, e:
            print ("/gazebo/reset_world service call failed")

    def init_values(self):

        rospy.wait_for_service('/gazebo/reset_world')
        try:
            # reset_proxy.call()
            self.reset_proxy()
        except rospy.ServiceException, e:
            print ("/gazebo/reset_world service call failed")

        self._time_step = Float64(0.01)
        self._max_update_rate = Float64(100.0)

        self._gravity = Vector3()
        self._gravity.x = 0.0
        self._gravity.y = 0.0
        self._gravity.z = -9.81

        self._ode_config = ODEPhysics()
        self._ode_config.auto_disable_bodies = False
        self._ode_config.sor_pgs_precon_iters = 0
        self._ode_config.sor_pgs_iters = 1000
        self._ode_config.sor_pgs_w = 1.3
        self._ode_config.sor_pgs_rms_error_tol = 0.0
        self._ode_config.contact_surface_layer = 0.001
        self._ode_config.contact_max_correcting_vel = 100.0
        self._ode_config.cfm = 0.0
        self._ode_config.erp = 0.2
        self._ode_config.max_contacts = 20

        self.update_gravity_call()

    def update_gravity_call(self):

        self.pauseSim()

        set_physics_request = SetPhysicsPropertiesRequest()
        set_physics_request.time_step = self._time_step.data
        set_physics_request.max_update_rate = self._max_update_rate.data
        set_physics_request.gravity = self._gravity
        set_physics_request.ode_config = self._ode_config

        print(str(set_physics_request.gravity))

        result = self.set_physics(set_physics_request)
        print("Gravity Update Result==" + str(result.success) + ",message==" + str(result.status_message))

        self.unpauseSim()
        # rospy.sleep(3.0)

        

    def change_gravity(self, x, y, z):
        self._gravity.x = x
        self._gravity.y = y
        self._gravity.z = z

        self.update_gravity_call()