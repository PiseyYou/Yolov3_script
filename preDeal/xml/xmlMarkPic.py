# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os, cv2

# 将路径换成自己的即可
annota_dir = "/home/supernode/data/coco/result/Annotations"     #xml文件保存的路径
origin_dir = "/home/supernode/data/coco/result/images"      #jpg图片保存的路径
target_dir1= "/home/supernode/data/coco/result/checkMark"          #生成带有标签信息的文件夹路径，即想将转化后的图片保存在哪

def divide_img(oriname):
    img_file = os.path.join(origin_dir, oriname + '.jpg')
    im = cv2.imread(img_file)

    # 读取每个原图像的xml文件
    xml_file = os.path.join(annota_dir, oriname + '.xml')
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for object in root.findall('object'):
        object_name = object.find('name').text
        Xmin = int(object.find('bndbox').find('xmin').text)
        Ymin = int(object.find('bndbox').find('ymin').text)
        Xmax = int(object.find('bndbox').find('xmax').text)
        Ymax = int(object.find('bndbox').find('ymax').text)
        color = (4, 250, 7)
        cv2.rectangle(im, (Xmin, Ymin), (Xmax, Ymax), color, 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(im, object_name, (Xmin, Ymin - 7), font, 0.5, (6, 230, 230), 2)

    img_name = oriname + '.jpg'
    to_name = os.path.join(target_dir1, img_name)
    cv2.imwrite(to_name, im)
    print(to_name +" is been written....")

img_list = os.listdir(origin_dir)
for name in img_list:
    if(name.endswith(".jpg")):
        divide_img(name.rstrip('.jpg'))
print("转化完成！")