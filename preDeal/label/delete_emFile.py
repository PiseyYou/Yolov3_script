import  os

def delete_emFile(txtPath, annoPath, picPath):
	files = os.listdir(txtPath)
	for file in files:
		with open(os.path.join(txtPath, file), 'r') as f:
			contends =f.read()
			if contends == '':
				# os.remove(dir_path+file)
				# os.remove(os.path.join(txtPath, file))
				# # a = os.path.join(annoPath, str(file)[:-4] + '.xml')
				# os.remove(os.path.join(annoPath, str(file)[:-4] + '.xml'))
				# os.remove(os.path.join(picPath, str(file)[:-4] + '.jpg'))
				print(str(file) + " is empty, the label/anno/pic will be delete!")
			else:
				continue
	print('all empty file are been delete')


def delete_emPic(labelPath, picPath):
	files = os.listdir(labelPath)
	for file in files:
		with open(os.path.join(labelPath, file), 'rb') as f:
			contends =f.read()
			if contends == '':
				# os.remove(dir_path+file)
				os.remove(os.path.join(labelPath, file))
				# # a = os.path.join(annoPath, str(file)[:-4] + '.xml')
				# os.remove(os.path.join(annoPath, str(file)[:-4] + '.xml'))
				# os.remove(os.path.join(picPath, str(file)[:-4] + '.jpg'))
				print(str(file) + " is empty, the label/anno/pic will be delete!")
			else:
				continue
	print('all empty file are been delete')


labelPath = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/imagesAndlabel'
picPath = '/home/pisey/anaconda3/envs/vino/darknet/data/mask/imagesAndlabel'
# annoPath = '/home/supernode/anaconda3/envs/py36/darknet/face_mask_ori/Annotataions'
# picPath = '/home/supernode/anaconda3/envs/py36/darknet/face_mask_ori/images'

delete_emPic(labelPath, picPath)
