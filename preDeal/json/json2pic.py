from pycocotools.coco import COCO
import cv2
import pandas as pd
import json


# file_path = '/home/pisey/data/coco/'
# filename = 'new_instances_train2014.json'



# # file_path 为预测结果的存储路径，filename为存放预测结果的文件名，
# # 返回的是集合形式的数据
# def get_image_id(file_path, filename):
#     a = json.load(open(file_path + filename))
#     image_id_chongfu = []
#     annoDic = a['annotations']
#
#     for i in range(len(annoDic)):
#         image_id_chongfu.append(annoDic[i]['image_id'])
#     image_id = set(image_id_chongfu)
#     return image_id

def get_image_ids(file):
    a = json.load(open(file))
    image_id_chongfu = []
    annoDic = a['annotations']

    for i in range(len(annoDic)):
        image_id_chongfu.append(annoDic[i]['image_id'])
    image_id = set(image_id_chongfu)
    return image_id


def write_set_to_csv(data_set):
    data_list = list(data_set)
    test = pd.DataFrame(columns=['image_id'], data=data_list)
    # test = pd.DataFrame(data=data_list)
    test.to_csv('../image_id_file.csv', index=False)
    print("All image_id have been written into image_id_file.csv")
 
 
def showNimages(imageidFile, annFile, imageFile, resultFile):
    """
    :param imageidFile: 要查看的图片imageid，存储一列在csv文件里 （目前设计的imageid需要为6位数，如果少于6位数，可以在前面加多个0）
    :param annFile:使用的标注文件
    :param imageFile:要读取的image所在文件夹
    :param resultFile:画了标注之后的image存储文件夹
    :return:
    """
    data = pd.read_csv(imageidFile)
    list = data.values.tolist()
    image_id = []  # 存储的是要提取图片id
    for i in range(len(list)):
        image_id.append(list[i][0])
    print(image_id)
    print(len(image_id))
    coco = COCO(annFile)

    image_idfill = []
    for j in range(len(image_id)):
        namefill = str(image_id[j]).zfill(6)
        image_idfill.append(namefill)


    for i in range(len(image_idfill)):
        # image = cv2.imread(imageFile + 'COCO_train2014_000000' +str(image_id[i]) + '.jpg') %image_id[i]
        image = cv2.imread(imageFile + 'COCO_train2014_000000' + str(image_idfill[i]) + '.jpg')
        annIds = coco.getAnnIds(imgIds=image_id[i], iscrowd=None)
        anns = coco.loadAnns(annIds)
        for n in range(len(anns)):
            x, y, w, h = anns[n]['bbox']
            x, y, w, h = int(x), int(y), int(w), int(h)
            # print(x, y, w, h)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imwrite(resultFile + str(image_idfill[i]) + 'result.png', image)
    print("All pics are resotre in the {}".format(resultFile))

if __name__ == "__main__":
    # file_path = '/home/pisey/data/coco/annotations/'
    # filename = 'instances_train2014.json'

    imageidFile = '/home/pisey/data/coco/image_id_file.csv'
    annFile = '/home/pisey/data/coco/annotations/instances_train2014.json'
    imageFile = '/home/pisey/data/coco/train2014/'
    resultFile = '/home/pisey/data/coco/result_train2014/'

    # get_image_ids(annFile)
    write_set_to_csv(get_image_ids(annFile))
    # showNimages(imageidFile, annFile, imageFile, resultFile)
