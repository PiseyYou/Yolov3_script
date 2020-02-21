import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from PIL import Image


filePath = '/home/pisey/anaconda3/envs/yolo/darknet/face_mask_ori'
fileName =['trainval', 'test']

classes = ["face", "face_mask"]

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def convert_annotation(image_id):
    in_file = open(os.path.join(filePath, 'Annotations/%s.xml' %(image_id)))
    out_file = open(os.path.join(filePath, 'labels/%s.txt' %(image_id)), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()

    im = Image.open(os.path.join(filePath, 'images/%s.jpg' %(image_id)))
    w = int(im.size[0])
    h = int(im.size[1])

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()


for i in fileName:
    image_ids = open(os.path.join(filePath, 'ImageSets/Main/%s.txt' % (i))).read().strip().split()
    list_file = open(os.path.join(filePath, 'Abs_%s.txt' % (i)), 'w')
    for image_id in image_ids:
        list_file.write(os.path.join(filePath, 'images/%s.jpg\n' % (image_id)))
        convert_annotation(image_id)
    list_file.close()


#os.system("cat ../origin_trainval.txt > absTrain.txt")
#os.system("cat ../origin_test.txt > absTest.txt")

