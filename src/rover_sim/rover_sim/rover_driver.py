import rclpy
from geometry_msgs.msg import Twist, Quaternion
import math
from nav_msgs.msg import Odometry
import tf_transformations
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

HALF_DISTANCE_BETWEEN_WHEELS = 0.045
WHEEL_RADIUS = 0.025
class RoverDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.__left_motor = self.__robot.getDevice('left wheel motor')
        self.__right_motor = self.__robot.getDevice('right wheel motor')

        self.__left_sensor = self.__robot.getDevice('left wheel sensor')
        self.__right_sensor = self.__robot.getDevice('right wheel sensor')

        self.__left_sensor.enable(32)
        self.__right_sensor.enable(32)

        self.__left_motor.setPosition(float('inf'))
        self.__left_motor.setVelocity(0)

        self.__right_motor.setPosition(float('inf'))
        self.__right_motor.setVelocity(0)

        self.__target_twist = Twist()

        rclpy.init(args=None)
        self.__node = rclpy.create_node('rover_driver')
        self.tf_broadcaster = TransformBroadcaster(self.__node)
        self.__node.create_subscription(Twist, 'cmd_vel', self._cmd_vel_callback,1)
        self.__odom_pub = self.__node.create_publisher(Odometry, '/odom', 10)

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.last_left = 0.0
        self.last_right = 0.0
    
    def _cmd_vel_callback(self, twist):
        self.__target_twist = twist
    
    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)

        forward_speed = self.__target_twist.linear.x
        angular_speed = self.__target_twist.angular.z

        command_motor_left = (forward_speed - angular_speed * HALF_DISTANCE_BETWEEN_WHEELS)/ WHEEL_RADIUS
        command_motor_right = (forward_speed + angular_speed * HALF_DISTANCE_BETWEEN_WHEELS) / WHEEL_RADIUS

        self.__left_motor.setVelocity(command_motor_left)
        self.__right_motor.setVelocity(command_motor_right)

        left_pos = self.__left_sensor.getValue()
        right_pos = self.__right_sensor.getValue()
        dt = self.__robot.getBasicTimeStep() / 1000.0
        
        dl = (left_pos - self.last_left) * WHEEL_RADIUS
        dr = (right_pos - self.last_right) * WHEEL_RADIUS

        self.last_left = left_pos
        self.last_right = right_pos

        dc = (dr + dl) / 2.0
        dtheta = (dr - dl) / (2 * HALF_DISTANCE_BETWEEN_WHEELS)

        self.x += dc * math.cos(self.theta + dtheta / 2.0)
        self.y += dc * math.sin(self.theta + dtheta / 2.0)
        self.theta += dtheta
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

        #Publish Odom
        odom = Odometry()

        odom.header.stamp = self.__node.get_clock().now().to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        q = tf_transformations.quaternion_from_euler(0, 0, self.theta)

        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]

        # --- FIXED twist ---
        odom.twist.twist.linear.x = dc / dt
        odom.twist.twist.angular.z = dtheta / dt

        # --- REQUIRED FOR SLAM ---
        odom.pose.covariance = [
        0.05, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.05, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 99999.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 99999.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 99999.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.1
    ]

        odom.twist.covariance = list(odom.pose.covariance)

        self.__odom_pub.publish(odom)

        #Tranform
        t = TransformStamped()
        t.header.stamp = odom.header.stamp
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"

        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0

        t.transform.rotation = odom.pose.pose.orientation

        self.tf_broadcaster.sendTransform(t)