
#!usr/bin/env python
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
#
"""
Classes to handle Carla imu sensor
"""

import logging
import math
import pyproj
import numpy as np

from transforms3d.euler import euler2quat

import carla_common.transforms as trans

from .sensor import Sensor
from cyber_py import cyber, cyber_time
from modules.drivers.gnss.proto.imu_pb import Imu
from modules.localization.proto.imu_pb import CorrectedImu


class ImuSensor(Sensor):

    """
    Actor implementation details for imu sensor
    """

    def __init__(self, uid, name, parent, relative_spawn_pose, node, carla_actor, synchronous_mode):
        """
        Constructor
        :param uid: unique identifier for this object
        :type uid: int
        :param name: name identiying this object
        :type name: string
        :param parent: the parent of this
        :type parent: carla_ros_bridge.Parent
        :param relative_spawn_pose: the relative spawn pose of this
        :type relative_spawn_pose: geometry_msgs.Pose
        :param node: node-handle
        :type node: CompatibleNode
        :param carla_actor : carla actor object
        :type carla_actor: carla.Actor
        :param synchronous_mode: use in synchronous mode?
        :type synchronous_mode: bool
        """
        super(ImuSensor, self).__init__(uid=uid,
                                        name=name,
                                        parent=parent,
                                        relative_spawn_pose=relative_spawn_pose,
                                        node=node,
                                        carla_actor=carla_actor,
                                        synchronous_mode=synchronous_mode)

        if self.__class__.__name__ == "Camera":
            logging.warning("Created Unsupported Imu Actor"
                          "(id={}, parent_id={}, type={}, attributes={})".format(
                              self.get_id(), self.get_parent_id(),
                              self.carla_actor.type_id, self.carla_actor.attributes))


    def destroy(self):
        logging.debug("Destroy ImuSensor(id={})".format(self.get_id()))
        if self.carla_actor.is_listening:
            self.carla_actor.stop()
        if self.update_lock.acquire():
            self.current_sensor_data = None
        
        super(ImuSensor, self).destroy()
        
        
        

    # pylint: disable=arguments-differ
    def sensor_data_updated(self, carla_imu_measurement):
        """
        Function to transform a received imu measurement into a ROS Imu message
        :param carla_imu_measurement: carla imu measurement object
        :type carla_imu_measurement: carla.IMUMeasurement
        """
        imu_msg = Imu()
        imu_msg.header.CopyFrom(self.parent.get_cyber_header())
        imu_msg.measurement_time = imu_msg.header.timestamp_sec
        imu_msg.measurement_span = 0.0
        # Carla uses a left-handed coordinate convention (X forward, Y right, Z up).
        # Here, these measurements are converted to the right-handed ROS convention
        #  (X forward, Y left, Z up).
        imu_msg.angular_velocity.x = -carla_imu_measurement.gyroscope.x
        imu_msg.angular_velocity.y = carla_imu_measurement.gyroscope.y
        imu_msg.angular_velocity.z = -carla_imu_measurement.gyroscope.z

        imu_msg.linear_acceleration.x = carla_imu_measurement.accelerometer.x
        imu_msg.linear_acceleration.y = -carla_imu_measurement.accelerometer.y
        imu_msg.linear_acceleration.z = carla_imu_measurement.accelerometer.z

        # roll, pitch, yaw = trans.carla_rotation_to_RPY(carla_imu_measurement.transform.rotation)
        # quat = euler2quat(roll, pitch, yaw)
        # imu_msg.orientation.w = quat[0]
        # imu_msg.orientation.x = quat[1]
        # imu_msg.orientation.y = quat[2]
        # imu_msg.orientation.z = quat[3]

        self.write_cyber_message('/apollo/sensor/gnss/imu' , imu_msg)

        corrected_imu_msg = CorrectedImu()
        corrected_imu_msg.header.CopyFrom(self.parent.get_cyber_header())
        corrected_imu_msg.angular_velocity.x = -carla_imu_measurement.gyroscope.x
        corrected_imu_msg.angular_velocity.y = carla_imu_measurement.gyroscope.y
        corrected_imu_msg.angular_velocity.z = -carla_imu_measurement.gyroscope.z

        corrected_imu_msg.linear_acceleration.x = carla_imu_measurement.accelerometer.x
        corrected_imu_msg.linear_acceleration.y = -carla_imu_measurement.accelerometer.y
        corrected_imu_msg.linear_acceleration.z = carla_imu_measurement.accelerometer.z

        roll, pitch, yaw = trans.carla_rotation_to_RPY(carla_imu_measurement.transform.rotation)
        corrected_imu_msg.euler_angles.x = roll
        corrected_imu_msg.euler_angles.y = pitch
        corrected_imu_msg.euler_angles.z = yaw
        self.write_cyber_message('/apollo/sensor/gnss/corrected_imu' , corrected_imu_msg)
