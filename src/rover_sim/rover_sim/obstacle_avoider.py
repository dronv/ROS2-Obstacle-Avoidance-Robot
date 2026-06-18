import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

SAFE_DISTANCE = 0.30
ESCAPE_DISTANCE = 0.15

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')

        self.pub = self.create_publisher(Twist, 'cmd_vel', 1)

        self.left = None
        self.right = None

        self.last_turn = 1  # 1 = left, -1 = right

        self.create_subscription(Range, 'left_sensor', self.left_cb, 1)
        self.create_subscription(Range, 'right_sensor', self.right_cb, 1)

    def left_cb(self, msg):
        self.left = msg.range
        self.control()

    def right_cb(self, msg):
        self.right = msg.range
        self.control()

    def control(self):
        if self.left is None or self.right is None:
            return

        cmd = Twist()

        min_dist = min(self.left, self.right)

        # 🚨 ESCAPE MODE (very close corner)
        if min_dist < ESCAPE_DISTANCE:
            cmd.linear.x = -0.1   # reverse
            cmd.angular.z = 1.0 * self.last_turn
            self.pub.publish(cmd)
            return

        # ⚠️ OBSTACLE AVOIDANCE
        if min_dist < SAFE_DISTANCE:
            cmd.linear.x = 0.0

            if self.left < self.right:
                self.last_turn = -1
                cmd.angular.z = -0.8
            else:
                self.last_turn = 1
                cmd.angular.z = 0.8

        else:
            # forward motion
            cmd.linear.x = 0.2
            cmd.angular.z = 0.0

        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()