import os
import xml.etree.ElementTree as ET

xmlPath = '/ext_data/trafficSystem_8type/Annotations'
picPath = '/ext_data/trafficSystem_8type/JPEGImages'
nameList = '/ext_data/trafficSystem_8type/trafficSystem.names'
txtPath = '/ext_data/trafficSystem_8type/labels'

def get_xmlPath(xmlPath):
    all_xmlName = next(os.walk(xmlPath))[2]
    xmlPath_list = [os.path.join(xmlPath, i) for i in all_xmlName]
    return xmlPath_list

def get_picPath(picPath):
    all_picName = next(os.walk(picPath))[2]
    picPath_list = [os.path.join(picPath, i) for i in all_picName]
    return picPath_list

def get_txtPath(txtPath):
    all_txtName = next(os.walk(txtPath))[2]
    txtPath_list = [os.path.join(txtPath, i) for i in all_txtName]
    return txtPath_list

def get_classNameList(classNamePath):
    with open(classNamePath, 'r', encoding='utf8') as file:
        nameContent = file.read()
        line_list = [k for k in nameContent.split('\n') if k.strip() != '']
        nameList= sorted(line_list, reverse=False)
    return nameList

def delete_file(filePath):
    if not os.path.exists(filePath):
        print('%s the file is not exist, please check' %filePath)
    else:
        print('%s these file will be delete' %filePath)
        os.remove(filePath)


# check annotation with pic
def check_1(xmlPath, picPath):
    # check the pic without annotation and delete
    imageFilePath_list = get_picPath(picPath)
    relimgPath_list = [os.path.basename(i) for i in imageFilePath_list]
    allpicMarked = True
    for imageFilePath in relimgPath_list:
        xmlFilePath = imageFilePath[:-4] + '.xml'
        abxmlFilePath = os.path.join(xmlPath, xmlFilePath)
        if not os.path.exists(abxmlFilePath):
            delete_file(os.path.join(picPath, imageFilePath))
            allpicMarked = False
    if allpicMarked:
        print('check_1 pass, all pics have right annotation!')

    # check the xml without pic and delete
    xmlFilePath_list = get_xmlPath(xmlPath)
    relxmlPath_list = [os.path.basename(i) for i in xmlFilePath_list]
    allxmlMarked = True
    for xmlFilePath in relxmlPath_list:
        picFilePath = xmlFilePath[:-4] + '.jpg'
        abpicFilePath = os.path.join(picPath, picFilePath)
        if not os.path.exists(abpicFilePath):
            delete_file(os.path.join(xmlPath, xmlFilePath))
            allxmlMarked = False
    if allxmlMarked:
        print('check 1 pass, all xml files have right pic!')

    # check the txt without pic and delete
    txtFilePath_list = get_txtPath(txtPath)
    reltxtPath_list = [os.path.basename(i) for i in txtFilePath_list]
    alltxtMarked = True
    for txtFilePath in reltxtPath_list:
        picFilePath = txtFilePath[:-4] + '.jpg'
        abpicFilePath = os.path.join(picPath, picFilePath)
        if not os.path.exists(abpicFilePath):
            delete_file(os.path.join(txtPath, txtFilePath))
            alltxtMarked = False
    if alltxtMarked:
        print('check 1 pass, all txt files have right pic!')


# check xml with all type
def check_2(xmlPath, nameList):

    className_set = set(get_classNameList(nameList))
    xmlFilePath_list = get_xmlPath(xmlPath)
    allFileCorrect = True
    for xmlFilePath in xmlFilePath_list:
        if xmlFilePath.endswith("xml"):
            with open(xmlFilePath) as file:
                fileContent = file.read()
            root = ET.XML(fileContent)
            object_list = root.findall('object')
            for object_item in object_list:
                name = object_item.find('name')
                className = name.text
                if className not in className_set:
                    print('%s the xml file has wrong type "%s" ' %(xmlFilePath, className))
                    allFileCorrect = False
    if allFileCorrect:
        print('check_2 pass, all xml files have right type!')

import  os
def delete_emFile(txtPath, annoPath, picPath):
	files = os.listdir(txtPath)
	for file in files:
		with open(os.path.join(txtPath, file), 'r') as f:
			contends =f.read()
			if contends == '':
				# os.remove(dir_path+file)
				# os.remove(os.path.join(txtPath, file))
				# # a = os.path.join(annoPath, str(file)[:-4] + '.xml')
				# os.remove(os.path.join(annoPath, str(file)[:-4] + '.xml'))
				# os.remove(os.path.join(picPath, str(file)[:-4] + '.jpg'))
				print(str(file) + " is empty, the label/anno/pic will be delete!")
			else:
				continue
	print('all empty file are been delete')

from PIL import Image
def check_3(xmlPath, picPath):
    xmlFilePath_list = get_xmlPath(xmlPath)
    allFileCorrect = True
    xmlFilePath_list = [i for i in xmlFilePath_list if i.endswith('xml')]

    for xmlFilePath in xmlFilePath_list:
        picFilePath = os.path.basename(xmlFilePath[:-4]) + '.jpg'
        abpicFilePath = os.path.join(picPath, picFilePath)
        image = Image.open(abpicFilePath)
        width, height = image.size

        with open(xmlFilePath) as file:
            fileContent = file.read()
        root = ET.XML(fileContent)
        object_list = root.findall('object')
        for object_item in object_list:
            bndbox = object_item.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            if xmin>=1 and ymin>=1 and xmax<=width and ymax<=height:
                continue
            else:
                delete_file(xmlFilePath)
                delete_file(abpicFilePath)
                allFileCorrect = False
                break

    if allFileCorrect:
        print('check_3 pass, all file have already test, all xml file boxes are not overbounary!')

def selectPic(xmlPath, picPath):
    picFilePath = get_picPath(picPath)
    picFilePath_list = [i for i in picFilePath if i.endswith('.jpg')]
    allpicMark = True
    for picFilePath in picFilePath_list:
        xmlFilePath = picFilePath[:-4] + '.xml'
        image = Image.open(picFilePath)
        width, height = image.size
        if width >= 416 and height >= 416:
            continue
        else:
            delete_file(os.path.join(picPath, picFilePath))
            delete_file(os.path.join(xmlPath, xmlFilePath))
            allpicMark = False
            break

    if allpicMark:
        print('selectPic pass, all the pics are qualified!')
        print('All pic number is ' + str(len(picFilePath_list)))


check_1(xmlPath, picPath) # check xml with the pic
check_2(xmlPath, nameList) # check xml with all names
#delete_emFile(txtPath, xmlPath, picPath) # delete empty label/anno/pic
#check_3(xmlPath, picPath) # check overbounnary
#selectPic(xmlPath, picPath) # select 416 size pic
# import argparse
# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-x', '--xmlPath', type=str, help='annotation', default='./xml.bak')
#     parser.add_argument('-p', '--picPath', type=str, help='image', default='./pic.bak')
#     parser.add_argument('-n', '--nameList', type=str, help = 'namelist', default='../person.name')
#     argument_namespace = parser.parse_args()
#     return argument_namespace
#
#
# if __name__ == '__main__':
#     argument_namespace = parse_args()
#
#     xmlPath = argument_namespace.xmlPath
#     assert os.path.exists(xmlPath), 'not exists this path: %s' % xmlPath
#
#     picPath = argument_namespace.picPath
#     assert os.path.exists(xmlPath), 'not exists this path: %s' % xmlPath
#
#     nameList = argument_namespace.nameLis
#     assert os.path.exists(nameList), 'not exists this path: %s' % nameList


