import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from tqdm import tqdm

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x,y,w,h)

def convert_annotation(in_path,filename,out_path, classes):
    in_file = open(in_path+'/%s.xml' %(filename), encoding='UTF-8')
    out_file = open(out_path+'/%s.txt' %(filename), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def get_classNameList(classNamePath):
    with open(classNamePath, 'r', encoding='utf8') as file:

        nameContent = file.read()
        nameContent = nameContent.encode('utf-8').decode('utf-8-sig')
        line_list = [k for k in nameContent.split('\n') if k.strip() != '']
        nameList= sorted(line_list, reverse=False)
    return nameList


def changeRemainXml(xmlPath, txtPath):
    className_set = set(get_classNameList(nameList))
    classes = list(className_set)
    xmlFilesList = os.listdir(xmlPath)
    txtPathList = os.listdir(txtPath)
    txtHavexmlPath = [i[:-4] + ".xml" for i in txtPathList]
    remainPath = list(set(xmlFilesList) - set(txtHavexmlPath))

    print("total have %d num diff file." %len(remainPath))
    print("the diff pic are ", remainPath)

    xmlfileTypeNum = 0

    # change xml name
    for file_name in remainPath:
        # absFilePath = os.path.join(xmlPath, i)
        if file_name.endswith(".xml"):
            doc = ET.parse(os.path.join(xmlPath, file_name))
            xml_root = doc.getroot()
            object_list = xml_root.findall('object')
            xmlfileTypeNum = 0
            for object_item in object_list:
                name = object_item.find('name')
                className = name.text
                if className in className_set:
                    continue
                elif className == 'person':
                    name.text = 'pedestrains'
                doc.write(os.path.join(xmlPath, file_name))  # 保存修改
                xmlfileTypeNum += 1
            # print(os.path.join(xmlPath, file_name) + " had been name changed...")

    print("total all %d xml files have been changed..." % xmlfileTypeNum)

    for file_name in tqdm(remainPath):
        fileName = file_name.split(".")[0]
        convert_annotation(xmlPath, fileName, txtPath, classes)


if __name__ == '__main__':
    nameList = "/home/supernode/anaconda3/envs/helmet/trafficSystem_8type/trafficSystem.names"
    xmlPath = "/home/supernode/anaconda3/envs/helmet/trafficSystem_8type/Annotations"
    txtPath = "/home/supernode/anaconda3/envs/helmet/trafficSystem_8type/labels"
    changeRemainXml(xmlPath, txtPath)
