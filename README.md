# Yolo-v5-2.0 for RDK x3
使用本仓库训练的模型可以用于地平线RDK x3的AI工具链使用，进行模型量化和RDK x3板端部署。    
## 使用说明
本仓库的代码可直接上传至Colab使用     
### 数据集标注
#### 使用ROS2标注
进入`./annotation/usb_ros2`文件夹进行编译，然后运行    
```zsh
ros2 run image_annotation annotation
```
即可接收图像并标注。   
#### 使用本地摄像头标注
将相机插在本地电脑上，运行`./annotation/usb_local_camera`文件夹中的`annotation.py`，即可进行标注。    
#### 标注方法
弹出画面后，画面是实时的，鼠标点击画面，当前帧锁定。鼠标点击、释放，画出一个矩形，并按下`1`,`2`等键进行类别选择，当前帧所有目标物标注完后，按下回车，即可保存`image`和`label`到指定文件夹。按`q`退出标注。
```
注意：一次框选一个物体并按一次类别按键。如果对此次标注不满意，按下其他键即可取消当前标注。
```
### 模型训练
#### 导入数据
将先前标注的数据中的`image`放在仓库`.data/images`中，`label`放在仓库`.data/labels`中，先运行`makeTxt_for_txt.py`程序，再运行`voc_label_for_txt.py`程序，然后直接运行`train.py`即可。
```zsh
部分路径需要自己设置
```

**参考链接**   
[YOLOv5训练自己的txt标签数据集](https://blog.csdn.net/weixin_52950958/article/details/125676839)