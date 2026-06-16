import math
import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion

class OdometryPublisher(Node):
    def __init__(self):
        super().__init__('odometry_publisher')

        self.publisher = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.publish_odom
        )

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

    def publish_odom(self):
        self.x += 0.01

        msg = Odometry()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "odom"

        msg.child_frame_id = "base_link"

        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.position.z = 0.0

        msg.pose.pose.orientation = Quaternion(
            x=0.0,
            y=0.0,
            z=0.0,
            w=1.0
        )

        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = OdometryPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()