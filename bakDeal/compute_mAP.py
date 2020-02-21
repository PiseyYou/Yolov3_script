from voc_eval import voc_eval
 
print(voc_eval('/home/pisey/anaconda3/envs/yolo/darknet/results/{}.txt', '/home/pisey/anaconda3/envs/yolo/darknet/mask/Annotations/{}.xml', '/home/pisey/anaconda3/envs/yolo/darknet/mask/ImageSets/Main/test.txt', 'nomask', '.'))

