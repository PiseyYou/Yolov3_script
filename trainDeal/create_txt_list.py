import os  
import random
from tqdm import tqdm
  
xmlfilepath=r'/home/supernode/anaconda3/envs/helmet/trafficSystem_8type/Annotations'
saveBasePath=r'/home/supernode/anaconda3/envs/helmet/trafficSystem_8type'
  
trainval_percent = 0.85
train_percent = 0.7
total_xml = os.listdir(xmlfilepath)
total_xml = os.listdir(xmlfilepath)

# num=len(total_xml)//2 # the pic and anno is in the same fold
num=len(total_xml)
list=range(num)
tv=int(num*trainval_percent)    
tr=int(tv*train_percent)
te=int(num*(1-trainval_percent))
trainval= random.sample(list, tv)
train=random.sample(trainval, tr)
  
print("train and val size", tv)
# print("train size",tr)
print("test size", te)
ftrainval = open(os.path.join(saveBasePath, 'trainval.txt'), 'w')
ftest = open(os.path.join(saveBasePath, 'test.txt'), 'w')
# ftrain = open(os.path.join(saveBasePath,'train.txt'), 'w')
# fval = open(os.path.join(saveBasePath,'val.txt'), 'w')
  
for i in tqdm(list):
    name = total_xml[i][:-4]+'\n'
    if i in trainval:    
        ftrainval.write(name)    
        # if i in train:
        #     ftrain.write(name)
        # else:
        #     fval.write(name)
    else:    
        ftest.write(name)    
    
ftrainval.close()    
# ftrain.close()
# fval.close()
ftest .close() 

