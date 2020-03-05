import os

def check_fileExist(file):
    # nameList = []
    flag = True
    num = 0
    with open(file, 'r') as f:
        for line in f.readlines():
            # if os.path.isfile(str(line).rstrip()):
            if os.path.exists(str(line).rstrip()):
                num += 1
            else:
                print('%s is not exist, please check the file' %(str(line)))
                flag = False
        if flag:
            print('All %d file is exist.' %num)



def del_coco_line(infile, outfile):

    outf = open(outfile, "w")
    with open(infile, 'r') as f:
        for line in f.readlines():
            if line.startswith('/home/ai/data/coco/image_data/2014'):
                continue
            outf.writelines(line)
            print(line)
        outf.close()


def del_noPath(infile, outfile):
    outf = open(outfile, "w")
    num = 0

    with open(infile, 'r') as f:
        label_files = [(x.replace('py36/darknet/face_mask_ori/images', 'vino/darknet/data/mask/imagesAndlabel')[:-4] + '.txt') for x in f.read().splitlines()]
        nameList = []
        for line in label_files:
            nameList.append(line.rstrip())
        nameList = list(set(nameList))
            # if os.path.exists(line):
            #     num += 1
            #     outf.writelines(str(line) + '\n')
            # else:
            #     print('the %s is not exist.' % str(line))
        for line in nameList:
            if not os.path.exists(line):
                continue
            else:
                num +=1
                outf.writelines(line + '\n')

        print('total %d is exist' % (num))
        outf.close()


def compare_txt(existPath, existFile, outfile):
    all_fileName = next(os.walk(existPath))[2]
    txtList =[os.path.join(existPath, x) for x in all_fileName if x.endswith('.txt')]
    # txtList = list(set(txtList))
    outputFile = open(outfile, "w")
    num = 0
    nameList = []
    with open(existFile, 'r') as f:
        for line in f.readlines():
            nameList.append(line.rstrip())
        nameList = list(set(nameList))

        for i in nameList:
            # a = line.rstrip()
            if i not in txtList:
                print(i)
                continue
            else:
                num +=1
                outputFile.writelines(line)
        print('total %d label are written' %num)
    outputFile.close()



if __name__ == '__main__':
    # infile = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/Abs_trainval.txt'
    # outfile ='/home/pisey/anaconda3/envs/vino/darknet/data/mask/Abs_del_trainval.txt'
    # check_fileExist('/home/pisey/anaconda3/envs/py36/yolov3-channel-and-layer-pruning/coco/trainvalno5k.txt')
	# del_coco_line('valid_coco_person_and_bus_vedio_noperson_truck_car_bus_person_shuffle.txt', "valid_no_coco.txt")

    existPath = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/imagesAndlabel'
    existFile = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/Abs_del_trainval.txt'
    # existFile = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/seLabel.txt'
    outfile = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/test_output.txt'
    # del_noPath(infile, outfile)
    # check_fileExist(outfile)
    compare_txt(existPath, existFile, outfile)
