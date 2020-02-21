# Test
script 分为 数据集处理——preDeal, 训练准备——trainDeal 和后处理——bakDeal

preDeal:
	包括xml标注文件还原pic: xml fold
	   Json标注文件还原pic: json fold
	
	标注文件和图片对应检查，种类检查，越界检查，筛选图片：check_xml_pic.py
	批量更改xml文件名
