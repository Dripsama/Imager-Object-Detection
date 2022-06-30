from PIL import Image
import numpy as np
from numpy import expand_dims
import requests
import json
from utilities import *

def new_method(path):
	#change location of image
	img=Image.open(path)
	print("image size:", img.size)
	imgw = img.size[0]
	imgh = img.size[1]
	
	# img.show()
	new_img = make_square(img)
	new_img=new_img.resize((416,416))
	# new_img.show()

	arr = np.asarray(new_img)
	# arr = np.asarray(img.resize((416,416)))
	shape = arr.shape
	print("image size as array:", shape)
	# arr = arr.reshape(1, *shape)
	arr = expand_dims(arr,0)
	print("converted to 4d tensor:",arr.shape)
	float_array = arr.astype(np.float)
	float_array=float_array/255.0

	base_url='http://localhost:8501/v1/models/test'
	resp=requests.get(base_url,verify=False)

	data = json.dumps({"signature_def":"serving_default","instances":float_array.tolist()})
	headers={"content-type":"application/json"}

	rep=requests.post("http://localhost:8501/v1/models/test:predict",data=data,headers=headers)
    # print(rep.text)
	res=(json.loads(rep.text)['predictions'][0])
	# print(len(res))
	temp=np.asarray(res)
	temp=expand_dims(temp,0)
	print(temp.shape)
	anchs=np.array([(1.3221, 1.73145),(3.19275, 4.00944),(5.05587, 8.09892),(9.47112, 4.84053),(11.2364, 10.0071)])
	cl=np.array(["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck",
    	"boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    	"bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    	"backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
   	 	"sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    	"tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
    	"apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
    	"chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse",
    	"remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
    	"book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
	])
	boxes, scores, classes=raw2Box(temp, anchors=anchs, numClass=len(cl), imgw =imgw, imgh=imgh,scoreThresh=0.5, iouThresh=0.6)
	boxes_arr = (convertbox(boxes.numpy())).astype('float64')
	scores_arr = scores.numpy().astype('float64')
	classes_arr = classes.numpy()
	size = len(boxes_arr)
	output_list = []
	for i in range(0,size):
		# boxes_arr[i][0], boxes_arr[i][1], boxes_arr[i][2], boxes_arr[i][3] = boxes_arr[i][0], boxes_arr[i][1]*imgh/imgw, boxes_arr[i][2], boxes_arr[i][3]*imgw/imgh
		# boxes_arr[i][0] = np.clip(boxes_arr[i][0], a_min=0, a_max=img.size[1])
		# boxes_arr[i][1] = np.clip(boxes_arr[i][1], a_min=0, a_max=img.size[0])
		nx=img.size[0]/416.0
		ny=img.size[1]/416.0
		boxes_arr[i][2], boxes_arr[i][3] = boxes_arr[i][2]*ny, boxes_arr[i][3]*nx

		item  = {'bbox' : boxes_arr[i].tolist(), 'class' : cl[classes_arr[i]], 'score' : scores_arr[i]}
		output_list.append(item)
	
	print(output_list)
	return output_list
	# painter = Visualizer(cl)
	# fig = painter.drawBox(img, boxes.numpy(), scores.numpy(), classes.numpy())
	# plt.show()