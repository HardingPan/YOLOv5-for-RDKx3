import os
import random
 
 
trainval_percent = 0.99
train_percent = 0.99
xmlfilepath = '/content/drive/MyDrive/yolov5-2.0/data/labels'
txtsavepath = '/content/drive/MyDrive/yolov5-2.0/data/images'
total_xml = os.listdir(xmlfilepath)
 
num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)
 
ftrainval = open('/content/drive/MyDrive/yolov5-2.0/data/ImageSets/trainval.txt', 'w')
ftest = open('/content/drive/MyDrive/yolov5-2.0/data/ImageSets/test.txt', 'w')
ftrain = open('/content/drive/MyDrive/yolov5-2.0/data/ImageSets/train.txt', 'w')
fval = open('/content/drive/MyDrive/yolov5-2.0/data/ImageSets/val.txt', 'w')
 
for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)
 
ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
 