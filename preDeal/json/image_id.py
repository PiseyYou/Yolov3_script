# -*- coding: utf-8 -*-
import json
import pandas as pd
import re
 
# file_path = '/home/pisey/data/coco/'
# filename = 'new_instances_val2014.json'

file_path = '/home/pisey/data/coco/annotations/'
filename = 'instances_val2014.json'
 
# file_path 为预测结果的存储路径，filename为存放预测结果的文件名，
# 返回的是集合形式的数据
def get_image_id(file_path, filename):
    a = json.load(open(file_path + filename))
    image_id_chongfu = []
    annoDic = a['annotations']

    for i in range(len(annoDic)):
        # b = annoDic[i]['image_id']
        # image_id_chongfu.append(b)
        # print(b)
        # c = b['image_id']

        image_id_chongfu.append(annoDic[i]['image_id'])
    image_id = set(image_id_chongfu)
    return image_id
    # return b

def write_set_to_csv(data_set):
    data_list=list(data_set)
    test = pd.DataFrame(columns=['image_id'], data=data_list)
    # test = pd.DataFrame(data=data_list)
    test.to_csv('image_id_file.csv', index=False)
    print("数据已经写入到image_id_file.csv 文件")

image_ids = get_image_id(file_path, filename)
write_set_to_csv(image_ids)
