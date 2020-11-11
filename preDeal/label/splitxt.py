import os, shutil

def movePic(srcfileDir, dstfileDir):
	if not os.path.exists(dstfileDir):
		os.mkdir(dstfileDir)
	num = 0
	for i in os.listdir(srcfileDir):

		#对不同后缀名格式的图片
		ext = ['.jpg', '.png', '.JPG', '.bmp']
		if i.endswith(tuple(ext)):
			# srcfileDir = os.path.join(basePath,"a",i)
			# shutil.move(os.path.join(basePath,"imageAndlabel",i), dstfileDir)
			shutil.move(os.path.join(basePath,"imageAndlabel",i), dstfileDir)
			num+=1
	print("total %d file had been move" %num)


def moveFile(srcfileDir, dstfileDir):
	if not os.path.exists(dstfileDir):
		os.mkdir(dstfileDir)
	num = 0
	for i in os.listdir(srcfileDir):
		if i.endswith("txt"):
			# srcfileDir = os.path.join(basePath,"a",i)
			# shutil.move(os.path.join(basePath,"imageAndlabel",i), dstfileDir)
			shutil.move(os.path.join(basePath,"imageAndlabel",i), dstfileDir)
			num+=1
	print("total %d file had been move" %num)



def renamePic(srcfileDir, suffix):
	renameNum = 0
	for i in os.listdir(srcfileDir):
		portion = os.path.splitext(i)  # 分离文件名与扩展名
		# 如果后缀是jpg
		if portion[1] != suffix:
			# 重新组合文件名和后缀名
			newname = portion[0] + suffix
			os.rename(srcfileDir+i, srcfileDir+newname)
			renameNum +=1
	jpgNum = 0
	for j in os.listdir(srcfileDir):
		if j.endswith("jpg"):
			jpgNum +=1

	print("there are now total %d type .jpg, %d pic had been rename" %(jpgNum, renameNum))


# basePath = "/home/ai/PycharmProjects/dataSetDeal/txt2voc/"
# movePic(os.path.join(basePath,"a"),os.path.join(basePath,"b"))

# basePath = "/home/ai/anaconda3/envs/helmet/trafficSystem_8type/"
# movePic(os.path.join(basePath,"imageAndlabel"),os.path.join(basePath,"JPEGImages"))

basePath = "/home/ai/anaconda3/envs/helmet/trafficSystem_8type/"
moveFile(os.path.join(basePath,"imageAndlabel"),os.path.join(basePath,"labels"))



# srcfileDir = "/home/ai/PycharmProjects/dataSetDeal/txt2voc/b/"
# renamePic(srcfileDir,".jpg")

# srcfileDir = "/home/ai/anaconda3/envs/helmet/trafficSystem_8type/JPEGImages/"
# renamePic(srcfileDir,".jpg")