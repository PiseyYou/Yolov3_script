import numpy as np  
import sys,os  
import cv2
# from dataprocess import *
caffe_root = '/home/l/install/anaconda3/envs/py36/caffe/'
sys.path.insert(0, caffe_root + 'python')  
import caffe
from time import time


# net_file= 'deploy.prototxt'
# caffe_model='mobilenet_iter_73000.caffemodel'
net_file= '/home/l/install/anaconda3/envs/py36/MobileNet-SSD/deploy_no_bn.prototxt'
caffe_model='/home/l/install/anaconda3/envs/py36/MobileNet-SSD/mobilenet_iter_73000_no_bn.caffemodel'
test_dir = "images"

if not os.path.exists(caffe_model):
    print(caffe_model + " does not exist")
    exit()
if not os.path.exists(net_file):
    print(net_file + " does not exist")
    exit()
net = caffe.Net(net_file,caffe_model,caffe.TEST)  

CLASSES = ('background',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')


def timeCalc(func):
    import time
    def run(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("函数{0}的运行时间为： {1}".format(func.__name__, time.time() - start))
        return result
    return run

def fpsCalc(func):
    import time
    def run(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("函数{0}的运行帧率为： {1}".format(func.__name__, 1/(time.time() - start)))
        return result
    return run

def preprocess(src):
    img = cv2.resize(src, (300,300))
    img = img - 127.5
    img = img * 0.007843
    return img

def postprocess(img, out):   
    h = img.shape[0]
    w = img.shape[1]
    box = out['detection_out'][0,0,:,3:7] * np.array([w, h, w, h])

    cls = out['detection_out'][0,0,:,1]
    conf = out['detection_out'][0,0,:,2]
    return (box.astype(np.int32), conf, cls)

@timeCalc
def detect(imgfile):
    origimg = cv2.imread(imgfile)
    start_time = time()
    img = preprocess(origimg)
    
    img = img.astype(np.float32)
    img = img.transpose((2, 0, 1))

    net.blobs['data'].data[...] = img

    # netDect_time = time()
    out = net.forward()
    # netCost_time = time() - netDect_time
    # print("network cost time: %f" %netCost_time)

    box, conf, cls = postprocess(origimg, out)

    for i in range(len(box)):
       p1 = (box[i][0], box[i][1])
       p2 = (box[i][2], box[i][3])
       cv2.rectangle(origimg, p1, p2, (0,255,0))
       p3 = (max(p1[0], 15), max(p1[1], 15))
       title = "%s:%.2f" % (CLASSES[int(cls[i])], conf[i])
       cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (0, 255, 0), 1)
    elapsed = (time() - start_time)
    print("Mobilenet-SSD time cost: %.2f" % elapsed);
    fps = 1 / elapsed
    print("Estimated frames per second : %.2f" % fps)
    cv2.imshow("SSD", origimg)
 
    k = cv2.waitKey(0) & 0xff
        #Exit if ESC pressed
    if k == 27 : return False
    return True



def read_video(video_path):

    cap = cv2.VideoCapture(video_path)
    basename = os.path.basename(video_path)
    img_name = basename.split('.')[0]

    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fNUMS = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out_fps = 25
    output_movie = cv2.VideoWriter('/home/l/install/anaconda3/envs/py36/MobileNet-SSD/video_test/result/Mobilenet_SSD_test12_origin.mp4', fourcc, fps, size)

    while (cap.isOpened()):
        # 读帧
        ret, origimg = cap.read()
        # output_movie.write(origimg)
        if ret == True:
            start_time = time()

            img = preprocess(origimg)
            img = img.astype(np.float32)
            img = img.transpose((2, 0, 1))
            net.blobs['data'].data[...] = img

            netDect_time = time()
            out = net.forward()
            netCost_time = time() - netDect_time
            # print("network cost time: %f" % netCost_time)

            box, conf, cls = postprocess(origimg, out)

            for i in range(len(box)):
                p1 = (box[i][0], box[i][1])
                p2 = (box[i][2], box[i][3])
                cv2.rectangle(origimg, p1, p2, (255, 0, 0), 2)
                p3 = (max(p1[0], 15), max(p1[1], 15))
                title = "%s:%.2f" % (CLASSES[int(cls[i])], conf[i])
                cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (255, 0, 0), 2)

            elapsed = (time() - start_time)
            # print("Mobilenet-SSD time cost: %.2f" %elapsed)
            print("Estimated frames per second : %.2f" % (1/elapsed))

            output_movie.write(origimg)

            # cv2.imshow("Mobilenet-SSD", origimg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    output_movie.release()
    cv2.destroyAllWindows()


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

def fromVideo_getData(video_path):
    cap = cv2.VideoCapture(video_path)
    basename = os.path.basename(video_path)
    img_name = basename.split('.')[0]

    saveImgNum = 0
    while (cap.isOpened()):
        # 读帧
        ret, origimg = cap.read()

        # img_box = origimg.copy()
        # cv2.imshow("origimg", origimg)
        # cv2.waitKey(1)

        if ret == True:
            saveImgNum += 1
            img = preprocess(origimg)
            img = img.astype(np.float32)
            img = img.transpose((2, 0, 1))
            net.blobs['data'].data[...] = img

            out = net.forward()
            box, conf, cls = postprocess(origimg, out)

            if saveImgNum % 25 == 0:
                save_xml_dir = os.path.join(save_dir, "Annotations")
                if not os.path.exists(save_xml_dir):
                    os.makedirs(save_xml_dir)
                save_name = img_name + "_" + str(saveImgNum) + ".jpg"
                save_xml(origimg, save_name, box, cls, save_xml_dir)

                save_img_dir = os.path.join(save_dir, "JPEGImages")
                if not os.path.exists(save_img_dir):
                    os.makedirs(save_img_dir)

                cv2.imwrite(os.path.join(save_img_dir, save_name), origimg)
                print(save_name +" and " + save_name[:-4]+".xml files have been written....")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    # 对单张图片检测
    # detect("/home/l/Videos/sample_720p.jpg")

    # #对文件夹图片进行训练
    # for f in os.listdir(test_dir):
    #     if detect(test_dir + "/" + f) == False:
    #        break

    # 对视频进行检测
    # video_path = '/home/l/install/anaconda3/envs/py36/MobileNet-SSD/video_test/test12_origin.mp4'
    # read_video(video_path)
    # exit(0)

    # 从视频获取图片
    save_dir = "/home/l/install/anaconda3/envs/py36/MobileNet-SSD/create_lmdb/ImageAndXml"
    video_path = '/home/l/install/anaconda3/envs/py36/MobileNet-SSD/video_test/test4.mp4'
    fromVideo_getData(video_path)
