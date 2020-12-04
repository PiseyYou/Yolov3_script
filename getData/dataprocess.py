import os
import cv2

def fixEdge_H(p_val, img_h):
    if p_val <= 0:
        p_val = 1
    if p_val >= img_h:
        p_val = img_h - 1
    return p_val


def fixEdge_W(p_val, img_w):
    if p_val <= 0:
        p_val = 1
    if p_val >= img_w:
        p_val = img_w - 1
    return p_val

def save_xml(image, filename, bbox, cls, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    width = image.shape[1]
    height = image.shape[0]

    Obj_num = len(bbox)

    xml_file = open((save_dir + '/' + filename[:-4] + '.xml'), 'w')

    xml_file.write('<annotation>\n')

    xml_file.write('    <filename>' + filename + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')

    img_copy = image.copy()

    # for i in range(len(box)):
    #     p1 = (box[i][0], box[i][1])
    #     p2 = (box[i][2], box[i][3])
    #     cv2.rectangle(origimg, p1, p2, (255, 0, 0), 2)
    #     p3 = (max(p1[0], 15), max(p1[1], 15))
    #     title = "%s:%.2f" % (CLASSES[int(cls[i])], conf[i])
    #     cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (255, 0, 0), 2)

    for i in range(Obj_num):

        w = bbox[i][2] - bbox[i][0]
        h = bbox[i][3] - bbox[i][1]
        if w <= 0 or h <= 0:
            continue
        xmin = fixEdge_W(int(bbox[i][0]), width)
        ymin = fixEdge_H(int(bbox[i][1]), height)
        xmax = fixEdge_W(int(bbox[i][2]), width)
        ymax = fixEdge_H(int(bbox[i][3]), height)

        # 查看检测后的图片
        cv2.rectangle(img_copy, (xmin, ymin), (xmax, ymax), (255, 0, 0), 1, 1)
        p3 = (max(xmin, 15), max(ymin, 15))
        title = "%s" %CLASSES[int(cls[i])]
        cv2.putText(img_copy, title, p3, cv2.FONT_ITALIC, 0.6, (255, 0, 0), 2)

        cv2.imshow('img', img_copy)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        name = CLASSES[int(cls[i])]
        xml_file.write('    <object>\n')
        xml_file.write('        <name>' + name + '</name>\n')
        xml_file.write('        <difficult>' + str(0) + '</difficult>\n')
        xml_file.write('        <bndbox>\n')
        xml_file.write('            <xmin>' + str(xmin) + '</xmin>\n')
        xml_file.write('            <ymin>' + str(ymin) + '</ymin>\n')
        xml_file.write('            <xmax>' + str(xmax) + '</xmax>\n')
        xml_file.write('            <ymax>' + str(ymax) + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')

    xml_file.write('</annotation>\n')
    xml_file.close()

def make_lmdblist(root_dir, savetxt_dir, percent):
    f_trainval = open(os.path.join(savetxt_dir, 'trainval.txt'), 'w')
    f_test = open(os.path.join(savetxt_dir, 'test.txt'), 'w')
    imgroot_dir = "JPEGImages_0615"
    xmlroot_dir = "Annotations"
    img_path = os.path.join(root_dir, imgroot_dir)

    img_length = 0
    name_list = []
    for root, dirs, files in os.walk(img_path, topdown=False):
        for file_name in files:
            relimg_path = root[root.rfind(imgroot_dir):]
            relxml_path = relimg_path.replace(imgroot_dir, xmlroot_dir)
            img_length += 1
            xmlName = file_name[:-4]+".xml"

            # 判断是否包含中文字符
            if u'\u4e00' <= file_name <= u'\u9fff':
                # print(file_name)
                continue
            else:
                img_xml_path = relimg_path + '/' + file_name + ' ' + relxml_path + '/' + xmlName + '\n'
                print(img_xml_path)
                # f_text.write(imgroot_dir + '/' + type_name + '/' + img_name)
                # f_text.write(' ')
                # f_text.write(xmlroot_dir + '/' + type_name + '/' + img_name[:-3] + 'xml\n')
                name_list.append(img_xml_path)
    import random
    random.shuffle(name_list)

    for idx, line in enumerate(name_list):
        if idx < percent * len(name_list):
            f_trainval.write(line)
        else:
            f_test.write(line)
    print(str(int(percent*len(name_list))) + " trainval and " + str(int((1-percent)*len(name_list))) + " test files have been written...")

if __name__ == '__main__':
    root_dir = "/ext_data/obav_detection/"
    savetxt_dir = "/ext_data/obav_detection/"
    make_lmdblist(root_dir, savetxt_dir, 0.9)

