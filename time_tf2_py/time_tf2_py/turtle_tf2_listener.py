# Copyright 2021 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

import math

from geometry_msgs.msg import Twist

import rclpy
from rclpy.node import Node

from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from tf2_ros import TransformListener, Buffer

from turtlesim.srv import Spawn


class FrameListener(Node):

    def __init__(self):
        super().__init__('turtle_tf2_frame_listener')

        self.declare_parameter('target_frame', 'turtle1')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.spawner = self.create_client(Spawn, 'spawn')
        self.turtle_spawning_service_ready = False
        self.turtle_spawned = False

        self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 1)
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        from_frame_rel = self.get_parameter('target_frame').get_parameter_value().string_value
        to_frame_rel = 'turtle2'

        if self.turtle_spawning_service_ready:
            if self.turtle_spawned:
                when = self.get_clock().now() - rclpy.time.Duration(seconds=5.0)
                try:
                    t = self.tf_buffer.lookup_transform_full(
                        target_frame=to_frame_rel,
                        target_time=rclpy.time.Time(),
                        source_frame=from_frame_rel,
                        source_time=when,
                        fixed_frame='world',
                        timeout=rclpy.duration.Duration(seconds=0.05))
                except (LookupException, ConnectivityException, ExtrapolationException):
                    self.get_logger().info('Transform not ready')
                    return

                msg = Twist()
                scale_rotation_rate = 1.0
                msg.angular.z = scale_rotation_rate * math.atan2(
                    t.transform.translation.y,
                    t.transform.translation.x)

                scale_forward_speed = 0.5
                msg.linear.x = scale_forward_speed * math.sqrt(
                    t.transform.translation.x ** 2 +
                    t.transform.translation.y ** 2)

                self.publisher.publish(msg)
            else:
                if self.result.done():
                    self.get_logger().info('Spawn finished')
                    self.turtle_spawned = True
                else:
                    self.get_logger().info('Spawn is not finished')
        else:
            if self.spawner.service_is_ready():
                request = Spawn.Request()
                request.name = 'turtle2'
                request.x = float(4)
                request.y = float(2)
                request.theta = float(0)
                self.result = self.spawner.call_async(request)
                self.turtle_spawning_service_ready = True
            else:
                self.get_logger().info('Service is not ready')


def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()
