import os
import random
from tqdm import tqdm

if __name__ == '__main__':
    source_folder='/home/supernode/anaconda3/envs/helmet/trafficSystem_8type/JPEGImages'
    saveBasePath = '/home/supernode/anaconda3/envs/helmet/trafficSystem_8type/'

    trainval_percent = 0.85
    train_percent = 0.7

    total_images = os.listdir(source_folder)
    num=len(total_images) # the pic and anno is in the same fold

    list=range(num)
    tv=int(num*trainval_percent)
    tr=int(tv*train_percent)
    te=int(num*(1-trainval_percent))

    trainval= random.sample(list,tv)
    print("train and val size",tv)
    print("test size", te)

    ftrainval = open(os.path.join(saveBasePath, 'trainval.txt'), 'w')
    ftest = open(os.path.join(saveBasePath, 'test.txt'), 'w')

    pbar = tqdm(list)
    for i in pbar:
        abs_pic_path = os.path.join(source_folder, total_images[i])
        if i in trainval:
            ftrainval.write(abs_pic_path + '\n')
        else:
            ftest.write(abs_pic_path + '\n')
    pbar.set_description("Processing %s" % i)
    ftrainval.close()
    ftest .close()

