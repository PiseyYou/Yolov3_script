import os
from tqdm import tqdm
import shutil

# file_dir = '/home/ai/data/VideoCapture/rename/image_data/person_no/central_k30_11-07-30_12-27-30_0/'


dir = '/home/ai/data/VideoCapture/label_data/label_truck_car_bus_van_person/person_no/missing/K52+350_C2R0P131_07-15-00_10-00-59_0/'
# img_dir = '/home/ai/data/VideoCapture/image_data/person_no/Highway_Crowded/'

def rename_pic_label(dir):
    basename = dir.split('/')[-2]
    # basename = dir
    file_list = os.listdir(dir)

    pic_list = [i for i in file_list if i.endswith('.jpg')]
    label_list = [i for i in file_list if i.endswith('.txt')]

    for pic in pic_list:
    # # #     old_name = os.path.join(dir, pic)
    # # #     new_name = os.path.join(dir, basename + "_" + str(int(pic[:-4])) + '.jpg')
        os.rename(os.path.join(dir, pic), os.path.join(dir, basename + "_" + str(int(pic[:-4])) + '.jpg'))
        # os.rename(os.path.join(dir, pic), os.path.join(dir, basename + "_" + str(int(pic.strip("frame")[:-4])) + '.jpg'))
    # #     # abs_pic_path = os.path.join(file_dir, dir, pic)
    # #     # if pic.startswith('frame'):
    # #     #     os.rename(os.path.join(file_dir, dir, pic),
    # #     #               os.path.join(file_dir, dir, basename + "_" + str(int(pic[:-4].strip('frame'))) + '.jpg'))
    # #     # else:
    # #     #     os.rename(os.path.join(file_dir, dir, pic), os.path.join(file_dir, dir, basename + "_" + str(int(pic.split('_')[:-4])) + '.jpg'))
    # #
        print("%s is been written..." %pic)

    for label in label_list:
        # pic_name = os.path.basename(label)[:-4] + '.jpg'
        # shutil.copy(os.path.join(img_dir, pic_name), os.path.join(dir, pic_name))
        # print('%s is been written...' % pic_name)

        # os.rename(os.path.join(dir, label), os.path.join(dir, basename + "_" + str(int(label[:-4])) + '.txt'))
        os.rename(os.path.join(dir, label),
                  os.path.join(dir, basename + "_" + str(int(label.strip("frame")[:-4])) + '.txt'))
        print('%s is been written...' %label)

rename_pic_label(dir)

# for root, dirs, files in os.walk(file_dir):
#     dir_list = dirs
#     pbar1 = tqdm(dir_list)
#     for each_dir in pbar1:
#     # for each_dir in dir_list:
#         # print(i)
#         rename_pic_label(os.path.join(file_dir, each_dir))
#         pbar1.set_description("Processing %s" % each_dir)