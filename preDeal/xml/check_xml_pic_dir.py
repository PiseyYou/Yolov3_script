import os,shutil
import xml.etree.ElementTree as ET

xmlPath = '/ext_data/obav_detection/Annotations'
picPath = '/ext_data/obav_detection/JPEGImages_0615'
nameList = '/ext_data/obav_detection/labelmap/labels_ft.names'
# txtPath = '/ext_data/trafficSystem_8type/labels'

def get_xmlPath(xmlPath):
    all_xmlName = next(os.walk(xmlPath))[2]
    xmlPath_list = [os.path.join(xmlPath, i) for i in all_xmlName]
    return xmlPath_list

def get_xmlPath_dir(xmlPath):
    all_xmlName = next(os.walk(xmlPath))[2]
    xmlPath_list = [os.path.join(xmlPath, i) for i in all_xmlName]
    return xmlPath_list

def get_picPath(picPath):
    all_picName = next(os.walk(picPath))[2]
    picPath_list = [os.path.join(picPath, i) for i in all_picName]
    return picPath_list

def get_picPath_dir(picPath):
    all_picName = next(os.walk(picPath))[2]
    picPath_list = [os.path.join(picPath, i) for i in all_picName]
    return picPath_list

# def get_txtPath(txtPath):
#     all_txtName = next(os.walk(txtPath))[2]
#     txtPath_list = [os.path.join(txtPath, i) for i in all_txtName]
#     return txtPath_list

def get_classNameList(classNamePath):
    with open(classNamePath, 'r', encoding='utf8') as file:

        nameContent = file.read()
        nameContent = nameContent.encode('utf-8').decode('utf-8-sig')
        line_list = [k for k in nameContent.split('\n') if k.strip() != '']
        nameList= sorted(line_list, reverse=False)
    return nameList

def delete_file(filePath):
    if not os.path.exists(filePath):
        print('%s the file is not exist, please check' %filePath)
    else:
        print('%s these file will be delete' %filePath)
        os.remove(filePath)

def delete_dir(dirPath):
    if not os.path.exists(dirPath):
        print('%s the file is not exist, please check' %dirPath)
    else:
        print('%s these file will be delete' %dirPath)
        shutil.rmtree(dirPath)


# check annotation with pic
def check_xml_pic_num(xmlPath, picPath):
    # delete the dir first
    for dirs in os.listdir(picPath):
        if not os.path.exists(os.path.join(xmlPath, dirs)):
            delete_dir(os.path.join(picPath, dirs))

    for dirs in os.listdir(xmlPath):
        if not os.path.exists(os.path.join(picPath, dirs)):
            delete_dir(os.path.join(xmlPath, dirs))

    pic_length = 0
    for root, dirs, files in os.walk(picPath, topdown=False):
        for file_name in files:

            # rename all file name to ".jpg"
            file_name_jpg = file_name[:-4] + ".jpg"
            os.rename(os.path.join(root, file_name), os.path.join(root, file_name_jpg))
            # print(os.path.join(root, file_name))

            pic_length += 1
            xmlName = file_name[:-4]+".xml"
            xmlDir = root.replace("JPEGImages_0615", "Annotations")
            # print(os.path.join(xmlDir, xmlName))
            if not os.path.exists(os.path.join(xmlDir, xmlName)):
                delete_file(os.path.join(root, file_name))

    print("check_xml_pic_num pass, all pic have total %d pics" %pic_length)

    xml_length = 0
    for root, dirs, files in os.walk(xmlPath, topdown=False):
        for file_name in files:
            xml_length += 1
            picName = file_name[:-4]+".jpg"
            picDir = root.replace("Annotations", "JPEGImages_0615")
            if not os.path.exists(os.path.join(picDir, picName)):
                delete_file(os.path.join(root, file_name))

    print("all xml have total %d xmls" %xml_length)

