# Yolov3_script

## Three type script for yolov3 training:

* preDeal for dataset, trainDeal for prepare training, bakDeal for cal mAP and loss log.

### preDeal:
* The fold preDeal include (Json/xml) restrore from the annotations：
   * fold Json for json type.
      * getSelectId.py is try to get need pic from COCO data;<br>
      * getpicJson.py is try to split the pic;<br>
   
   * fold xml for xml type.
      * check_xml_pic.py main for 4 check:
         * check_1 for match pic and xml
         * check_2 for match type and xml[name]
         * check_3 for match the box whether overbounary.
         * selete_pic for choose the pic size over 416*416.
         * pic_label_rename_singdir.py for change all pic and label name with the same to the fold name.
	```
	python check_1.py
	python check_2.py
	python check_3.py
	python selete_pic.py
	python pic_label_rename_singdir.py
	```

	
### trainDeal:
* create_txt_list.py for get the origin name for each pic.
* voc_label_anyfold.py for get the Abs for every pic.
* pic_train_test.py for only image without xml files to split into train and test file.
	
	python create_txt_list.py
	python voc_label_anyfold.py
	python pic_train_test.py
	
### bakDeal:
* the fold log is used for get loss and iou.
* before use compute_mAP.py need to command this order:
	
	./darknet detector valid mask/mask.data mask/mask.cfg backup/mask.back -out "" -gpu 0 -thresh .5
	python compute_mAP.py  
	python computer_Single_All_mAP.py 
	
