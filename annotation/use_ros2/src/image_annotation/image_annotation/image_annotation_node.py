import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import glob
import os

class ImageAnnotationNode(Node):
    def __init__(self):
        super().__init__('image_annotation_node')
        self.cv_bridge = CvBridge()
        self.image_subscriber = self.create_subscription(
            Image,
            'image_out',
            self.image_callback,
            10
        )
        self.current_frame = None
        self.annotation_data = []
        self.enable_annotation = False
        self.locked_frame = None

        self.save_data = SaveDate()
        # 标注是否开始
        self.annotation_flag = 1

    def image_callback(self, msg):
        if self.annotation_flag == 1:
            self.current_frame = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            self.locked_frame = cv2.copyTo(self.current_frame, None)
            self.h = self.current_frame.shape[0]
            self.w = self.current_frame.shape[1]
        else:
            pass
        cv2.imshow('Image', self.current_frame)
        
        cv2.setMouseCallback('Image', self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # 正在标注图像，不再刷新
            self.annotation_flag = 0
            # 鼠标按下，记录起始点
            self.start_point = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            # 鼠标释放，记录结束点，并绘制矩形框
            self.end_point = (x, y)
            self.current_frame = cv2.rectangle(self.current_frame, self.start_point, self.end_point, (0, 255, 0), 2)
            cv2.imshow('Image', self.current_frame)

            # 获取标注的类别
            label = self.get_current_label()
            if label == 'erro':
                print("erro class!")
            else:
                center_point_x = ((self.start_point[0] + self.end_point[0]) / 2) / self.w
                center_point_y = ((self.start_point[1] + self.end_point[1]) / 2) / self.h
                bbox_w = (abs(self.start_point[0] - self.end_point[0])) / self.w
                bbox_h = (abs(self.start_point[1] - self.end_point[1])) / self.h
                annotation = [label, center_point_x, center_point_y, bbox_w, bbox_h]
                print(annotation)
                self.annotation_data.append(annotation)

    def get_current_label(self):
        key = cv2.waitKey(0)
        if key == ord('1'):
            return '1'
        elif key == ord('2'):
            return '2'
        elif key == ord('3'):
            return '3'
        elif key == ord('4'):
            return '4'
        else:
            return 'erro'

    def run(self):
        while rclpy.ok():
            # self.annotation_data = []
            rclpy.spin_once(self)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == 13:
                self.save_annotation_data()
                self.annotation_flag = 1
                print(f"No.{self.save_data.get_index()} data has been saved!")
                self.annotation_data = []
                cv2.imshow('Image', self.current_frame)

    def save_annotation_data(self):
        self.save_data.save_data(self.locked_frame, self.annotation_data)

class SaveDate():

    def __init__(self) -> None:
        self.path_image = "/home/harding/yolo/dataset/images"
        self.path_label = "/home/harding/yolo/dataset/labels"
        self.index = len(glob.glob(os.path.join(self.path_image, '*.jpg')))
        assert len(glob.glob(os.path.join(self.path_image, '*.jpg'))) == len(glob.glob(os.path.join(self.path_label, '*.txt')))

    def save_data(self, image, label):
        self.index = self.index + 1
        image_name = self.path_image + "/" + str(self.index).zfill(4) + ".jpg"
        txt_name = self.path_label + "/" + str(self.index).zfill(4) + ".txt"
        cv2.imwrite(image_name, image)
        open_txt = open(txt_name, "w", encoding="utf-8")
        for item in label:
            class_id = item[0]
            x = item[1]
            y = item[2]
            w = item[3]
            h = item[4]
            line = f"{class_id} {x} {y} {w} {h}\n"
            open_txt.write(line)
        open_txt.close()

    def get_index(self):
        return self.index


def main(args=None):
    rclpy.init(args=args)
    node = ImageAnnotationNode()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()