import os
import xml.etree.ElementTree as ET

labelPath = '/home/supernode/anaconda3/envs/py36/darknet/face_mask_ori/Annotataions'
picPath = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/imagesAndlabel'
# labelPath = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/labels'
nameList = '/home/pisey/anaconda3/envs/yolo/darknet/face_mask_ori/mask_2.name'
labelPath = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/imagesAndlabel'

def get_labelPath(labelPath):
    all_xmlName = next(os.walk(labelPath))[2]
    labelPath_list = [os.path.join(labelPath, i) for i in all_xmlName]
    return labelPath_list

def get_picPath(picPath):
    all_picName = next(os.walk(picPath))[2]
    picPath_list = [os.path.join(picPath, i) for i in all_picName]
    return picPath_list

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
def check_PicLabel(labelPath, picPath):
    # check the pic without annotation and delete
    imageFilePath_list = get_picPath(picPath)
    relimgPath_list = [os.path.basename(i) for i in imageFilePath_list]
    allpicMarked = True
    numlabel = 0
    numpic = 0
    for imageFilePath in relimgPath_list:
        labelFilePath = imageFilePath[:-4] + '.txt'
        ablabelFilePath = os.path.join(labelPath, labelFilePath)
        if not os.path.exists(ablabelFilePath):
            numpic += 1
            delete_file(os.path.join(picPath, imageFilePath))
            allpicMarked = False
    print('%d pic will be delete' %numpic)

    if allpicMarked:
        print('check Pic pass, all pics have right label!')

    # check the label without pic and delete
    labelFilePath_list = get_labelPath(labelPath)
    rellabelPath_list = [os.path.basename(i) for i in labelFilePath_list]
    all_labelMarked = True
    for labelFilePath in rellabelPath_list:
        picFilePath = labelFilePath[:-4] + '.jpg'
        abpicFilePath = os.path.join(picPath, picFilePath)
        if not os.path.exists(abpicFilePath):
            numlabel +=1
            delete_file(os.path.join(labelPath, labelFilePath))
            all_labelMarked = False
    print('%d label will be delete' % numlabel)
    if all_labelMarked:
        print('check Label pass, all label files have right pic!')

check_PicLabel(labelPath, picPath)