def check_type_num(xmlPath, nameList):
    className_set = set(get_classNameList(nameList))
    # print("clasName_set: ", className_set)
    # allclassName_set = className_set;
    classDict = dict.fromkeys(className_set, 0)
    # for name in className_set:
    #     if ("/" in name):
    #         subNameList = name.split("/")
    #         for i in subNameList:
    #             classDict.update({i: 0})
    # allclassName = set(list(classDict.keys()))
    # print("classDict: ", classDict)

    allFileCorrect = True
    for root, dirs, files in os.walk(xmlPath, topdown=False):
        if files == []:
            continue
        for file_name in files:
            # xmlFilePath_list = get_xmlPath(xmlPath)
            # allFileCorrect = True
            # for xmlFilePath in xmlFilePath_list:
            if file_name.endswith("xml"):
                # if os.path.join(root, file_name) =
                with open(os.path.join(root, file_name)) as file:
                    fileContent = file.read()
                if len(fileContent) < 10:
                    # print("fileConten: " + fileContent)
                    break
                else:
                    # print("--------------------")
                    # print("fileConten: " + fileContent)
                    root_xml = ET.XML(fileContent)
                    object_list = root_xml.findall('object')
                    for object_item in object_list:
                        name = object_item.find('name')
                        className = name.text
                        if className not in className_set:
                            # if className not in allclassName:
                            print('%s the xml file has wrong type "%s" ' % (root + "/" + file_name, className))
                            allFileCorrect = False
                        else:
                            classDict[className] += 1
    print(classDict)
    if allFileCorrect:
        print('check_type_num pass, all xml files have right type!')

    lessDict = {k: v for k, v in classDict.items() if v < 10}
    lessList = list(lessDict.keys())
    # for i in lessList:
    #     i = eval(i)
    # lessList = [i for i in lessList]
    print(str(len(lessList)) + " type num less than 10: ", lessDict)
    print("lessList is: ", lessList)

    # 找出类别少于10个的路径
    # lessType = []
    # for k, v in classDict.items():
    #     if v < 10:
    #         # print("the type " + k + " tatal num is less than 10")
    #         lessType.append(k)
    # print("total all " + str(len(lessType)) + " are less than 10... the list is ")
    # print(lessType)

    for root, dirs, files in os.walk(xmlPath, topdown=False):
        if files == []:
            break
        for file_name in files:
            # xmlFilePath_list = get_xmlPath(xmlPath)
            # allFileCorrect = True
            # for xmlFilePath in xmlFilePath_list:
            if file_name.endswith("xml"):
                with open(os.path.join(root, file_name)) as file:
                    fileContent = file.read()
                root_xml = ET.XML(fileContent)
                object_list = root_xml.findall('object')
                for object_item in object_list:
                    name = object_item.find('name')
                    if name.text in lessList:
                        print(name.text + ":" + os.path.join(root, file_name))


def update_xml_filename(xmlPath):
    xmlfileNum = 0
    for root, dirs, files in os.walk(xmlPath, topdown=False):
        for file_name in files:
            # xml_file = open(os.path.join(root, file_name), 'w')
            # xml_file = os.path.join(root, file_name)
            doc = ET.parse(os.path.join(root, file_name))
            xml_root = doc.getroot()
            xml_filename = xml_root.find('filename')  # 找到filename标签，
            if xml_filename.text.endswith(".jpg"):
                continue
            xml_filename.text = xml_filename.text.split(".")[0] + ".jpg"  # 修改标签内容
            doc.write(os.path.join(root, file_name))  # 保存修改
            xmlfileNum += 1
            print(os.path.join(root, file_name) + " had been name changed...")
    print("total all %d xml files have been changed..." %xmlfileNum)


def updata_xml_typename(xmlPath):
    className_set = set(get_classNameList(nameList))
    for root, dirs, files in os.walk(xmlPath, topdown=False):
        if files == []:
            continue
        for file_name in files:
            if file_name.endswith(".xml"):
                # print("file_name: " + file_name)
                # print(os.path.join(root, file_name) + "\n")
                doc = ET.parse(os.path.join(root, file_name))
                # doc = ET.parse(os.path.join("/ext_data/obav_detection/Annotations/huang_ting_hong/", "IMG_20190728_233238.xml"))
                xml_root = doc.getroot()
                object_list = xml_root.findall('object')
                xmlfileTypeNum = 0
                for object_item in object_list:
                    name = object_item.find('name')
                    className = name.text
                    if className in className_set:
                        continue
                    elif className == 'chair':
                        name.text = 'furniture'
                    elif className == ' textile':
                        name.text = 'textile'
                    elif className == 'broom/mop':
                        name.text = 'cleaner'
                    elif className == 'hair accessory':
                        name.text = 'other'
                    elif className == ' box':
                        name.text = 'box'
                    elif className == 'paper roll':
                        name.text = 'other'
                    elif className == 'hair accessory':
                        name.text = 'small object'
                    elif className == 'key/pendant/small object':
                        name.text = 'small object'
                    elif className in ['plastic_bag', 'plastic bag/packing bag']:
                        name.text = 'packing bag'
                    elif className in ['alarm clock', 'alarm clock/clock']:
                        name.text = 'clock'
                    doc.write(os.path.join(root, file_name))  # 保存修改
                    xmlfileTypeNum += 1
                # print(os.path.join(root, file_name) + " had been name changed...")

            # doc.write(os.path.join("/ext_data/obav_detection/Annotations/huang_ting_hong", "IMG_20190728_233238.xml"))  # 保存修改
    print("total all %d xml files have been changed..." % xmlfileTypeNum)


