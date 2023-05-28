#!/usr/bin/env python3
import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge 
import cv2 
import numpy as np 
import ctypes
from ctypes.util import find_library
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image, CameraInfo


rclpy.init()
nh = Node("coordinate_publisher_initiated")
publisher = nh.create_publisher(Image, '/camera/image_raw',10)
publisher2 = nh.create_publisher(CameraInfo,"/camera/camera_info", 10)


def main():
  
  camera_info = CameraInfo()
  camera_info.header.frame_id = "narrow-stereo"
  camera_info.width = 640
  camera_info.height = 480
  camera_info.distortion_model = 'plumb_bob'
  camera_info.d = [0.09444668457828621, -0.2691296513089623, 0.004564347646972995, 0.00955579384018999, 0.0]
  camera_info.k =  [659.6814584171026, 0.0, 341.4858478952067, 0.0, 662.480225238167, 277.50868631449265, 0.0, 0.0, 1.0]
  camera_info.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
  camera_info.p = [662.2987060546875, 0.0, 345.9606989571039, 0.0, 0.0, 668.9464721679688, 278.6528497525451, 0.0, 0.0, 0.0, 1.0, 0.0]
  
  

  cap = cv2.VideoCapture(0)
  br = CvBridge()
  while True:
    ret,frame = cap.read()
    publisher.publish(br.cv2_to_imgmsg(frame, encoding='bgr8'))
    publisher2.publish(camera_info)
    cv2.imshow("video",frame)

    if (cv2.waitKey(30) == 27):
       break
    
  cap.release()
  cv2.destroyAllWindows()
  rclpy.spin(nh)
  nh.destroy_node()
  rclpy.shutdown()

  
if __name__ == '__main__':
  main()