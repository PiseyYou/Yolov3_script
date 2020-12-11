import os, shutil
from PIL import Image
import random

def get_xmlPath(xmlPath):
    all_xmlName = next(os.walk(xmlPath))[2]
    xmlPath_list = [os.path.join(xmlPath, i) for i in all_xmlName]
    return xmlPath_list

def get_picPath(picPath):
    all_picName = next(os.walk(picPath))[2]
    picPath_list = [os.path.join(picPath, i) for i in all_picName]
    return picPath_list

def delete_file(filePath):
    if not os.path.exists(filePath):
        print('%s the file is not exist, please check' %filePath)
    else:
        print('%s these file will be delete' %filePath)
        os.remove(filePath)

def selectPic(xmlPath, picPath):
    # dic = {}
    picFilePath = get_picPath(picPath)
    picFilePath_list = [i for i in picFilePath if i.endswith('.jpg')]
    allpicMark = True
    for picFilePath in picFilePath_list:
        xmlFilePath = picFilePath[:-4] + '.xml'
        image = Image.open(picFilePath)
        width, height = image.size
        # dic[width, height] = 0
        if width >= 416 and height >= 416:
            # dic[width, height] += 1
            continue
        else:
            delete_file(os.path.join(picPath, picFilePath))
            delete_file(os.path.join(xmlPath, xmlFilePath))
            allpicMark = False
            # break
    if allpicMark:
        print('selectPic pass, all the pics are qualified!')
        print('All pic number is ' + str(len(picFilePath_list)))
        # print(dic)

def copyPicXml(sample_num, xmlPath, picPath):
    picFilePath = get_picPath(picPath)
    picFilePath_list = [i for i in picFilePath if i.endswith('.jpg')]
    rdPic = random.sample(picFilePath_list, sample_num)
    if not os.path.exists(picSavePath):
        os.makedirs(picSavePath)

    if not os.path.exists(xmlSavePath):
        os.makedirs(xmlSavePath)

    for picFilePath in rdPic:
        repicFilePath = picFilePath.split("/")[-1]
        rexmlFilePath = repicFilePath[:-4] + '.xml'
        shutil.copy(os.path.join(picPath, repicFilePath), os.path.join(picSavePath, repicFilePath))
        print(os.path.join(picSavePath, repicFilePath) + " is been written....")
        shutil.copy(os.path.join(xmlPath, rexmlFilePath), os.path.join(xmlSavePath, rexmlFilePath))
        print(os.path.join(xmlSavePath, rexmlFilePath) + " is been written....")
    print("copy pic and xml process is done!")

if __name__ == '__main__':
    sample_num = 6000
    picPath = '/home/supernode/data/coco/result/images'
    xmlPath = '/home/supernode/data/coco/result/Annotations'

    picSavePath = "/home/supernode/anaconda3/envs/helmet/trafficSystem_8type/JPEGImages"
    xmlSavePath = "/home/supernode/anaconda3/envs/helmet/trafficSystem_8type/Annotations"
    # selectPic(xmlPath, picPath)
    copyPicXml(sample_num, xmlPath, picPath)