def check_type(xmlPath):
    nameSet = set()
    # allFileCorrect = True
    for root, dirs, files in os.walk(xmlPath, topdown=False):
        if files == []:
            continue
        for file_name in files:
            # xmlFilePath_list = get_xmlPath(xmlPath)
            # allFileCorrect = True
            # for xmlFilePath in xmlFilePath_list:
            if file_name.endswith("xml"):
                doc = ET.parse(os.path.join(root, file_name))
                with open(os.path.join(root, file_name)) as file:
                    fileContent = file.read()
                root_xml = ET.XML(fileContent)
                object_list = root_xml.findall('object')
                for object_item in object_list:
                    name = object_item.find('name')
                    className = name.text
                    nameSet.add(className)
                    # if className not in className_set:
                    #     # if className not in allclassName:
                    #     print('%s the xml file has wrong type "%s" ' % (file_name, className))
                    #     allFileCorrect = False
                    # else:
                    #     classDict[className] += 1
    # print(classDict)
    # if allFileCorrect:
    print("nameSet长度为: " + str(len(nameSet)), nameSet)


def check_trainval_test_type(path):
    # trainval_val_path = "/ext_data/obav_detection/lmdb"
    data_path = "/ext_data/obav_detection/"
    nameSet = set()
    for i in ["trainval", "test"]:
        trainval_path = os.path.join(trainval_val_path, i+".txt")
        with open(trainval_path, 'r', encoding='utf8') as file:
            nameContent = file.read()
        nameContent = nameContent.encode('utf-8').decode('utf-8-sig')
        line_list = [k for k in nameContent.split("\n") if k.strip() != '']
        nameList= sorted(line_list, reverse=False)
        for j in nameList:
            # if j.endswith(".xml"):
            xml_file = j.split(" ")[1]
            abs_xml_path = os.path.join(data_path, xml_file)
            # print(abs_xml_path)
            if abs_xml_path.endswith(".xml"):
                doc = ET.parse(os.path.join(data_path, xml_file))
                xml_root = doc.getroot()
                object_list = xml_root.findall('object')
                xmlfileTypeNum = 0
                # with open(os.path.join(data_path, xml_file)) as file:
                #     fileContent = file.read()
                # root_xml = ET.XML(fileContent)
                # object_list = root_xml.findall('object')
                for object_item in object_list:
                    name = object_item.find('name')
                    className = name.text
                    nameSet.add(className)
                    if className == 'chair':
                        name.text = 'furniture'
                    elif className == ' textile':
                        name.text = 'textile'
                    elif className == 'broom/mop':
                        name.text = 'cleaner'
                    elif className == 'hair accessory':
                        name.text = 'other'
                    elif className == ' box':
                        name.text = 'box'
                    elif className == 'paper roll':
                        name.text = 'other'
                    # elif className == 'hairbrush':
                    #     name.text = ""
                    #     print(abs_xml_path)
                    elif className == 'hair accessory':
                        name.text = 'small object'
                    elif className == 'key/pendant/small object':
                        name.text = 'small object'
                    elif className in ['plastic_bag', 'plastic bag/packing bag']:
                        name.text = 'packing bag'
                        # print(abs_xml_path)
                    elif className in ['alarm clock', 'alarm clock/clock']:
                        name.text = 'clock'

                    # print()
                    # doc.write(os.path.join(data_path, xml_file))  # 保存修改
                    xmlfileTypeNum += 1
            else:
                break
    # print(nameSet)
    print(str(xmlfileTypeNum) + " have been changed...")
    # return nameList


if __name__ == '__main__':
    # check_xml_pic_num(xmlPath,picPath)
    check_type_num(xmlPath, nameList)
    # update_xml_filename(xmlPath)
    # updata_xml_typename(xmlPath)
    # check_type(xmlPath)

    trainval_val_path = "/ext_data/obav_detection/lmdb"
    # check_trainval_test_type(trainval_val_path)